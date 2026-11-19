import hashlib
import hmac
import secrets
import re
from datetime import datetime, timezone

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from fastapi import HTTPException, Request
from pwdlib import PasswordHash

passwords = PasswordHash.recommended()
DUMMY_HASH = passwords.hash('a-dummy-password-used-only-for-timing')


def now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def digest(value):
    return hashlib.sha256(value.encode()).digest()


def csrf_for(settings, raw_session):
    return hmac.new(settings.csrf_key, raw_session.encode(), hashlib.sha256).hexdigest()


def verify_csrf(request: Request, raw_session: str):
    expected = csrf_for(request.app.state.settings, raw_session)
    supplied = request.headers.get('x-csrf-token', '')
    if not re.fullmatch(r'[0-9a-f]{64}', supplied) or not hmac.compare_digest(expected, supplied):
        raise HTTPException(403, 'Please refresh the page and try again.')


def identity_lookup(settings, student_id):
    return hmac.new(settings.lookup_key, ('institution\0' + student_id).encode(), hashlib.sha256).digest()


def encrypt_identity(settings, student_id, player_public_id):
    nonce = secrets.token_bytes(12)
    value = AESGCM(settings.identity_key).encrypt(nonce, student_id.encode(), player_public_id.encode())
    return value[:-16], nonce, value[-16:]


def set_cookie(response, settings, name, token, seconds):
    response.set_cookie(name, token, max_age=seconds, httponly=True,
                        secure=settings.cookie_secure, samesite='strict', path='/api')
