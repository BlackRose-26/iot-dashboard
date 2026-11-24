"""Event load rehearsal: many phones and an operator running rounds, on a throwaway database.

  backend\\.venv\\Scripts\\python.exe backend\\rehearse_event.py                      loopback, 60 phones, 5 min
  backend\\.venv\\Scripts\\python.exe backend\\rehearse_event.py --players 80 --minutes 10
  backend\\.venv\\Scripts\\python.exe backend\\rehearse_event.py --tunnel             through a temporary Cloudflare tunnel

Each synthetic phone scans (entry grant), registers, keeps the live-update connection open
like the app does, re-reads its ticket on every update (and every 15 s as a fallback), and
leaves 5 s after seeing its result. The operator polls the dashboard every 2 s and runs
simulated rounds back to back: ready, Call next player, start, then a win or loss.

Uses only a generated disposable database and port 8001; the event database is never
opened. --tunnel exposes that throwaway server at a random trycloudflare.com address for
the length of the run (synthetic data only) to measure the real internet path. The summary
is written to docs/ui-review/load-rehearsal-<mode>.json and holds timings and counts only.
"""
import os
os.environ['STACK_SKIP_DEFAULT_APP'] = '1'
import argparse
import base64
import json
import re
import subprocess
import sys
import threading
import time
import uuid
from dataclasses import replace
from pathlib import Path

import httpx
from sqlalchemy.engine import make_url

ROOT = Path(__file__).resolve().parents[1]
HIDDEN = {'creationflags': subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}
PASSWORD = 'Only-a-disposable-test-password'
LIMITS = {'loopback': {'p95_ms': 1000, 'result_p95_ms': 5000}, 'tunnel': {'p95_ms': 2500, 'result_p95_ms': 8000}}


def percentile(values, share):
    if not values: return None
    ordered = sorted(values)
    return round(ordered[min(len(ordered)-1, int((len(ordered)-1)*share))], 1)


class Recorder:
    def __init__(self):
        self.lock = threading.Lock(); self.timings = {}; self.errors = []; self.ws_drops = 0
        self.result_seen = {}; self.finished_at = {}; self.joined = []; self.called = []

    def timed(self, name, call):
        started = time.perf_counter()
        try:
            response = call()
        except httpx.HTTPError as error:
            with self.lock: self.errors.append(f'{name}: {type(error).__name__}')
            return None
        elapsed = (time.perf_counter()-started)*1000
        with self.lock:
            self.timings.setdefault(name, []).append(elapsed)
            if response.status_code >= 500 or response.status_code in (401, 403, 429):
                self.errors.append(f'{name}: HTTP {response.status_code}')
        return response


def start_tunnel():
    exe = ROOT/'.tools'/'free-online'/('cloudflared.exe' if os.name == 'nt' else 'cloudflared')
    if not exe.is_file():
        raise SystemExit('Install the tunnel helper first: backend\\.venv\\Scripts\\python.exe scripts\\install-cloudflared.py')
    child = subprocess.Popen([str(exe), 'tunnel', '--url', 'http://127.0.0.1:8001', '--protocol', 'http2', '--no-autoupdate'],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, **HIDDEN)
    found = {}

    def read():
        for line in child.stdout:
            match = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com\b', line)
            if match and 'url' not in found: found['url'] = match.group(0)
    threading.Thread(target=read, daemon=True).start()
    for _ in range(120):
        if 'url' in found: return child, found['url']
        if child.poll() is not None: break
        time.sleep(.5)
    child.kill()
    raise SystemExit('The temporary tunnel did not start.')


def wait_ready(base, child, seconds=90):
    for _ in range(seconds*2):
        if child.poll() is not None: raise SystemExit('The rehearsal server stopped while starting.')
        try:
            if httpx.get(base+'/api/health', timeout=5).status_code == 200: return
        except httpx.HTTPError: pass
        time.sleep(.5)
    raise SystemExit(f'{base} did not become ready.')


