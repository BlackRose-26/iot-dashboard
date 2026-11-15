"""Shared origin policy for browser writes and normalized QR entry URLs."""
from urllib.parse import urlsplit


def canonical_origin(value):
    try:
        parsed = urlsplit(value)
        if (parsed.scheme not in ('http', 'https') or not parsed.hostname
                or parsed.username or parsed.password or parsed.query or parsed.fragment
                or parsed.path not in ('', '/')):
            return None
        host = parsed.hostname.lower()
        if host in ('localhost', '127.0.0.1', '::1'):
            host = 'localhost'
        port = parsed.port
        return (parsed.scheme, host, port if port is not None else (443 if parsed.scheme == 'https' else 80))
    except (TypeError, ValueError):
        return None


def origin_allowed(request, value, settings):
    origin = canonical_origin(value)
    if origin is None:
        return False
    candidates = [settings.public_url, *settings.allowed_origins,
                  f'{request.url.scheme}://{request.headers.get("host", "")}']
    if settings.development:
        candidates.extend(('http://localhost:5173', 'http://localhost:4173'))
    return origin in {canonical_origin(candidate) for candidate in candidates}
