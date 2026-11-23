import base64
import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

BACKEND = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Settings:
    database_url: str = field(repr=False)
    identity_key: bytes = field(repr=False)
    lookup_key: bytes = field(repr=False)
    csrf_key: bytes = field(repr=False)
    device_token: str = field(repr=False)
    public_url: str = 'http://127.0.0.1:5173'
    cookie_secure: bool = False
    simulator_enabled: bool = True
    development: bool = True
    allowed_origins: tuple[str, ...] = ()
    ai_enabled: bool = True
    ollama_url: str = 'http://127.0.0.1:11434'
    ollama_model: str = 'qwen3:4b-instruct'

    @classmethod
    def load(cls):
        load_dotenv(BACKEND / '.env')
        public_url=os.getenv('STACK_PUBLIC_URL') or os.getenv('RENDER_EXTERNAL_URL') or 'http://127.0.0.1:5173'
        database_url=os.getenv('STACK_DATABASE_URL')
        if not database_url:
            from sqlalchemy.engine import URL
            database_url=URL.create('mysql+pymysql',username='stack_moko_app',
                password=os.environ['STACK_DB_PASSWORD'],host=os.environ['STACK_DB_HOST'],
                port=3306,database='stack_moko_baby',query={'charset':'utf8mb4'}).render_as_string(hide_password=False)
        if os.getenv('STACK_ENV','development') != 'development':
            from urllib.parse import urlsplit
            public=urlsplit(public_url)
            if (public.scheme!='https' or not public.hostname or public.username or public.password
                    or public.path not in ('','/') or public.query or public.fragment
                    or os.getenv('STACK_COOKIE_SECURE','false').lower()!='true'):
                raise RuntimeError('Production needs an HTTPS public origin and secure cookies.')
        def key(name):
            value = os.environ.get(name)
            if not value:
                raise RuntimeError('Run the local backend setup before starting the API.')
            result = base64.urlsafe_b64decode(value)
            if len(result) != 32:
                raise RuntimeError('Invalid backend key configuration.')
            return result
        return cls(
            database_url=database_url,
            identity_key=key('STACK_IDENTITY_KEY'),
            lookup_key=key('STACK_LOOKUP_KEY'),
            csrf_key=key('STACK_CSRF_KEY'),
            device_token=os.environ['STACK_DEVICE_TOKEN'],
            public_url=public_url.rstrip('/'),
            cookie_secure=os.getenv('STACK_COOKIE_SECURE', 'false').lower() == 'true',
            simulator_enabled=os.getenv('STACK_SIMULATOR_ENABLED', 'true').lower() == 'true',
            development=os.getenv('STACK_ENV', 'development') == 'development',
            allowed_origins=tuple(value.strip() for value in os.getenv('STACK_ALLOWED_ORIGINS', '').split(',') if value.strip()),
            ai_enabled=os.getenv('STACK_AI_ENABLED', 'true').lower() == 'true',
            ollama_url=os.getenv('STACK_OLLAMA_URL', 'http://127.0.0.1:11434'),
            ollama_model=os.getenv('STACK_OLLAMA_MODEL', 'qwen3:4b-instruct'),
        )
