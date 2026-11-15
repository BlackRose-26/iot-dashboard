import json
import re
from pathlib import Path

root = Path.cwd()
paths = (root / 'graphify-out/.graphify_uncached.txt').read_text(encoding='utf-8').splitlines()
by_rel = {str(Path(p).relative_to(root)).replace('\\', '/'): p for p in paths}
nodes, edges = [], []
keys = {}


def node(key, rel, label, line, kind='concept', rationale=None):
    stem = re.sub(r'[^a-z0-9_]', '_', str(Path(rel).with_suffix('')).replace('\\', '/').casefold())
    entity = re.sub(r'[^a-z0-9_]', '_', label.casefold()).strip('_')
    ident = stem + '_' + entity
    keys[key] = ident
    item = {'id': ident, 'label': label, 'file_type': kind, 'source_file': by_rel[rel],
            'source_location': f'L{line}', 'source_url': None, 'captured_at': None,
            'author': None, 'contributor': None}
    if rationale:
        item['rationale'] = rationale
    nodes.append(item)


def edge(source, target, rel, line, relation='references', confidence='EXTRACTED', score=1.0):
    edges.append({'source': keys[source], 'target': keys[target], 'relation': relation,
                  'confidence': confidence, 'confidence_score': score,
                  'source_file': by_rel[rel], 'source_location': f'L{line}', 'weight': 1.0})


