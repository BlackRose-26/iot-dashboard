import base64

import pytest

from app.config import Settings


def cloud_env(monkeypatch):
    monkeypatch.setattr('app.config.load_dotenv',lambda *args,**kwargs:None)
    for name in ('STACK_DATABASE_URL','STACK_PUBLIC_URL'): monkeypatch.delenv(name,raising=False)
    monkeypatch.setenv('STACK_DB_HOST','private-db.example.internal')
    monkeypatch.setenv('STACK_DB_PASSWORD','synthetic-test-only')
    monkeypatch.setenv('STACK_DEVICE_TOKEN','synthetic-test-only-device-token')
    monkeypatch.setenv('STACK_ENV','production')
    monkeypatch.setenv('STACK_COOKIE_SECURE','true')
    monkeypatch.setenv('STACK_SIMULATOR_ENABLED','false')
    monkeypatch.setenv('STACK_AI_ENABLED','false')
    monkeypatch.setenv('RENDER_EXTERNAL_URL','https://synthetic-test.onrender.com')
    for name in ('IDENTITY','LOOKUP','CSRF'):
        monkeypatch.setenv(f'STACK_{name}_KEY',base64.urlsafe_b64encode(bytes(32)).decode())


def test_cloud_origin_and_private_database_without_xampp_paths(monkeypatch):
    cloud_env(monkeypatch)
    settings=Settings.load()
    assert settings.public_url=='https://synthetic-test.onrender.com'
    assert 'private-db.example.internal' in settings.database_url
    assert settings.cookie_secure and not settings.simulator_enabled and not settings.ai_enabled


@pytest.mark.parametrize('origin',['http://public.example','https://user:secret@public.example','https://public.example/path'])
def test_production_rejects_insecure_or_non_origin_public_urls(monkeypatch,origin):
    cloud_env(monkeypatch)
    monkeypatch.setenv('STACK_PUBLIC_URL',origin)
    with pytest.raises(RuntimeError): Settings.load()


def test_production_rejects_insecure_cookies(monkeypatch):
    cloud_env(monkeypatch)
    monkeypatch.setenv('STACK_COOKIE_SECURE','false')
    with pytest.raises(RuntimeError): Settings.load()
