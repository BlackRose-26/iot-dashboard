"""Relocate a generated map from staging to the requested project root."""
import json
import sys
from pathlib import Path

source = Path(sys.argv[1]).resolve()
destination = Path(sys.argv[2]).resolve()
out = destination / 'graphify-out'
out.mkdir(exist_ok=True)


def replace(text):
    return text.replace(str(source), str(destination)).replace(source.as_posix(), destination.as_posix())


def walk(value):
    if isinstance(value, str):
        return replace(value)
    if isinstance(value, list):
        return [walk(v) for v in value]
    if isinstance(value, dict):
        return {replace(k): walk(v) for k, v in value.items()}
    return value


for path in (source / 'graphify-out').rglob('*'):
    if not path.is_file() or path.suffix in {'.log', '.pid'}:
        continue
    target = out / path.relative_to(source / 'graphify-out')
    target.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == '.json':
        target.write_text(json.dumps(walk(json.loads(path.read_text(encoding='utf-8'))), ensure_ascii=False, indent=2), encoding='utf-8')
    else:
        target.write_text(replace(path.read_text(encoding='utf-8')), encoding='utf-8')
(out / '.graphify_root').write_text(str(destination), encoding='utf-8')
(out / '.graphify_python').write_text(str(destination / '.tools/graphify-venv/Scripts/python.exe'), encoding='utf-8')
print('Project map relocated with destination source references.')
