"""Opt-in loopback load, process restart and synthetic backup/restore checks.

Uses only uniquely generated test databases and dedicated ports. Never opens the
configured event database. Run after the frontend production build.
"""
import os
os.environ['STACK_SKIP_DEFAULT_APP']='1'
import base64
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import json
from pathlib import Path
import queue
import re
import shutil
import subprocess
import sys
import threading
import time

import httpx
import pymysql
from fastapi.testclient import TestClient
from sqlalchemy.engine import make_url

from app.config import Settings
from app.database import execute, one, all_rows
from app.game import simulated_result
from app.main import create_app
from run_browser_tests import executable, wait_for

ROOT=Path(__file__).resolve().parents[1]
HIDDEN={'creationflags':subprocess.CREATE_NO_WINDOW} if os.name=='nt' else {}


def test_database(name):
    if not re.fullmatch(r'stack_moko_test_[a-f0-9]{10}',name or ''):
        raise RuntimeError('This check only permits generated disposable test databases.')
    return name


def serve():
    import uvicorn
    settings=Settings.load()
    test_database(make_url(settings.database_url).database)
    app=create_app(settings)
    if os.getenv('STACK_TEST_DEFER_OUTBOX')=='1': app.state.live.interval=3600
    uvicorn.run(app,host='127.0.0.1',port=8001,access_log=False,log_level='error',
                ws_max_size=1024,ws_max_queue=4)


def percentile(values,percent):
    return round(sorted(values)[min(len(values)-1,int((len(values)-1)*percent))],2)


