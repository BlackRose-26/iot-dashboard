"""Optional same-origin production SPA; API misses must stay API errors."""
from pathlib import Path

from fastapi import HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


def mount_frontend(app, directory):
    root = Path(directory).resolve()
    if not (root / 'index.html').is_file():
        raise RuntimeError('Build the React frontend before starting this deployment.')
    app.mount('/assets', StaticFiles(directory=root/'assets'), name='assets')

    @app.get('/{path:path}', include_in_schema=False)
    def frontend(path: str):
        if path == 'api' or path.startswith('api/') or any(part.startswith('.') for part in Path(path).parts):
            raise HTTPException(404, 'Not found.')
        file = (root/path).resolve()
        if not file.is_relative_to(root): raise HTTPException(404, 'Not found.')
        return FileResponse(file if file.is_file() else root/'index.html')
