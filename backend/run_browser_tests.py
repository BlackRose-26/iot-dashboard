"""Run real browser flows against a disposable XAMPP database and dedicated ports."""
import os
import secrets
import subprocess
import sys
import time
import base64
from dataclasses import replace
from pathlib import Path
import pymysql
import httpx
from sqlalchemy.engine import URL
from app.config import Settings
from app.database import make_engine
from setup_local import migrate, seed

ROOT=Path(__file__).resolve().parents[1]
runtime=Path(r'C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1112-737-0_26.1112.737.0_x64__3k8sg7r9htsxt/dependencies')
database='stack_moko_test_'+secrets.token_hex(5)
password='Disposable-browser-test-password'
root=pymysql.connect(host='127.0.0.1',user='root',password=os.getenv('STACK_DB_ROOT_PASSWORD',''),autocommit=True)
children=[]
try:
    migrate(root,database)
    url=URL.create('mysql+pymysql',username='root',password=os.getenv('STACK_DB_ROOT_PASSWORD',''),host='127.0.0.1',database=database).render_as_string(hide_password=False)
    settings=Settings(database_url=url,identity_key=secrets.token_bytes(32),lookup_key=secrets.token_bytes(32),csrf_key=secrets.token_bytes(32),device_token='disposable-browser-device-token',public_url='http://127.0.0.1:5174')
    engine=make_engine(url);seed(engine,settings,password);engine.dispose()
    env=dict(os.environ,STACK_DATABASE_URL=url,STACK_PUBLIC_URL=settings.public_url,STACK_API_TARGET='http://127.0.0.1:8001',STACK_TEST_URL=settings.public_url,STACK_TEST_PASSWORD=password)
    env.update({f'STACK_{name}_KEY':base64.urlsafe_b64encode(value).decode() for name,value in [('IDENTITY',settings.identity_key),('LOOKUP',settings.lookup_key),('CSRF',settings.csrf_key)]})
    env['STACK_DEVICE_TOKEN']=settings.device_token
    env.pop('STACK_SKIP_DEFAULT_APP',None)
    children.append(subprocess.Popen([sys.executable,'-m','uvicorn','app.main:app','--host','127.0.0.1','--port','8001','--no-access-log'],cwd=ROOT/'backend',env=env,stdout=subprocess.DEVNULL))
    node=runtime/'node/bin/node.exe'
    children.append(subprocess.Popen([str(node),'node_modules/vite/bin/vite.js','--host','127.0.0.1','--port','5174','--strictPort'],cwd=ROOT/'frontend',env=env,stdout=subprocess.DEVNULL))
    for _ in range(60):
        try:
            if httpx.get(settings.public_url+'/api/health').status_code==200: break
        except httpx.HTTPError: pass
        time.sleep(.5)
    else: raise RuntimeError('Dedicated test servers did not start')
    result=subprocess.run([str(node),'node_modules/@playwright/test/cli.js','test',*sys.argv[1:]],cwd=ROOT/'frontend',env=env)
finally:
    for child in reversed(children):
        child.terminate()
        try: child.wait(timeout=10)
        except subprocess.TimeoutExpired: child.kill()
    assert database.startswith('stack_moko_test_') and len(database)==26
    with root.cursor() as c:c.execute(f'DROP DATABASE `{database}`')
    root.close()
sys.exit(result.returncode)
