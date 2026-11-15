import json
import re
from pathlib import Path

root = Path.cwd()
out = root / 'graphify-out'
fragment = json.loads((out / '.graphify_chunk_01.json').read_text(encoding='utf-8'))
paths = (out / '.graphify_uncached.txt').read_text(encoding='utf-8').splitlines()
allowed = set(paths)
by_rel = {str(Path(p).relative_to(root)).replace('\\', '/'): p for p in paths}
nodes = [n for n in fragment['nodes'] if n['source_file'] in allowed]
ids = {n['id'] for n in nodes}
edges = [e for e in fragment['edges'] if e['source_file'] in allowed and e['source'] in ids and e['target'] in ids]
hypers = [h for h in fragment.get('hyperedges', []) if h['source_file'] in allowed and all(n in ids for n in h['nodes'])]


def ident(rel, label):
    stem = re.sub(r'[^a-z0-9_]', '_', str(Path(rel).with_suffix('')).replace('\\', '/').casefold())
    return stem + '_' + re.sub(r'[^a-z0-9_]', '_', label.casefold()).strip('_')


replacements = {}
for n in nodes:
    rel = str(Path(n['source_file']).relative_to(root)).replace('\\', '/')
    if rel == 'docs/tech-stack.md':
        if n['label'] == 'Proposed React TypeScript Vite frontend':
            old = n['id']
            n['label'] = 'Confirmed React JavaScript JSX Vite frontend'
            n['id'] = ident(rel, n['label'])
            n['rationale'] = 'User selected React JavaScript/JSX; use Vite react template, .jsx components and .js modules, with optional JSDoc.'
            replacements[old] = n['id']
        elif n['label'] == 'MySQL 8.4 InnoDB persistence proposal':
            old = n['id']
            n['label'] = 'Confirmed XAMPP MariaDB 10.11.16 persistence'
            n['id'] = ident(rel, n['label'])
            n['rationale'] = 'User selected the XAMPP MySQL service; inspected local binary is MariaDB 10.11.16. Use InnoDB and MariaDB-compatible schema behavior.'
            replacements[old] = n['id']
        line = int(n['source_location'][1:])
        if line >= 73:
            n['source_location'] = f'L{line+12}'
        if n['label'] == 'Proposed LAN deployment with verified TLS':
            n['rationale'] = 'Windows event PC uses XAMPP database and native FastAPI/Uvicorn behind HTTPS; keep MariaDB and phpMyAdmin local, with no Docker/WSL2 requirement.'
    elif rel == 'docs/README.md' and n['label'] == 'Confirmed Stack Moko Baby baseline':
        n['rationale'] = 'User confirmed final name, LED matrix/button gameplay, required private student ID, React JavaScript/JSX with Vite, and the XAMPP database service verified as MariaDB 10.11.16.'
    elif rel == 'docs/schema.md' and n['label'] == 'Candidate MySQL data model':
        n['rationale'] = 'Candidate MySQL-compatible data model targets installed XAMPP MariaDB 10.11.16 and utf8mb4_unicode_ci. Existing XAMPP databases are not modified by the documentation task.'
    elif rel == 'docs/research-and-decisions.md' and n['label'] == 'Open hardware rules TLS provider and retention decisions':
        n['source_location'] = 'L53'
    elif rel == 'docs/implementation-plan.md' and n['label'] == 'Future MySQL identity and authentication build':
        n['rationale'] = 'Future Alembic migrations and identity/authentication services must be tested on isolated MariaDB matching the installed XAMPP version.'

for e in edges:
    e['source'] = replacements.get(e['source'], e['source'])
    e['target'] = replacements.get(e['target'], e['target'])
    if e['source_file'] == by_rel['docs/tech-stack.md'] and int(e['source_location'][1:]) >= 73:
        e['source_location'] = f"L{int(e['source_location'][1:])+12}"
    elif e['source_file'] == by_rel['docs/research-and-decisions.md'] and e['source_location'] == 'L51':
        e['source_location'] = 'L53'
for h in hypers:
    h['nodes'] = [replacements.get(n, n) for n in h['nodes']]


def add_node(rel, label, line, rationale, kind='concept'):
    node = {'id': ident(rel, label), 'label': label, 'file_type': kind, 'source_file': by_rel[rel],
            'source_location': f'L{line}', 'source_url': None, 'captured_at': None,
            'author': None, 'contributor': None, 'rationale': rationale}
    nodes.append(node)
    return node['id']


