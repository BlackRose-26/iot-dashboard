"""Explicit Render pre-deploy initialization; never logs passwords or identities.

Use only the dedicated cloud database account, which owns its own schema.
Do not use this to import local event data or replace encryption keys.
"""
import os
import time
import pymysql

from app.config import Settings
from app.database import make_engine, execute, one
from setup_local import migrate, seed


def main():
    settings=Settings.load()
    from sqlalchemy.engine import make_url
    url=make_url(settings.database_url)
    if url.database!='stack_moko_baby':
        raise RuntimeError('Server setup requires the dedicated project database.')
    connection=None
    for attempt in range(20):
        try:
            connection=pymysql.connect(host=url.host,port=url.port or 3306,user=url.username,password=url.password,
                                      database=url.database,autocommit=True,connect_timeout=5)
            break
        except pymysql.OperationalError:
            if attempt==19: raise RuntimeError('The private database is not ready; check the Render database service and credentials.') from None
            time.sleep(3)
    with connection:
        migrate(connection,url.database)
    engine=make_engine(settings.database_url)
    with engine.connect() as c:
        empty=not one(c,'SELECT id FROM staff_users LIMIT 1')
    if empty:
        password=os.getenv('STACK_INITIAL_ADMIN_PASSWORD','')
        if len(password)<16: raise RuntimeError('Set a private initial admin password of at least 16 characters.')
        seed(engine,settings,password)
    with engine.begin() as c:
        execute(c,"UPDATE events SET settings=JSON_SET(settings,'$.active_ruleset','matrix-v1') WHERE code='acs-day'")
    engine.dispose()
    print('Server migrations/configuration ready. Existing credentials and results preserved.')


if __name__=='__main__': main()
