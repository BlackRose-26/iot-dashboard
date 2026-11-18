from datetime import timedelta
from contextlib import asynccontextmanager
import asyncio
from time import monotonic
import hashlib
import hmac
import json
import re
import secrets
import uuid
from urllib.parse import urlsplit
from typing import Literal

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from .config import Settings
from .assistant import Assistant, Question, basic_response, REQUEST_SECONDS
from .analytics import collect, Period, Source
from .assistant_training import TrainingStore, Proposal, Review
from .origins import origin_allowed
from .database import make_engine, one, all_rows, execute
from .game import RULES, RULES_HASH, canonical, replay, simulated_result
from .security import passwords, DUMMY_HASH, now, digest, csrf_for, verify_csrf, identity_lookup, encrypt_identity, set_cookie


def create_app(settings=None):
    settings = settings or Settings.load()
    engine = make_engine(settings.database_url)
    assistant = Assistant(settings, engine)
    training = TrainingStore(engine)
    @asynccontextmanager
    async def lifespan(_app):
        try: yield
        finally: await assistant.close()
    app = FastAPI(title='Stack Moko Baby', docs_url=None, redoc_url=None, openapi_url=None,lifespan=lifespan)
    app.state.engine = engine
    app.state.settings = settings

    @app.exception_handler(IntegrityError)
    async def conflicting_write(request, exc):
        return JSONResponse({'detail':'This record changed. Refresh and try again.'}, status_code=409)

    @app.exception_handler(SQLAlchemyError)
    async def database_unavailable(request, exc):
        # Do not expose SQL parameters, identity material or connection credentials.
        return JSONResponse({'detail':'The event database is unavailable. Please try again shortly.'}, status_code=503)

    @app.exception_handler(RequestValidationError)
    async def invalid_input(request, exc):
        # Never reflect a student's submitted ID (including malformed input) in errors.
        return JSONResponse({'detail':'Check the submitted fields.'}, status_code=422)

    @app.middleware('http')
    async def boundaries(request, call_next):
        if request.method not in ('GET','HEAD','OPTIONS'):
            origin = request.headers.get('origin')
            if origin and not origin_allowed(request, origin, settings):
                return JSONResponse({'detail':'This request origin is not allowed.'}, status_code=403)
        response = await call_next(request)
        response.headers['Cache-Control'] = 'no-store'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'no-referrer'
        return response

    def subject(c, request, kind, write=False, required=True):
        raw = request.cookies.get('sm_admin' if kind=='admin' else 'sm_player', '')
        row = one(c, '''SELECT a.*,s.username,s.enabled AS staff_enabled FROM auth_sessions a
          LEFT JOIN staff_users s ON s.id=a.staff_user_id WHERE a.token_hash=:hash
          AND a.expires_at>:now AND a.revoked_at IS NULL''', hash=digest(raw), now=now()) if raw else None
        valid = row and (row['staff_user_id'] and row['staff_enabled'] if kind=='admin' else row['player_id'])
        if not valid:
            if required: raise HTTPException(401, 'Please sign in.' if kind=='admin' else 'Scan the cabinet QR code to join.')
            return None
        if write: verify_csrf(request, raw)
        return dict(row, csrf=csrf_for(settings, raw))

    def session(c, response, kind, player_id=None, staff_id=None):
        raw=secrets.token_urlsafe(40)
        execute(c, '''INSERT INTO auth_sessions(token_hash,csrf_token_hash,player_id,staff_user_id,expires_at)
          VALUES(:hash,:csrf,:player,:staff,:expires)''', hash=digest(raw), csrf=digest(csrf_for(settings,raw)), player=player_id, staff=staff_id, expires=now()+timedelta(hours=12 if kind=='admin' else 24))
        set_cookie(response, settings, 'sm_admin' if kind=='admin' else 'sm_player', raw, 43200 if kind=='admin' else 86400)
        return csrf_for(settings,raw)

    def event_lock(c):
        return one(c, "SELECT * FROM events WHERE code='acs-day' FOR UPDATE")

    def machine(c, lock=False):
        return one(c, "SELECT * FROM machines WHERE code='cabinet-01'"+(' FOR UPDATE' if lock else ''))

    def active(c):
        return one(c, '''SELECT g.*,p.nickname,p.public_code FROM game_sessions g JOIN players p ON p.id=g.player_id
          WHERE g.active_machine_id=1 LIMIT 1''')

    def machine_state(m,g):
        health=json.loads(m['health'] or '{}')
        fresh=m['last_seen_at'] and (now()-m['last_seen_at']).total_seconds()<15
        if health.get('source')=='simulator' and settings.simulator_enabled:
            fresh=True
        if not fresh: return 'offline'
        return {'reserved':'reserved','countdown':'reserved','playing':'playing','awaiting_result':'pending','review':'pending'}.get(g['status'] if g else '', 'ready' if m['observed_state']=='ready' else 'offline')

    def rounds(c, source=None):
        rows=all_rows(c, '''SELECT g.*,p.nickname,p.public_code FROM game_sessions g JOIN players p ON p.id=g.player_id
          WHERE g.status='completed' AND g.invalidated_at IS NULL AND (:source IS NULL OR g.result_source=:source)
          ORDER BY g.completed_at DESC,g.id DESC''', source=source)
        proofs={}
        for p in all_rows(c, '''SELECT p.* FROM placements p JOIN game_sessions g ON g.id=p.session_id
          WHERE g.status='completed' AND g.invalidated_at IS NULL AND (:source IS NULL OR g.result_source=:source)
          ORDER BY p.session_id,p.sequence_no''',source=source):
            proofs.setdefault(p['session_id'],[]).append(p)
        result=[]
        for r in rows:
            placements=proofs.get(r['id'],[])
            result.append({'id':r['public_id'],'code':r['public_code'],'nickname':r['nickname'], 'won':r['outcome']=='win',
              'reason':{'target_reached':'Target reached','zero_overlap':'No overlap','timeout':'Time expired'}[r['end_reason']],
              'score':r['score'],'level':r['highest_level'],'perfect':r['perfect_rows'], 'overlap':r['overlap_total'],
              'totalWidth':r['attempted_width_total'],'accuracy':round(100*r['overlap_total']/r['attempted_width_total'],1) if r['attempted_width_total'] else 0,
              'duration':round(r['duration_ms']/1000,2),'hour':(r['completed_at'].hour+8)%24,
              'completedAt':r['completed_at'].isoformat()+'Z','source':r['result_source'],
              'placements':[{'level':p['level_no'],'overlap':p['overlap_width'],'width':p['candidate_width']} for p in placements]})
        return result

    def player_context(c, request):
        p=subject(c,request,'player',required=False)
        raw=request.cookies.get('sm_entry','')
        grant=one(c, '''SELECT e.*,q.enabled FROM entry_grants e JOIN qr_links q ON q.id=e.qr_link_id
          WHERE e.token_hash=:hash AND e.expires_at>:now''',hash=digest(raw),now=now()) if raw else None
        event=one(c,"SELECT status FROM events WHERE code='acs-day'")
        result={'canRegister':bool(grant and grant['enabled'] and not grant['used_at']), 'admissionsOpen':event['status']=='open',
          'csrf':p['csrf'] if p else csrf_for(settings,raw) if grant else '', 'ticket':None, 'notifications':[]}
        if not p: return result
        cabinet_state=machine_state(machine(c),active(c))
        result['cabinetState']=cabinet_state
        result['queueState']=('paused' if event['status']!='open' else
          'offline' if cabinet_state=='offline' else
          'awaiting_operator' if cabinet_state=='ready' else 'busy')
        q=one(c, '''SELECT q.*,p.nickname,p.public_code,g.public_id AS session_uuid,g.status AS game_status,g.outcome,g.score,g.highest_level,g.result_source
          FROM queue_entries q JOIN players p ON p.id=q.player_id LEFT JOIN game_sessions g ON g.queue_entry_id=q.id
          WHERE q.player_id=:player ORDER BY q.id DESC LIMIT 1''',player=p['player_id'])
        if q:
            position=one(c,"SELECT COUNT(*) AS n FROM queue_entries WHERE event_id=:event AND status='waiting' AND (joined_at<:joined OR (joined_at=:joined AND id<=:id))",event=q['event_id'],joined=q['joined_at'],id=q['id'])['n'] if q['status']=='waiting' else None
            status= 'completed' if q['game_status']=='completed' else 'playing' if q['game_status']=='playing' else 'called' if q['status']=='assigned' else q['status']
            result['ticket']={'id':q['public_id'],'nickname':q['nickname'],'code':q['public_code'],'status':status,'position':position,
              'sessionId':q['session_uuid'],'outcome':q['outcome'],'score':q['score'],'level':q['highest_level'],'source':q['result_source']}
        result['notifications']=[{'id':r['public_id'],'outcome':r['outcome'],'score':r['score']} for r in all_rows(c,'''SELECT n.public_id,g.outcome,g.score FROM player_notifications n JOIN game_sessions g ON g.id=n.session_id WHERE n.player_id=:player ORDER BY n.id DESC LIMIT 5''',player=p['player_id'])]
        return result

    def audit(c,staff,action,entity=None,reason=None):
        execute(c,'''INSERT INTO audit_logs(event_id,staff_user_id,action,entity_type,entity_public_id,reason,details_safe,request_id)
          VALUES(1,:staff,:action,'queue',:entity,:reason,'{}',:request)''',staff=staff,action=action,entity=entity,reason=reason,request=str(uuid.uuid4()))

    @app.get('/api/health')
    def health():
        with engine.connect() as c: one(c,'SELECT 1 AS ok')
        return {'status':'ok','application':'stack-moko-baby','database':'XAMPP MariaDB'}

    @app.post('/api/admin/login')
    def login(body:Login, request:Request,response:Response):
        key=digest((request.client.host if request.client else '')+'\0'+body.username.lower())
        with engine.begin() as c:
            execute(c, 'INSERT IGNORE INTO login_attempts(key_hash,attempts,window_start) VALUES(:key,0,:now)',key=key,now=now())
            a=one(c,'SELECT * FROM login_attempts WHERE key_hash=:key FOR UPDATE',key=key)
            count=a['attempts'] if (now()-a['window_start']).total_seconds()<900 else 0
            if count>=8: return JSONResponse({'detail':'Too many attempts. Try again in 15 minutes.'},status_code=429)
            user=one(c,'SELECT * FROM staff_users WHERE username=:name',name=body.username)
            try: valid=passwords.verify(body.password,user['password_hash'] if user else DUMMY_HASH)
            except Exception: valid=False
            if not valid or not user or not user['enabled']:
                execute(c,'UPDATE login_attempts SET attempts=:count,window_start=:start WHERE key_hash=:key',key=key,count=count+1,start=a['window_start'] if count else now())
                return JSONResponse({'detail':'Username or password is incorrect.'},status_code=401)
            execute(c,'DELETE FROM login_attempts WHERE key_hash=:key',key=key)
            old=request.cookies.get('sm_admin')
            if old: execute(c,'UPDATE auth_sessions SET revoked_at=:now WHERE token_hash=:hash',now=now(),hash=digest(old))
            return {'username':user['username'],'csrf':session(c,response,'admin',staff_id=user['id'])}

    @app.get('/api/admin/session')
    def admin_session(request:Request):
        with engine.connect() as c:
            p=subject(c,request,'admin')
            return {'username':p['username'],'csrf':p['csrf']}

    @app.post('/api/admin/logout')
    def logout(request:Request,response:Response):
        with engine.begin() as c:
            p=subject(c,request,'admin',write=True)
            execute(c,'UPDATE auth_sessions SET revoked_at=:now WHERE id=:id',now=now(),id=p['id'])
        response.delete_cookie('sm_admin',path='/api')
        return {'ok':True}

    @app.get('/api/admin/snapshot')
    def snapshot(request:Request):
        with engine.connect() as c:
            subject(c,request,'admin')
            m=machine(c);g=active(c)
            event=one(c,"SELECT * FROM events WHERE code='acs-day'")
            qr=one(c,'SELECT token FROM qr_links WHERE enabled=1 AND machine_id=:id LIMIT 1',id=m['id'])
            queue=all_rows(c,"SELECT q.public_id,p.nickname,p.public_code,q.joined_at FROM queue_entries q JOIN players p ON p.id=q.player_id WHERE q.event_id=1 AND q.status='waiting' ORDER BY q.joined_at,q.id")
            return {'queue':[{'id':q['public_id'],'nickname':q['nickname'],'code':q['public_code'],'joinedAt':q['joined_at'].isoformat()+'Z'} for q in queue],
              'admissionsOpen':event['status']=='open','machineState':machine_state(m,g),'machine':{'lastSeen':m['last_seen_at'].isoformat()+'Z' if m['last_seen_at'] else None,'health':json.loads(m['health'] or '{}'),'firmware':m['firmware_version']},
              'currentPlayer':{'nickname':g['nickname'],'code':g['public_code'],'sessionId':g['public_id'],'source':g['result_source']} if g else None,
              'rounds':rounds(c),'qrPath':'/join/'+qr['token'] if qr else None,'simulatorEnabled':settings.simulator_enabled}

    def assistant_staff(request,write=False):
        with engine.connect() as c:
            return subject(c,request,'admin',write=write)['staff_user_id']

    @app.get('/api/admin/assistant/status')
    async def assistant_status(request:Request):
        await run_in_threadpool(assistant_staff,request)
        return await assistant.status()

    @app.get('/api/admin/analytics')
    def analytics(request:Request,period:Period='event_to_date',source:Source='simulator'):
        with engine.connect() as c: subject(c,request,'admin')
        return collect(engine,period,source,simulator_enabled=settings.simulator_enabled)

    @app.post('/api/admin/assistant/prepare')
    async def assistant_prepare(request:Request):
        await asyncio.to_thread(assistant_staff,request,True)
        return await assistant.prepare()

    @app.get('/api/admin/assistant/memory')
    async def assistant_memory(request:Request):
        staff_id=await asyncio.to_thread(assistant_staff,request)
        return await assistant.memory_view(staff_id)

    @app.delete('/api/admin/assistant/memory')
    async def assistant_forget_memory(request:Request):
        staff_id=await asyncio.to_thread(assistant_staff,request,True)
        return await assistant.forget_memory(staff_id)

    @app.get('/api/admin/assistant/training/options')
    def assistant_training_options(request:Request):
        assistant_staff(request)
        return training.options()

    @app.get('/api/admin/assistant/training')
    def assistant_training_list(request:Request,before:int|None=None):
        staff_id=assistant_staff(request)
        return training.list(staff_id,before)

    @app.post('/api/admin/assistant/training')
    def assistant_training_propose(body:Proposal,request:Request):
        staff_id=assistant_staff(request,True)
        return training.propose(staff_id,body)

    @app.patch('/api/admin/assistant/training/{example_id}')
    def assistant_training_review(example_id:uuid.UUID,body:Review,request:Request):
        staff_id=assistant_staff(request,True)
        return training.review(staff_id,str(example_id),body)

    @app.delete('/api/admin/assistant/training/{example_id}')
    def assistant_training_remove(example_id:uuid.UUID,request:Request):
        staff_id=assistant_staff(request,True)
        return training.remove(staff_id,str(example_id))

    @app.post('/api/admin/assistant/training/export')
    def assistant_training_export(request:Request):
        staff_id=assistant_staff(request,True)
        return training.export(staff_id)

    @app.post('/api/admin/assistant/query')
    async def assistant_query(body:Question,request:Request):
        async def within_deadline():
            staff_id=None
            started=monotonic()
            try:
                async with asyncio.timeout(REQUEST_SECONDS):
                    staff_id=await asyncio.to_thread(assistant_staff,request,True)
                    return await assistant.ask(body,staff_id,started=started)
            except asyncio.TimeoutError:
                if staff_id is None:
                    raise HTTPException(503,'Sign-in verification took too long. Please retry shortly.')
                result=basic_response(body,'unavailable','The assistant request reached its time limit. Please retry shortly. Ordinary dashboard functions remain available.','timeout')
                assistant.enqueue_audit(staff_id,result,'timeout',{},int((monotonic()-started)*1000))
                return result
        async def disconnected():
            while not await request.is_disconnected(): await asyncio.sleep(0.25)
        answer=asyncio.create_task(within_deadline())
        disconnect=asyncio.create_task(disconnected())
        try:
            done,_=await asyncio.wait([answer,disconnect],return_when=asyncio.FIRST_COMPLETED)
            if answer in done: return await answer
            return Response(status_code=499)
        finally:
            for task in (answer,disconnect):
                if not task.done(): task.cancel()
            await asyncio.gather(answer,disconnect,return_exceptions=True)

    @app.post('/api/player/entry')
    def entry(body:Entry,request:Request,response:Response):
        try:
            scanned=urlsplit(body.qrContent.strip())
            scanned_origin=f'{scanned.scheme.lower()}://{scanned.netloc.lower()}'
            match=re.fullmatch(r'/join/([A-Za-z0-9_-]{43})',scanned.path)
            if scanned.scheme not in ('http','https') or not origin_allowed(request, scanned_origin, settings) or scanned.username or scanned.password or scanned.query or scanned.fragment or not match:
                raise ValueError()
            token=match.group(1)
        except ValueError:
            raise HTTPException(422,'Scan a Stack Moko Baby QR code for this event website.')
        with engine.begin() as c:
            event_lock(c)
            qr=one(c,'SELECT * FROM qr_links WHERE token=:token AND enabled=1',token=token)
            if not qr: raise HTTPException(404,'This QR code is no longer active. Ask the operator for the current code.')
            raw=secrets.token_urlsafe(40)
            execute(c,'INSERT INTO entry_grants(token_hash,qr_link_id,expires_at) VALUES(:hash,:qr,:expires)',hash=digest(raw),qr=qr['id'],expires=now()+timedelta(hours=2))
            set_cookie(response,settings,'sm_entry',raw,7200)
        return {'ok':True}

    @app.get('/api/player/context')
    def context(request:Request):
        with engine.connect() as c: return player_context(c,request)

    @app.post('/api/player/register')
    def register(body:Registration,request:Request,response:Response):
        nickname=body.nickname.strip();student=body.studentId.strip()
        if not re.fullmatch(r'[\w .\-]{2,24}',nickname) or not re.fullmatch(r'[A-Za-z0-9\-]{4,32}',student) or not body.acknowledged:
            raise HTTPException(422,'Enter a valid nickname and student ID, and acknowledge the privacy notice.')
        with engine.begin() as c:
            event=event_lock(c)
            raw=request.cookies.get('sm_entry','')
            grant=one(c,'''SELECT e.*,q.enabled FROM entry_grants e JOIN qr_links q ON q.id=e.qr_link_id WHERE e.token_hash=:hash AND e.expires_at>:now FOR UPDATE''',hash=digest(raw),now=now())
            if not grant or not grant['enabled']: raise HTTPException(403,'Scan the cabinet QR code first.')
            player=subject(c,request,'player',required=False)
            verify_csrf(request,request.cookies.get('sm_player') if player else raw)
            if grant['used_at']:
                if not player or player['player_id']!=grant['player_id']: raise HTTPException(409,'This entry has already been used. Scan the QR again.')
                return {'ok':True}
            if event['status']!='open': raise HTTPException(409,'Admissions are paused. Please check with the operator.')
            identity=one(c,"SELECT player_id FROM student_identities WHERE institution_code='institution' AND lookup_key_version=1 AND id_lookup=:hash",hash=identity_lookup(settings,student))
            if identity and (not player or player['player_id']!=identity['player_id']):
                raise HTTPException(409,'We could not create a new ticket. Use your existing ticket or ask the operator for help.')
            if identity:
                pid=identity['player_id']
                if one(c,"SELECT id FROM queue_entries WHERE player_id=:id AND status IN ('waiting','assigned')",id=pid):
                    raise HTTPException(409,'Your ticket is already active. Open your queue ticket.')
                execute(c,'UPDATE players SET nickname=:name WHERE id=:id',name=nickname,id=pid)
            else:
                public=str(uuid.uuid4())
                pid=execute(c,"INSERT INTO players(public_id,public_code,nickname,notice_version,notice_ack_at) VALUES(:id,:code,:name,'2026-11-v1',:now)",id=public,code='SMB-'+secrets.token_hex(8).upper(),name=nickname,now=now()).lastrowid
                encrypted,nonce,tag=encrypt_identity(settings,student,public)
                execute(c,"INSERT INTO student_identities(player_id,institution_code,id_lookup,lookup_key_version,encrypted_id,nonce,auth_tag,encryption_key_version,purge_after) VALUES(:id,'institution',:hash,1,:encrypted,:nonce,:tag,1,:purge)",id=pid,hash=identity_lookup(settings,student),encrypted=encrypted,nonce=nonce,tag=tag,purge=event['ends_at']+timedelta(days=30))
            execute(c,"INSERT INTO queue_entries(public_id,event_id,player_id) VALUES(:uuid,1,:id)",uuid=str(uuid.uuid4()),id=pid)
            execute(c,'UPDATE entry_grants SET used_at=:now,player_id=:id WHERE id=:grant',now=now(),id=pid,grant=grant['id'])
            session(c,response,'player',player_id=pid)
        return {'ok':True}

    @app.post('/api/player/cancel')
    def cancel(request:Request):
        with engine.begin() as c:
            event_lock(c);p=subject(c,request,'player',write=True)
            execute(c,"UPDATE queue_entries SET status='cancelled',closed_at=:now,revision=revision+1 WHERE player_id=:id AND status='waiting'",now=now(),id=p['player_id'])
        return {'ok':True}

    @app.get('/api/player/leaderboard')
    def leaderboard(request:Request):
        with engine.connect() as c:
            p=subject(c,request,'player')
            completed=one(c,"SELECT g.result_source,g.status FROM queue_entries q LEFT JOIN game_sessions g ON g.queue_entry_id=q.id WHERE q.player_id=:id ORDER BY q.id DESC LIMIT 1",id=p['player_id'])
            if not completed or completed['status']!='completed': raise HTTPException(403,'Finish your game to unlock the leaderboard.')
            return {'rounds':rounds(c,completed['result_source']),'source':completed['result_source']}

    @app.post('/api/admin/admissions')
    def admissions(body:Admissions,request:Request):
        with engine.begin() as c:
            p=subject(c,request,'admin',write=True);event_lock(c)
            execute(c,'UPDATE events SET status=:status,revision=revision+1 WHERE id=1',status='open' if body.open else 'paused')
            audit(c,p['staff_user_id'],'admissions_open' if body.open else 'admissions_paused')
        return {'ok':True}

    @app.post('/api/admin/queue/{ticket}/skip')
    def skip(ticket:str,body:Reason,request:Request):
        with engine.begin() as c:
            p=subject(c,request,'admin',write=True);event_lock(c)
            changed=execute(c,"UPDATE queue_entries SET status='cancelled',closed_at=:now,revision=revision+1 WHERE public_id=:id AND status='waiting'",now=now(),id=ticket).rowcount
            if not changed: raise HTTPException(409,'This ticket is no longer waiting.')
            audit(c,p['staff_user_id'],'queue_skipped',ticket,body.reason.strip())
        return {'ok':True}

    @app.post('/api/admin/queue/call-next')
    def call_next(request:Request):
        with engine.begin() as c:
            p=subject(c,request,'admin',write=True);event=event_lock(c);m=machine(c,True)
            key=request.headers.get('Idempotency-Key','')
            if not re.fullmatch(r'[a-f0-9-]{36}',key): raise HTTPException(422,'A request key is required.')
            receipt=one(c,"SELECT response_safe FROM request_receipts WHERE actor_scope=:actor AND operation='call-next' AND idempotency_key=:key",actor='staff:'+str(p['staff_user_id']),key=key)
            if receipt: return json.loads(receipt['response_safe'])
            if event['status']!='open' or machine_state(m,active(c))!='ready': raise HTTPException(409,'The cabinet must be ready and admissions open.')
            q=one(c,"SELECT * FROM queue_entries WHERE event_id=1 AND status='waiting' ORDER BY joined_at,id LIMIT 1 FOR UPDATE")
            if not q: raise HTTPException(409,'No players are waiting.')
            source='simulator' if json.loads(m['health'] or '{}').get('source')=='simulator' else 'device'
            public=str(uuid.uuid4())
            sid=execute(c,"INSERT INTO game_sessions(public_id,event_id,machine_id,queue_entry_id,player_id,ruleset_id,ready_deadline_at,result_source) VALUES(:uuid,1,1,:queue,:player,1,:deadline,:source)",uuid=public,queue=q['id'],player=q['player_id'],deadline=now()+timedelta(minutes=3),source=source).lastrowid
            execute(c,"UPDATE queue_entries SET status='assigned',revision=revision+1 WHERE id=:id",id=q['id'])
            execute(c,"INSERT INTO device_commands(public_id,machine_id,session_id,command_type,expected_revision,payload,issued_by,expires_at) VALUES(:uuid,1,:sid,'reserve',1,:payload,:staff,:expires)",uuid=str(uuid.uuid4()),sid=sid,payload=json.dumps({'sessionId':public,'rules':RULES,'rulesHash':RULES_HASH.hex(),'source':source}),staff=p['staff_user_id'],expires=now()+timedelta(minutes=3))
            result={'sessionId':public}
            execute(c,"INSERT INTO request_receipts(actor_scope,operation,idempotency_key,request_hash,response_status,response_safe) VALUES(:actor,'call-next',:key,:hash,200,:response)",actor='staff:'+str(p['staff_user_id']),key=key,hash=digest('call-next'),response=json.dumps(result))
            audit(c,p['staff_user_id'],'player_called',public)
        return result

    def device(c,request):
        raw=request.headers.get('X-Device-Token','')
        m=machine(c,True)
        if not raw or not hmac.compare_digest(digest(raw),m['device_token_hash']): raise HTTPException(401,'Device authentication required.')
        return m

    def start(c,public,source):
        g=one(c,'SELECT * FROM game_sessions WHERE public_id=:id FOR UPDATE',id=public)
        if not g or g['result_source']!=source: raise HTTPException(409,'This round does not belong to this source.')
        if g['status']=='playing': return {'ok':True}
        if g['status']!='reserved' or g['ready_deadline_at']<now(): raise HTTPException(409,'This reservation is not ready to start. Ask the operator.')
        execute(c,"UPDATE game_sessions SET status='playing',started_at=:now,revision=revision+1 WHERE id=:id",now=now(),id=g['id'])
        execute(c,"UPDATE device_commands SET status='applied',applied_at=:now WHERE session_id=:id AND command_type='reserve'",now=now(),id=g['id'])
        return {'ok':True}

    def finish(c,public,body,source):
        g=one(c,'SELECT * FROM game_sessions WHERE public_id=:id FOR UPDATE',id=public)
        if not g or g['result_source']!=source: raise HTTPException(409,'This round does not belong to this source.')
        payload=body.model_dump(mode='json') if isinstance(body,BaseModel) else body
        hashed=hashlib.sha256(canonical(payload).encode()).digest()
        if g['status']=='completed':
            if g['terminal_id']==payload['terminalId'] and hmac.compare_digest(g['result_hash'],hashed): return {'ok':True,'score':g['score']}
            raise HTTPException(409,'A different terminal result was already recorded.')
        if g['status']!='playing': raise HTTPException(409,'Start this round before submitting a result.')
        if payload['rulesHash']!=RULES_HASH.hex(): raise HTTPException(422,'Ruleset mismatch.')
        try: result=replay(payload['placements'],payload['durationMs'],payload['outcome'])
        except (ValueError,KeyError,TypeError): raise HTTPException(422,'The placement trace is not valid for this ruleset.')
        if source=='device' and (now()-g['started_at']).total_seconds()*1000+2000<payload['durationMs']: raise HTTPException(422,'Result timing is not valid.')
        for seq,p in enumerate(result['placements'],1):
            execute(c,'''INSERT INTO placements(session_id,sequence_no,level_no,candidate_x,candidate_width,support_x,support_width,overlap_width,locked_at_ms)
              VALUES(:id,:seq,:level,:x,:width,:sx,:sw,:overlap,:locked)''',id=g['id'],seq=seq,level=p['level'],x=p['x'],width=p['width'],sx=p['support_x'],sw=p['support_width'],overlap=p['overlap'],locked=p['locked'])
        execute(c,'''UPDATE game_sessions SET status='completed',completed_at=:now,received_at=:now,terminal_id=:terminal,result_hash=:hash,
          outcome=:outcome,end_reason=:reason,duration_ms=:duration,score=:score,highest_level=:level,perfect_rows=:perfect,
          overlap_total=:retained,attempted_width_total=:attempted,revision=revision+1 WHERE id=:id''',now=now(),terminal=payload['terminalId'],hash=hashed,outcome=payload['outcome'],reason=result['reason'],duration=payload['durationMs'],score=result['score'],level=result['level'],perfect=result['perfect'],retained=result['retained'],attempted=result['attempted'],id=g['id'])
        execute(c,"UPDATE queue_entries SET status='served',closed_at=:now,revision=revision+1 WHERE id=:id",now=now(),id=g['queue_entry_id'])
        execute(c,"UPDATE machines SET observed_state='ready',last_seen_at=:now WHERE id=1",now=now())
        execute(c,'INSERT INTO player_notifications(public_id,player_id,session_id) VALUES(:uuid,:player,:session)',uuid=str(uuid.uuid4()),player=g['player_id'],session=g['id'])
        execute(c,"INSERT INTO outbox_events(public_id,event_id,event_revision,event_type,entity_public_id,payload_safe) VALUES(:uuid,1,:revision,'round.completed',:entity,:payload)",uuid=str(uuid.uuid4()),revision=g['revision']+1,entity=public,payload=json.dumps({'sessionId':public,'outcome':payload['outcome'],'score':result['score'],'source':source}))
        return {'ok':True,'score':result['score']}

    @app.post('/api/admin/simulator/{action}')
    def simulator(action:str,request:Request):
        if not settings.simulator_enabled: raise HTTPException(404,'Simulator disabled.')
        with engine.begin() as c:
            p=subject(c,request,'admin',write=True);event_lock(c);machine(c,True);g=active(c)
            if action=='ready':
                if g: raise HTTPException(409,'Finish or release the active round first.')
                execute(c,"UPDATE machines SET observed_state='ready',last_seen_at=:now,health=:health WHERE id=1",now=now(),health='{"source":"simulator"}')
                result={'ok':True}
            elif action=='start' and g: result=start(c,g['public_id'],'simulator')
            elif action in ('win','loss') and g: result=finish(c,g['public_id'],simulated_result(action),'simulator')
            elif action=='release' and g and g['result_source']=='simulator':
                execute(c,"UPDATE game_sessions SET status='aborted',end_reason='operator_abort',revision=revision+1 WHERE id=:id",id=g['id'])
                execute(c,"UPDATE queue_entries SET status='cancelled',closed_at=:now,revision=revision+1 WHERE id=:id",now=now(),id=g['queue_entry_id'])
                execute(c,"UPDATE device_commands SET status='expired' WHERE session_id=:id AND status='pending'",id=g['id'])
                result={'ok':True}
            else: raise HTTPException(409,'This action is not available for the current round.')
            audit(c,p['staff_user_id'],'simulator_'+action,g['public_id'] if g else None)
        return result

    @app.post('/api/device/heartbeat')
    def heartbeat(body:Heartbeat,request:Request):
        with engine.begin() as c:
            event_lock(c);device(c,request)
            execute(c,'UPDATE machines SET observed_state=:state,last_seen_at=:now,firmware_version=:firmware,health=:health WHERE id=1',state=body.state,now=now(),firmware=body.firmware,health=json.dumps({'source':'device','rssi':body.rssi}))
            g=active(c)
            return {'activeSession':g['public_id'] if g and g['result_source']=='device' else None,'rules':RULES,'rulesHash':RULES_HASH.hex()}

    @app.post('/api/device/sessions/{public}/start')
    def device_start(public:str,request:Request):
        with engine.begin() as c:
            event_lock(c);device(c,request)
            return start(c,public,'device')

    @app.post('/api/device/sessions/{public}/result')
    def device_result(public:str,body:Result,request:Request):
        with engine.begin() as c:
            event_lock(c);device(c,request)
            return finish(c,public,body,'device')

    return app


