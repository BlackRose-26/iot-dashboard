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

    @classmethod
    def load(cls):
        load_dotenv(BACKEND / '.env')
        def key(name):
            value = os.environ.get(name)
            if not value:
                raise RuntimeError('Run the local backend setup before starting the API.')
            result = base64.urlsafe_b64decode(value)
            if len(result) != 32:
                raise RuntimeError('Invalid backend key configuration.')
            return result
        return cls(
            database_url=os.environ['STACK_DATABASE_URL'],
            identity_key=key('STACK_IDENTITY_KEY'),
            lookup_key=key('STACK_LOOKUP_KEY'),
            csrf_key=key('STACK_CSRF_KEY'),
            device_token=os.environ['STACK_DEVICE_TOKEN'],
            public_url=os.getenv('STACK_PUBLIC_URL', 'http://127.0.0.1:5173').rstrip('/'),
            cookie_secure=os.getenv('STACK_COOKIE_SECURE', 'false').lower() == 'true',
            simulator_enabled=os.getenv('STACK_SIMULATOR_ENABLED', 'true').lower() == 'true',
            development=os.getenv('STACK_ENV', 'development') == 'development',
            allowed_origins=tuple(value.strip() for value in os.getenv('STACK_ALLOWED_ORIGINS', '').split(',') if value.strip()),
        )