def add_edge(source, target, rel, line, relation='references'):
    edges.append({'source': source, 'target': target, 'relation': relation, 'confidence': 'EXTRACTED',
                  'confidence_score': 1.0, 'source_file': by_rel[rel], 'source_location': f'L{line}', 'weight': 1.0})


lookup = {n['label']: n['id'] for n in nodes}
engine = add_node('docs/tech-stack.md', 'Verified XAMPP engine and database setup', 75,
                  'Local C:/xampp installation reports MariaDB 10.11.16. XAMPP calls it MySQL; inspected my.ini specifies port 3306. Runtime port should be reconfirmed if configuration changes.')
hosting = add_node('docs/tech-stack.md', 'Proposed native FastAPI hosting with XAMPP database', 21,
                   'Backend remains Python/FastAPI outside htdocs; Docker, WSL2 and PHP replacement are not required. Apache hosting/proxy is optional after HTTPS setup.')
js_contracts = add_node('docs/implementation-plan.md', 'JavaScript client contracts and runtime payload validation', 23,
                        'Generate a JavaScript client from OpenAPI; optional JSDoc provides editor hints and network payloads require runtime validation.')
collation = add_node('docs/schema.md', 'MariaDB compatible utf8mb4_unicode_ci schema', 159,
                     'Avoid Oracle MySQL 0900 collation and binary-JSON assumptions; validate generated columns, CHECK constraints, window functions and locking on installed MariaDB.')
db_access = add_node('docs/tech-stack.md', 'Local-only database and dedicated application account', 79,
                     'Keep MariaDB/phpMyAdmin local. Use restricted app and separate migration accounts; frontend and ESP32 access FastAPI rather than the database.')

add_edge(lookup['Proposed modular monolith architecture'], engine, 'docs/tech-stack.md', 75)
add_edge(lookup['Proposed modular monolith architecture'], hosting, 'docs/tech-stack.md', 21)
add_edge(engine, lookup['Confirmed XAMPP MariaDB 10.11.16 persistence'], 'docs/tech-stack.md', 75)
add_edge(engine, db_access, 'docs/tech-stack.md', 79)
add_edge(engine, collation, 'docs/tech-stack.md', 83)
add_edge(lookup['Candidate MySQL data model'], collation, 'docs/schema.md', 159)
add_edge(lookup['Future dependency-ordered implementation plan'], js_contracts, 'docs/implementation-plan.md', 23)
add_edge(js_contracts, lookup['Confirmed React JavaScript JSX Vite frontend'], 'docs/implementation-plan.md', 20)
add_edge(hosting, lookup['Proposed FastAPI backend'], 'docs/tech-stack.md', 80)
add_edge(lookup['Source-backed decisions and open gates'], engine, 'docs/research-and-decisions.md', 35)
add_edge(lookup['Confirmed Stack Moko Baby baseline'], lookup['Confirmed React JavaScript JSX Vite frontend'], 'docs/README.md', 25)
add_edge(lookup['Confirmed Stack Moko Baby baseline'], lookup['Confirmed XAMPP MariaDB 10.11.16 persistence'], 'docs/README.md', 26)

coverage = {p: len(Path(p).read_text(encoding='utf-8').splitlines()) for p in paths}
result = {'nodes': nodes, 'edges': edges, 'hyperedges': hypers, 'input_tokens': 0, 'output_tokens': 0, 'coverage': coverage}
node_ids = {n['id'] for n in nodes}
assert len(node_ids) == len(nodes)
assert all(e['source'] in node_ids and e['target'] in node_ids for e in edges)
assert len({(e['source'], e['target']) for e in edges}) == len(edges)
assert not any('typescript' in n['id'] or 'mysql_8_4' in n['id'] for n in nodes)
assert set(coverage) == allowed
for n in nodes:
    assert 1 <= int(n['source_location'][1:]) <= coverage[n['source_file']]
for e in edges:
    assert 1 <= int(e['source_location'][1:]) <= coverage[e['source_file']]
(out / '.graphify_chunk_01.json').write_text(json.dumps(result, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
print(json.dumps({'nodes': len(nodes), 'edges': len(edges), 'hyperedges': len(hypers), 'coverage': coverage}, indent=2))