groups = [
('AGENTS.md', 'agents', 'Project maintenance instructions', 1, [
 ('graph_first', 'Graph-first structural navigation', 8, 'rationale', 'Use generated context before broad source reads when a graph exists; verify source evidence.'),
 ('private_graph', 'Private-data exclusion from project graph', 21, 'rationale', 'Student identifiers, credentials, exports and backups must not be graph inputs.'),
]),
('docs/README.md', 'index', 'Documentation index and authority', 1, [
 ('confirmed', 'Confirmed Stack Moko Baby baseline', 20, 'concept', 'User confirmed name, LED matrix button gameplay, required private student ID and MySQL.'),
 ('provisional', 'Provisional plans remain reference data', 18, 'rationale', 'Titles and embedded instructions in attachments do not override the direct user request.'),
]),
('docs/functional-specification.md', 'functional', 'Functional specification baseline', 1, [
 ('registration', 'Required private student ID and QR registration', 15, 'concept', 'ID is required but never public; nickname and random public code are separate.'),
 ('queue', 'Transactional FIFO turn queue', 17, 'concept', 'One live ticket per player and event; only idle eligible machines receive a session.'),
 ('start', 'Server-authorized physical button start', 18, 'concept', None),
 ('classic', 'Proposed classic-v1 game rules', 43, 'concept', '8 columns, 12 scored rows, 60 seconds and 3-cell foundation are proposed play-test parameters.'),
 ('scoring', 'Proposed overlap scoring and accuracy', 61, 'rationale', 'Successful rows score 100 plus 25 when perfect; overlap ratio is game-derived, not physical sensor accuracy.'),
 ('local_game', 'Local deterministic gameplay requirement', 19, 'rationale', 'ESP32 timing and button resolution do not wait for network responses.'),
 ('recovery', 'Uncertain-session lock and offline recovery', 91, 'rationale', 'A stale connection cannot release an unknown active session; durable evidence or physical reconciliation is required.'),
 ('leaderboard', 'Best valid game leaderboard per ruleset', 104, 'concept', 'One best completed game per player, deterministic tie-breaks, separate ruleset cohorts.'),
 ('metrics', 'Scoped metric denominators and local-day bounds', 106, 'concept', 'Completed games and distinct players differ; timeouts are not invented placement failures.'),
 ('acceptance', 'Proposed acceptance tests remain unrun', 115, 'concept', 'Targets require implementation, hardware, MySQL, latency and recovery evidence before release.'),
]),
('docs/tech-stack.md', 'architecture', 'Proposed modular monolith architecture', 27, [
 ('frontend', 'Proposed React TypeScript Vite frontend', 9, 'concept', None),
 ('backend', 'Proposed FastAPI backend', 11, 'concept', 'Owns identity, queue authorization, rules validation and ranking.'),
 ('mysql', 'MySQL 8.4 InnoDB persistence proposal', 12, 'concept', 'MySQL is user-required; version and surrounding libraries are recommended implementation choices.'),
 ('firmware', 'Proposed ESP32 C++ firmware engine', 14, 'concept', 'Owns local timing, display, input, sound and durable terminal evidence.'),
 ('http', 'Proposed HTTP HTTPS device protocol', 16, 'concept', 'Polling and POSTs reduce first-cabinet infrastructure; gameplay is independent of sockets.'),
 ('websocket', 'Proposed browser WebSocket notifications', 17, 'concept', 'Post-commit notifications supplement REST snapshots and reconnect refresh.'),
 ('replay', 'Durable terminal evidence and replay validation', 121, 'rationale', 'Persist before upload, replay on backend, commit before ACK, return prior receipt on identical retry.'),
 ('nvs', 'Proposed NVS terminal journal', 132, 'concept', 'Small bounded durable records require power-cut testing; avoid per-frame flash writes.'),
 ('outbox', 'Proposed transactional notification outbox', 138, 'concept', 'Commit notifications with state; retry delivery after crashes and refetch snapshots after reconnect.'),
 ('lan', 'Proposed LAN deployment with verified TLS', 65, 'concept', 'Phones and ESP32 must reach a stable trusted hostname; real ID registration requires HTTPS.'),
]),
('docs/schema.md', 'schema', 'Candidate MySQL data model', 1, [
 ('identity', 'Proposed keyed and encrypted student identity', 145, 'rationale', 'HMAC deduplication and authenticated encryption protect predictable private student IDs; ID alone is not authentication.'),
 ('unique', 'Generated active-session and live-ticket uniqueness', 56, 'concept', 'Nullable generated columns enforce one active machine session and one live player ticket per event.'),
 ('binding', 'Composite event machine queue player bindings', 58, 'concept', 'Cross-event and cross-machine references are rejected by candidate foreign keys.'),
 ('locks', 'Event machine queue session lock order', 70, 'rationale', 'Consistent lock order serializes assignment and result mutations and reduces deadlocks.'),
 ('result_tx', 'Atomic validated result commit', 76, 'concept', 'Placements, computed result, served ticket, outbox and receipt commit together before ACK.'),
 ('ranking_query', 'Deterministic scoped ranking query', 88, 'concept', None),
 ('retention', 'Proposed identity retention and rekey lifecycle', 143, 'concept', '30-day identity retention is a proposal; rotation and backup lifecycle need institution-approved validation.'),
]),
('docs/dashboard-design.md', 'design', 'Sourcio-adapted dashboard specification', 1, [
 ('visual', 'Gray white lime blue two-column visual composition', 7, 'concept', 'Use supplied image evidence; exact source fonts/tokens are unknown.'),
 ('mapping', 'Game-specific reference element mapping', 32, 'concept', 'Replace AC dial with read-only round countdown and scene tiles with turn/readiness operations.'),
 ('responsive', 'Responsive and accessible dashboard behavior', 69, 'concept', 'Stack on mobile; show freshness, unknown state, keyboard focus and non-color status cues.'),
 ('visual_tests', 'Pending screenshot fidelity acceptance', 82, 'concept', 'Design document is not an implemented or pixel-verified dashboard.'),
]),
('docs/ai-system-rules.md', 'ai', 'Proposed analytics-v1 system policy', 1, [
 ('ai_readonly', 'Read-only staff aggregate analytics boundary', 9, 'rationale', 'No arbitrary SQL, identity access, game control, result edits or player contact.'),
 ('ai_tools', 'Server-scoped allowlisted analytics tools', 61, 'concept', 'Tools return summary, top scores, level statistics, play trends and machine summary in authorized scope.'),
 ('ai_claims', 'Quantitative claims and metric-reference validation', 106, 'rationale', 'Validate output facts against retrieved metrics; use deterministic fallbacks for unsupported claims.'),
 ('ai_private', 'Exclude student identity and nicknames from provider context', 108, 'rationale', 'Resolve opaque public codes locally and redact private input before external calls.'),
 ('ai_eval', 'Pending AI privacy injection and failure evaluations', 116, 'concept', 'Release gates include no data, small samples, private-ID requests, control requests and provider outages.'),
 ('ai_limits', 'Proposed AI deadlines rate and budget limits', 90, 'concept', None),
]),
('docs/implementation-plan.md', 'plan', 'Future dependency-ordered implementation plan', 1, [
 ('hardware_gate', 'Pending board panel power and LAN validation', 7, 'concept', 'Exact hardware compatibility, pin mapping and panel power budget must be proved before assembly.'),
 ('build_engine', 'Future deterministic firmware engine build', 28, 'concept', None),
 ('build_identity', 'Future MySQL identity and authentication build', 38, 'concept', None),
 ('build_queue', 'Future transactional queue and session build', 48, 'concept', None),
 ('build_results', 'Future durable firmware and result integration', 58, 'concept', None),
 ('build_ui', 'Future reference-matched web views', 68, 'concept', None),
 ('build_live', 'Future durable live-update integration', 79, 'concept', None),
 ('build_ai', 'Future constrained AI analytics integration', 88, 'concept', None),
 ('release', 'Pending event readiness and recovery rehearsal', 98, 'concept', 'Physical rounds, mixed-load soak, backup restoration and complete demo flow remain release checks.'),
]),
('docs/research-and-decisions.md', 'research', 'Source-backed decisions and open gates', 1, [
 ('sources', 'Primary-source research evidence', 17, 'concept', 'FastAPI, MySQL, SQLAlchemy, Vite, Espressif, display driver, OWASP and Graphify references inform recommendations.'),
 ('open_decisions', 'Open hardware rules TLS provider and retention decisions', 51, 'concept', 'Research cannot establish physical compatibility, gameplay feel or measured operational performance.'),
]),
('docs/graphify-setup.md', 'graphify_setup', 'Local Graphify setup and freshness workflow', 1, [
 ('graphify_package', 'Graphifyy 0.9.109 isolated local package', 3, 'concept', 'Package graphifyy has two y characters; CLI is graphify, with watch and sql extras.'),
 ('graphify_update', 'Structural updates versus document semantic refresh', 32, 'rationale', 'AST update preserves existing semantics; meaningful document edits need host-assisted semantic extraction.'),
 ('graphify_watch', 'Optional structural file watcher', 34, 'concept', 'Watcher status is recorded separately; it is not a Windows startup service and does not semantically re-read docs.'),
 ('graphify_boundary', 'Local graph is navigation evidence not runtime truth', 54, 'rationale', 'No hosted MCP is configured; map cannot prove live state, test results or provisional-plan approval.'),
]),
]