def phone(index, base, token, rec, stop):
    from websockets.sync.client import connect
    nickname = f'Rehearsal {index:03d}'
    headers = {'Origin': base}
    with httpx.Client(base_url=base, headers=headers, timeout=30) as client:
        if not rec.timed('entry', lambda: client.post('/api/player/entry', json={'qrContent': base+'/join/'+token, 'method': 'camera'})):
            return
        csrf = client.get('/api/player/context').json()['csrf']
        client.headers['X-CSRF-Token'] = csrf
        response = rec.timed('register', lambda: client.post('/api/player/register', json={
            'nickname': nickname, 'studentId': f'REHEARSAL-{uuid.uuid4().hex[:10]}', 'acknowledged': True}))
        if response is None or response.status_code != 200:
            with rec.lock: rec.errors.append(f'register: HTTP {getattr(response, "status_code", "none")}')
            return
        with rec.lock: rec.joined.append(nickname)
        cookie = '; '.join(f'{c.name}={c.value}' for c in client.cookies.jar)
        ws_url = base.replace('https://', 'wss://').replace('http://', 'ws://')+'/api/live/player'
        state = {'leave_at': None}

        def refresh():
            """Re-read the ticket like the app does; return True once the phone should leave."""
            response = rec.timed('player context', lambda: client.get('/api/player/context'))
            ticket = response.json().get('ticket') if response is not None and response.status_code == 200 else None
            if ticket and ticket.get('outcome') and nickname not in rec.result_seen:
                with rec.lock:
                    finished = rec.finished_at.get(nickname)
                    rec.result_seen[nickname] = (time.perf_counter()-finished)*1000 if finished else None
                state['leave_at'] = time.monotonic()+5
            return bool(state['leave_at'] and time.monotonic() > state['leave_at'])

        while not stop.is_set():
            try:
                with connect(ws_url, additional_headers={'Cookie': cookie, 'Origin': base}, open_timeout=20) as socket:
                    while not stop.is_set():
                        try: socket.recv(timeout=15)
                        except TimeoutError: pass  # fallback refresh, as the app does
                        if refresh(): return
            except Exception:
                with rec.lock: rec.ws_drops += 1
                if refresh(): return
                time.sleep(5)