def main():
    import socket
    import secrets
    sys.path.insert(0,str(ROOT/'backend/tests'))
    from test_player_flow import environment,join,post,accept_command
    for port in (8001,5174):
        with socket.socket() as probe:
            if probe.connect_ex(('127.0.0.1',port))==0:
                raise RuntimeError(f'Dedicated test port {port} is occupied.')
    node=executable([os.getenv('STACK_TEST_NODE'),shutil.which('node'),
        *sorted((Path(os.getenv('LOCALAPPDATA',''))/'Programs').glob('node-v*-win-x64/node.exe'),reverse=True)])
    browser=executable([os.getenv('STACK_TEST_BROWSER_PATH'),
        Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'),
        Path('C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe')])
    if not node or not browser: raise RuntimeError('Node and a supported browser are required.')
    if not (ROOT/'frontend/dist/index.html').is_file(): raise RuntimeError('Build the frontend first.')
    generator=environment.__wrapped__()
    fixture,_,token,engine,settings=next(generator)
    settings=replace(settings,public_url='http://127.0.0.1:5174',ai_enabled=False)
    database=test_database(make_url(settings.database_url).database)
    app=create_app(settings)
    children=[]
    restored=None
    dump=ROOT/('.tools/run/quality-synthetic-'+secrets.token_hex(5)+'.sql')
    result={}
    try:
        players=[join(app,token,index) for index in range(50)]
        cookies=[[{'name':c.name,'value':c.value,'domain':'127.0.0.1','path':c.path,'httpOnly':True}
                  for c in player.cookies.jar if c.name=='sm_player'] for player in players]
        env=dict(os.environ,STACK_DATABASE_URL=settings.database_url,STACK_PUBLIC_URL=settings.public_url,
                 STACK_API_TARGET='http://127.0.0.1:8001',STACK_DEVICE_TOKEN=settings.device_token,STACK_AI_ENABLED='false')
        env.update({f'STACK_{name}_KEY':base64.urlsafe_b64encode(value).decode()
            for name,value in [('IDENTITY',settings.identity_key),('LOOKUP',settings.lookup_key),('CSRF',settings.csrf_key)]})
        def start_api(deferred=False):
            child=subprocess.Popen([sys.executable,__file__,'--serve'],cwd=ROOT/'backend',
                env=dict(env,STACK_TEST_DEFER_OUTBOX='1' if deferred else '0'),**HIDDEN)
            children.append(child)
            wait_for('http://127.0.0.1:8001/api/health',[child])
            return child
        def stop(child):
            child.kill();child.wait(timeout=10)
            children.remove(child)
        api=start_api()
        preview=subprocess.Popen([node,'node_modules/vite/bin/vite.js','preview','--host','127.0.0.1','--port','5174','--strictPort'],
            cwd=ROOT/'frontend',env=env,stdout=subprocess.DEVNULL,**HIDDEN)
        children.append(preview);wait_for(settings.public_url+'/api/health',[api,preview])
        browser_process=subprocess.Popen([node,'e2e/quality-checks.mjs'],cwd=ROOT/'frontend',env=env,
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True,encoding='utf-8',**HIDDEN)
        children.append(browser_process)
        messages=queue.Queue()
        def consume():
            for line in browser_process.stdout:
                try: messages.put(json.loads(line))
                except json.JSONDecodeError: messages.put({'stage':'error','message':'Invalid browser check output'})
        threading.Thread(target=consume,daemon=True).start()
        def send(value):
            browser_process.stdin.write(json.dumps(value)+'\n');browser_process.stdin.flush()
        def receive(stage):
            value=messages.get(timeout=180)
            if value.get('stage')!=stage: raise RuntimeError('Synthetic browser stage failed: '+str(value))
            print('Browser check: '+stage,flush=True)
            return value
        send({'url':settings.public_url,'browser':browser,'cookies':cookies})
        assert receive('ready')['clients']==50
        admin=httpx.Client(base_url=settings.public_url,timeout=20)
        assert admin.post('/api/admin/login',json={'username':'admin','password':'Only-a-disposable-test-password'}).status_code==200
        admin.headers['X-CSRF-Token']=admin.get('/api/admin/session').json()['csrf']
        started=int(time.time()*1000)
        assert post(admin,'/api/admin/admissions',{'open':False}).status_code==200
        send({'action':'observe','text':'The operator has paused the queue. Your place is saved; wait for it to reopen.','startedAt':started})
        fanout=receive('observed')
        assert fanout['browserErrors']==0
        result['loopback_50_clients']={'clients':50,'ui_update_ms_p50':percentile(fanout['latencies'],.5),
            'ui_update_ms_p95':percentile(fanout['latencies'],.95),'ui_update_ms_max':max(fanout['latencies']),'browser_errors':0}
        def request(index):
            start=time.perf_counter()
            response=httpx.get(settings.public_url+'/api/player/context',cookies=dict(players[index%50].cookies),timeout=20)
            assert response.status_code==200 and response.json()['ticket']['status']=='waiting'
            return (time.perf_counter()-start)*1000
        with ThreadPoolExecutor(max_workers=20) as pool: latencies=list(pool.map(request,range(250)))
        result['loopback_context_requests']={'requests':250,'concurrency':20,'p50_ms':percentile(latencies,.5),'p95_ms':percentile(latencies,.95),'errors':0}
        send({'action':'one'});receive('one')
        stop(api);api=start_api(True)
        send({'action':'live'});receive('live')
        assert post(admin,'/api/admin/admissions',{'open':True}).status_code==200
        device=httpx.Client(base_url=settings.public_url,headers={'X-Device-Token':settings.device_token},timeout=20)
        assert device.post('/api/device/heartbeat',json={'state':'ready','firmware':'synthetic-quality-check'}).status_code==200
        session=post(admin,'/api/admin/queue/call-next').json()['sessionId']
        accept_command(device)
        assert device.post(f'/api/device/sessions/{session}/start').status_code==200
        time.sleep(3)
        payload=simulated_result('loss')
        response=device.post(f'/api/device/sessions/{session}/result',json=payload)
        assert response.status_code==200,response.text
        original=response.json()
        stop(api)
        with engine.connect() as c:
            pending=one(c,'SELECT COUNT(*) n FROM outbox_events WHERE published_at IS NULL')['n']
            assert pending>0
        api=start_api()
        send({'action':'observe','text':'Game finished. Thanks for playing!','startedAt':int(time.time()*1000)})
        recovery=receive('observed')
        assert recovery['browserErrors']==0
        replay=device.post(f'/api/device/sessions/{session}/result',json=payload)
        assert replay.status_code==200 and replay.json()==original
        with engine.connect() as c:
            assert one(c,"SELECT COUNT(*) n FROM game_sessions WHERE status='completed'")['n']==1
            assert one(c,'SELECT COUNT(*) n FROM player_notifications')['n']==1
        result['process_restart']={'pending_outbox_before_restart':pending,'result_replayed_once':True,
            'completed_rounds':1,'notifications':1,'browser_recovered':True,'recovery_ms':max(recovery['latencies'])}
        send({'action':'close'});browser_process.wait(timeout=20);children.remove(browser_process)
        stop(api);stop(preview);admin.close();device.close()
        # Exercise the actual XAMPP dump/restore tools, never the real event database.
        restored=test_database('stack_moko_test_'+secrets.token_hex(5))
        dump.parent.mkdir(exist_ok=True,parents=True)
        database_args=['--host=127.0.0.1','--user=root']
        dump_env=dict(os.environ,MYSQL_PWD=os.getenv('STACK_DB_ROOT_PASSWORD',''))
        with dump.open('wb') as output:
            subprocess.run(['C:/xampp/mysql/bin/mysqldump.exe','--no-defaults',*database_args,
                '--single-transaction','--skip-comments','--hex-blob',database],stdout=output,env=dump_env,check=True,**HIDDEN)
        root=pymysql.connect(host='127.0.0.1',user='root',password=os.getenv('STACK_DB_ROOT_PASSWORD',''),autocommit=True)
        try:
            with root.cursor() as c: c.execute(f'CREATE DATABASE `{restored}` CHARACTER SET utf8mb4')
            with dump.open('rb') as source:
                subprocess.run(['C:/xampp/mysql/bin/mysql.exe','--no-defaults',*database_args,restored],stdin=source,env=dump_env,check=True,**HIDDEN)
            from app.database import make_engine
            restored_engine=make_engine(make_url(settings.database_url).set(database=restored).render_as_string(hide_password=False))
            try:
                with engine.connect() as a,restored_engine.connect() as b:
                    tables=[next(iter(row.values())) for row in all_rows(a,'SHOW TABLES')]
                    assert all(one(a,f'SELECT COUNT(*) n FROM `{table}`')['n']==one(b,f'SELECT COUNT(*) n FROM `{table}`')['n'] for table in tables)
                    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
                    row=one(b,'SELECT p.public_id,i.encrypted_id,i.nonce,i.auth_tag FROM student_identities i JOIN players p ON p.id=i.player_id ORDER BY i.player_id LIMIT 1')
                    assert AESGCM(settings.identity_key).decrypt(row['nonce'],row['encrypted_id']+row['auth_tag'],row['public_id'].encode()).decode()=='DUMMY-TEST-0'
                restored_app=create_app(replace(settings,database_url=make_url(settings.database_url).set(database=restored).render_as_string(hide_password=False)))
                try:
                    restored_player=TestClient(restored_app,cookies=players[0].cookies)
                    data=restored_player.get('/api/player/context').json()
                    assert data['ticket']['status']=='completed' and data['ticket']['score']==375 and len(data['notifications'])==1
                    assert restored_player.get('/api/player/leaderboard').status_code==200
                finally: restored_app.state.engine.dispose()
                result['synthetic_restore']={'all_table_counts_match':True,'tables':len(tables),'synthetic_identity_decrypts':True,'private_ticket_restored':True,'score':375,'leaderboard_available':True}
            finally: restored_engine.dispose()
        finally:
            with root.cursor() as c:c.execute(f'DROP DATABASE IF EXISTS `{test_database(restored)}`')
            root.close()
        output=ROOT/'docs/ui-review/quality-runtime.json'
        output.write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps(result,indent=2),flush=True)
    finally:
        for child in reversed(children):
            if child.poll() is None:
                child.kill();child.wait(timeout=10)
        if dump.is_file(): dump.unlink()
        app.state.engine.dispose()
        try: next(generator)
        except StopIteration: pass


if __name__=='__main__':
    serve() if '--serve' in sys.argv else main()
