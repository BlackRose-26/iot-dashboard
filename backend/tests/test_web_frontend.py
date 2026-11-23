from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app.web_frontend import mount_frontend


def test_production_spa_preserves_api_and_private_file_boundaries(tmp_path):
    (tmp_path/'assets').mkdir()
    (tmp_path/'index.html').write_text('<html>Stack Moko Baby</html>')
    (tmp_path/'assets'/'app.js').write_text('/* build */')
    (tmp_path/'.private').write_text('must not be served')
    app=FastAPI()
    mount_frontend(app,tmp_path)
    with TestClient(app) as client:
        assert client.get('/admin/login').text=='<html>Stack Moko Baby</html>'
        assert client.get('/queue').status_code==200
        assert client.get('/assets/app.js').status_code==200
        assert client.get('/api/missing').status_code==404
        assert client.post('/api/missing',json={}).status_code==405
        assert client.get('/.private').status_code==404
        assert 'must not' not in client.get('/%2eprivate').text


def test_missing_production_build_fails_at_startup(tmp_path):
    with pytest.raises(RuntimeError): mount_frontend(FastAPI(),tmp_path)