def operator(base, rec, stop, game_seconds):
    headers = {'Origin': base}
    with httpx.Client(base_url=base, headers=headers, timeout=30) as admin:
        assert admin.post('/api/admin/login', json={'username': 'admin', 'password': PASSWORD}).status_code == 200
        admin.headers['X-CSRF-Token'] = admin.get('/api/admin/session').json()['csrf']
        rounds = 0

        def post(path):
            return rec.timed(path.rsplit('/', 1)[-1], lambda: admin.post(path, headers={'Idempotency-Key': str(uuid.uuid4())}))
        while not stop.is_set():
            snap = rec.timed('admin snapshot', lambda: admin.get('/api/admin/snapshot'))
            if snap is None or snap.status_code != 200: time.sleep(2); continue
            data = snap.json()
            if data['currentPlayer'] is None and data['queue']:
                post('/api/admin/simulator/ready')
                called = post('/api/admin/queue/call-next')
                if called is None or called.status_code != 200: time.sleep(2); continue
                current = admin.get('/api/admin/snapshot').json()['currentPlayer']
                with rec.lock: rec.called.append(current['nickname'])
                time.sleep(2)  # walking to the cabinet
                post('/api/admin/simulator/start')
                time.sleep(game_seconds)
                outcome = 'win' if rounds % 3 == 0 else 'loss'
                done = post(f'/api/admin/simulator/{outcome}')
                if done is not None and done.status_code == 200:
                    with rec.lock: rec.finished_at[current['nickname']] = time.perf_counter()
                rounds += 1
            else:
                time.sleep(2)
        return rounds


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--players', type=int, default=60)
    parser.add_argument('--minutes', type=float, default=5)
    parser.add_argument('--join-every', type=float, default=2.0, help='Seconds between new phones joining.')
    parser.add_argument('--game-seconds', type=float, default=8.0, help='Compressed round length.')
    parser.add_argument('--tunnel', action='store_true')
    args = parser.parse_args(argv)

    sys.path.insert(0, str(ROOT/'backend'/'tests'))
    from test_player_flow import environment
    from check_quality import test_database
    generator = environment.__wrapped__()
    _, _, token, engine, settings = next(generator)
    database = test_database(make_url(settings.database_url).database)
    children = []
    rec = Recorder(); stop = threading.Event()
    mode = 'tunnel' if args.tunnel else 'loopback'
    try:
        base = 'http://127.0.0.1:8001'
        if args.tunnel:
            # The throwaway server is public for the run: never use the fixed test password there.
            import secrets
            from app.security import passwords
            global PASSWORD
            PASSWORD = secrets.token_urlsafe(24)
            with engine.begin() as c:
                c.exec_driver_sql("UPDATE staff_users SET password_hash=%s WHERE username='admin'", (passwords.hash(PASSWORD),))
            tunnel, base = start_tunnel(); children.append(tunnel)
        env = dict(os.environ, STACK_DATABASE_URL=settings.database_url, STACK_PUBLIC_URL=base,
                   STACK_DEVICE_TOKEN=settings.device_token, STACK_AI_ENABLED='false')
        env.update({f'STACK_{name}_KEY': base64.urlsafe_b64encode(value).decode()
                    for name, value in [('IDENTITY', settings.identity_key), ('LOOKUP', settings.lookup_key), ('CSRF', settings.csrf_key)]})
        api = subprocess.Popen([sys.executable, 'check_quality.py', '--serve'], cwd=ROOT/'backend', env=env, **HIDDEN)
        children.append(api)
        wait_ready(base, api)
        print(f'Rehearsal ({mode}): {args.players} phones over {args.minutes:g} min against a throwaway database.', flush=True)

        ops = {}
        op_thread = threading.Thread(target=lambda: ops.setdefault('rounds', operator(base, rec, stop, args.game_seconds)), daemon=True)
        op_thread.start()
        phones = []
        ends = time.monotonic()+args.minutes*60
        for index in range(args.players):
            if time.monotonic() > ends: break
            thread = threading.Thread(target=phone, args=(index, base, token, rec, stop), daemon=True)
            thread.start(); phones.append(thread)
            time.sleep(args.join_every)
        while time.monotonic() < ends: time.sleep(1)
        stop.set(); op_thread.join(timeout=60)
        for thread in phones: thread.join(timeout=30)

        # FIFO: the called players must be exactly the earliest registrations, in order.
        fifo = rec.called == rec.joined[:len(rec.called)]
        with engine.connect() as c:
            duplicate_results = c.exec_driver_sql('''SELECT COUNT(*) FROM (SELECT queue_entry_id FROM game_sessions
              WHERE score IS NOT NULL GROUP BY queue_entry_id HAVING COUNT(*)>1) d''').scalar()
        results = [v for v in rec.result_seen.values() if v is not None]
        everything = [v for values in rec.timings.values() for v in values]
        limit = LIMITS[mode]
        summary = {
            'mode': mode, 'players_started': len(phones), 'players_registered': len(rec.joined),
            'minutes': args.minutes, 'rounds_completed': ops.get('rounds', 0), 'fifo_order_kept': fifo,
            'duplicate_results': int(duplicate_results), 'errors': len(rec.errors), 'error_kinds': sorted(set(rec.errors))[:10],
            'live_connection_drops': rec.ws_drops, 'requests': len(everything),
            'p50_ms': percentile(everything, .5), 'p95_ms': percentile(everything, .95), 'max_ms': percentile(everything, 1),
            'by_endpoint': {name: {'n': len(v), 'p50_ms': percentile(v, .5), 'p95_ms': percentile(v, .95), 'max_ms': percentile(v, 1)}
                            for name, v in sorted(rec.timings.items())},
            'result_visible_on_phone_ms': {'n': len(results), 'p50': percentile(results, .5), 'p95': percentile(results, .95)},
            'limits': limit,
        }
        summary['passed'] = bool(fifo and not duplicate_results and not rec.errors and summary['p95_ms'] is not None
                                 and summary['p95_ms'] <= limit['p95_ms'] and results
                                 and summary['result_visible_on_phone_ms']['p95'] <= limit['result_p95_ms'])
        out = ROOT/'docs'/'ui-review'/f'load-rehearsal-{mode}.json'
        out.write_text(json.dumps({'run_at': time.strftime('%Y-%m-%dT%H:%M:%S'), **summary}, indent=2), encoding='utf-8')
        print(json.dumps({k: summary[k] for k in ('passed', 'players_registered', 'rounds_completed', 'fifo_order_kept',
                                                  'duplicate_results', 'errors', 'live_connection_drops', 'p50_ms', 'p95_ms',
                                                  'max_ms', 'result_visible_on_phone_ms')}, indent=2))
        print(f'Saved {out.relative_to(ROOT)}')
        return 0 if summary['passed'] else 1
    finally:
        stop.set()
        for child in reversed(children):
            if child.poll() is None: child.kill(); child.wait(timeout=10)
        engine.dispose()
        assert database.startswith('stack_moko_test_')
        try: next(generator)
        except StopIteration: pass


if __name__ == '__main__':
    sys.exit(main())