class Login(BaseModel):
    username:str=Field(min_length=1,max_length=80)
    password:str=Field(min_length=1,max_length=200)
class Entry(BaseModel):
    model_config={'extra':'forbid'}
    qrContent:str=Field(min_length=20,max_length=1024)
    method:Literal['camera','upload']
class Registration(BaseModel):
    nickname:str=Field(min_length=2,max_length=24)
    studentId:str=Field(min_length=4,max_length=32)
    acknowledged:bool
class Admissions(BaseModel):
    open:bool
class Reason(BaseModel):
    reason:str=Field(min_length=1,max_length=160,pattern=r'.*\S.*')
class Heartbeat(BaseModel):
    state:str=Field(pattern=r'^(ready|playing|offline)$')
    firmware:str=Field(max_length=64)
    rssi:int|None=Field(default=None,ge=-120,le=0)
class Placement(BaseModel):
    candidate_x:int=Field(strict=True,ge=0,le=7)
    candidate_width:int=Field(strict=True,ge=1,le=3)
    overlap_width:int=Field(strict=True,ge=0,le=3)
    locked_at_ms:int=Field(strict=True,ge=30,lt=60000)
class Result(BaseModel):
    model_config={'extra':'forbid'}
    terminalId:str=Field(pattern=r'^[a-f0-9-]{36}$')
    rulesHash:str=Field(pattern=r'^[a-f0-9]{64}$')
    outcome:str=Field(pattern=r'^(win|loss)$')
    durationMs:int=Field(strict=True,ge=0,le=60000)
    placements:list[Placement]=Field(max_length=12)


app=create_app() if __name__!='__main__' and __import__('os').getenv('STACK_SKIP_DEFAULT_APP')!='1' else None
