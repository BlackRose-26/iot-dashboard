"""Bound API JSON bodies before parsing, including chunked requests."""
from fastapi import HTTPException
from starlette.responses import JSONResponse


class RequestSizeLimit:
    def __init__(self, app, max_bytes=65536):
        self.app, self.max_bytes = app, max_bytes

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)
        lengths = [value for key,value in scope['headers'] if key.lower() == b'content-length']
        if lengths and (len(lengths) != 1 or len(lengths[0])>20 or not lengths[0].isdigit()):
            return await JSONResponse({'detail':'Invalid request length.'},status_code=400)(scope,receive,send)
        if lengths and int(lengths[0]) > self.max_bytes:
            return await JSONResponse({'detail':'Request body is too large.'},status_code=413)(scope,receive,send)
        size = 0
        async def bounded_receive():
            nonlocal size
            message = await receive()
            if message['type'] == 'http.request':
                size += len(message.get('body',b''))
                if size > self.max_bytes:
                    raise HTTPException(413,'Request body is too large.')
            return message
        await self.app(scope,bounded_receive,send)
