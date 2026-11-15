"""Check documentation links, expected files and basic SQL model consistency."""
import importlib.util
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
docs = root / 'docs'
required = ['README.md', 'functional-specification.md', 'tech-stack.md', 'schema.md',
            'schema.sql', 'ai-system-rules.md', 'implementation-plan.md',
            'dashboard-design.md', 'research-and-decisions.md', 'graphify-setup.md',
            'verification.md']
errors = []
for name in required:
    if not (docs / name).is_file():
        errors.append(f'Missing {name}')
link_count = 0
word_count = 0
for path in docs.glob('*.md'):
    content = path.read_text(encoding='utf-8')
    word_count += len(content.split())
    if content.count('```') % 2:
        errors.append(f'Unclosed code fence: {path.name}')
    if '\ufffd' in content:
        errors.append(f'Invalid character: {path.name}')
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', content):
        if target.startswith(('http:', 'https:', '#')):
            continue
        link_count += 1
        if not (path.parent / target.split('#')[0]).exists():
            errors.append(f'Broken local link: {path.name} -> {target}')
sql = (docs / 'schema.sql').read_text(encoding='utf-8')
tables = re.findall(r'CREATE TABLE\s+(\w+)', sql, re.I)
for reference in re.findall(r'REFERENCES\s+(\w+)', sql, re.I):
    if reference not in tables:
        errors.append(f'Unknown referenced table: {reference}')
if len(tables) != len(set(tables)):
    errors.append('Duplicate SQL table name')
if importlib.util.find_spec('sqlglot'):
    import sqlglot
    statements = sqlglot.parse(sql, read='mysql', error_level='RAISE')
    print(f'MySQL-dialect parser: {len(statements)} statements parsed (not server execution)')
else:
    print('MySQL-dialect parser unavailable; schema checks are structural only')
for problem in errors:
    print('ERROR:', problem)
print(f'Documents: {len(required)}; words: {word_count}; local links: {link_count}; SQL tables: {len(tables)}')
raise SystemExit(1 if errors else 0)
