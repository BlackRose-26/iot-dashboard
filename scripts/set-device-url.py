"""Send the current tunnel address to the USB-connected cabinet. No reflash needed.

The firmware accepts "STACK-URL https://<host>.trycloudflare.com" on its USB serial
port, stores it in its own NVS settings (never the game journal) and reconnects. The
port is opened with DTR/RTS off so the ESP32 is not reset. Uses the installed Arduino
CLI serial monitor; no extra Python packages.

  python scripts/set-device-url.py                 # address from .tools/free-online/current-url.txt
  python scripts/set-device-url.py --url https://example.trycloudflare.com --port COM5
"""
import argparse
import importlib.util
import os
import queue
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = re.compile(r'https://[a-z0-9-]+(?:\.[a-z0-9-]+)*\.trycloudflare\.com')


def flash_helpers():
    spec = importlib.util.spec_from_file_location('flash_device', ROOT/'scripts'/'flash-device.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def send(cli, port, url, seconds):
    command = [cli, 'monitor', '-p', port, '-q', '-c', 'baudrate=115200,dtr=off,rts=off']
    monitor = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, encoding='utf-8', errors='replace', bufsize=1)
    lines = queue.Queue()
    threading.Thread(target=lambda: [lines.put(line) for line in monitor.stdout], daemon=True).start()
    deadline = time.monotonic() + seconds
    next_send = 0.0
    try:
        while time.monotonic() < deadline:
            if monitor.poll() is not None:
                return False, 'The serial port could not be opened (is another serial monitor using it?).'
            if time.monotonic() >= next_send:  # repeat until the cabinet answers (it may still be booting)
                monitor.stdin.write(f'STACK-URL {url}\n'); monitor.stdin.flush(); next_send = time.monotonic() + 2
            try: line = lines.get(timeout=0.25).strip()
            except queue.Empty: continue
            if line.startswith('STACK-URL-OK'): return True, line
            if line.startswith('STACK-URL-REJECTED'):
                if 'busy' in line: continue  # a round is in progress; keep retrying until it ends
                return False, line
        return False, 'No answer from the cabinet. Is the stack firmware (24 Nov or newer) flashed and running?'
    finally:
        monitor.kill()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--url')
    parser.add_argument('--port', default=os.getenv('STACK_ESP32_PORT'))
    parser.add_argument('--seconds', type=int, default=30)
    parser.add_argument('--if-present', action='store_true', help='Exit quietly when no cabinet is plugged in.')
    args = parser.parse_args()
    url = (args.url or (ROOT/'.tools'/'free-online'/'current-url.txt').read_text(encoding='utf-8')).strip().rstrip('/')
    if not URL.fullmatch(url): raise SystemExit('Use the https://<name>.trycloudflare.com address printed by the launcher.')
    helpers = flash_helpers()
    cli = helpers.arduino_cli()
    try: port = args.port or helpers.detect_port(cli)
    except SystemExit as reason:
        if args.if_present and 'No USB serial board' in str(reason):
            print('No cabinet on USB; plug it in and run: npm run device:url'); return
        raise
    ok, detail = send(cli, port, url, args.seconds)
    print(f'Cabinet on {port}: {detail}')
    if not ok: sys.exit(1)


if __name__ == '__main__': main()