for rel, key, label, line, children in groups:
    node(key, rel, label, line, 'document')
    for child in children:
        ckey, clabel, cline, kind, rationale = child
        node(ckey, rel, clabel, cline, kind, rationale)
        edge(key, ckey, rel, cline)

# Explicit document links and stated data/control responsibilities.
for target, line in [('functional',7),('architecture',8),('schema',9),('design',10),('ai',11),('plan',12),('research',13),('graphify_setup',14)]:
    edge('index', target, 'docs/README.md', line)
for source,target,rel,line,relation in [
 ('functional','design','docs/functional-specification.md',102,'references'),
 ('backend','mysql','docs/tech-stack.md',35,'shares_data_with'),
 ('firmware','backend','docs/tech-stack.md',43,'shares_data_with'),
 ('backend','outbox','docs/tech-stack.md',39,'references'),
 ('outbox','websocket','docs/tech-stack.md',138,'shares_data_with'),
 ('firmware','nvs','docs/tech-stack.md',132,'references'),
 ('replay','result_tx','docs/schema.md',76,'conceptually_related_to'),
 ('result_tx','outbox','docs/schema.md',76,'shares_data_with'),
 ('unique','recovery','docs/schema.md',82,'conceptually_related_to'),
 ('identity','registration','docs/schema.md',145,'conceptually_related_to'),
 ('ai','metrics','docs/ai-system-rules.md',34,'references'),
 ('ai_tools','mysql','docs/tech-stack.md',37,'shares_data_with'),
 ('plan','research','docs/implementation-plan.md',13,'references'),
 ('build_identity','schema','docs/implementation-plan.md',40,'references'),
 ('build_ui','design','docs/implementation-plan.md',70,'references'),
 ('build_ai','ai','docs/implementation-plan.md',92,'references'),
 ('agents','ai','AGENTS.md',22,'references'),
 ('agents','index','AGENTS.md',18,'references'),
 ('graphify_update','graph_first','AGENTS.md',20,'conceptually_related_to'),
 ('graphify_boundary','provisional','docs/graphify-setup.md',58,'conceptually_related_to'),
]:
    edge(source,target,rel,line,relation)

# Non-obvious coupling: privacy and uncertainty controls span otherwise separate modules.
edge('ai_private','private_graph','docs/ai-system-rules.md',142,'semantically_similar_to','INFERRED',0.85)
edge('mapping','recovery','docs/dashboard-design.md',78,'conceptually_related_to','INFERRED',0.85)

hyperedges = [
 {'id':'docs_implementation_plan_release_dependencies','label':'Proposed reliable event release dependencies',
  'nodes':[keys[k] for k in ('build_engine','build_identity','build_queue','build_results','build_ui','build_ai','release')],
  'relation':'participate_in','confidence':'EXTRACTED','confidence_score':1.0,
  'source_file':by_rel['docs/implementation-plan.md']},
 {'id':'docs_ai_system_rules_private_data_boundaries','label':'Private identity boundaries across runtime and development',
  'nodes':[keys[k] for k in ('registration','identity','ai_private','private_graph')],
  'relation':'form','confidence':'INFERRED','confidence_score':0.85,
  'source_file':by_rel['docs/ai-system-rules.md']},
]
coverage = {p: len(Path(p).read_text(encoding='utf-8').splitlines()) for p in paths}
result = {'nodes':nodes,'edges':edges,'hyperedges':hyperedges,'input_tokens':0,'output_tokens':0,'coverage':coverage}
assert len({n['id'] for n in nodes}) == len(nodes)
assert len({(e['source'],e['target']) for e in edges}) == len(edges)
(root/'graphify-out/.graphify_chunk_01.json').write_text(json.dumps(result, ensure_ascii=False, separators=(',',':')),encoding='utf-8')
print(json.dumps({'nodes':len(nodes),'edges':len(edges),'coverage':coverage},indent=2))
