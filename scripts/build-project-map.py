"""Local documentation map helper using the installed Graphify library.

prepare: detect/extract structural inputs and list uncached semantic documents.
finish: validate the assistant-produced fragment and generate Graphify outputs.
No model provider or private database is contacted.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'graphify-out'
SPEC = ROOT / '.codex/skills/graphify/references/extraction-spec.md'


def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def prepare():
    from graphify.detect import detect
    from graphify.extract import extract
    from graphify.cache import check_semantic_cache
    from graphify.watch import _read_build_excludes, _read_build_gitignore
    OUT.mkdir(exist_ok=True)
    (OUT / '.graphify_root').write_text(str(ROOT), encoding='utf-8')
    (OUT / '.graphify_python').write_text(sys.executable, encoding='utf-8')
    detection = detect(ROOT, extra_excludes=_read_build_excludes(OUT), gitignore=_read_build_gitignore(OUT))
    write('.graphify_detect.json', detection)
    code_files = [Path(p) for p in detection.get('files', {}).get('code', [])]
    ast = extract(code_files, cache_root=ROOT, root=ROOT) if code_files else {'nodes': [], 'edges': []}
    write('.graphify_ast.json', ast)
    docs = [p for cat in ('document', 'paper', 'image') for p in detection.get('files', {}).get(cat, [])]
    nodes, edges, hypers, uncached = check_semantic_cache(docs, root=str(ROOT), prompt_file=str(SPEC))
    write('.graphify_cached.json', {'nodes': nodes, 'edges': edges, 'hyperedges': hypers})
    (OUT / '.graphify_uncached.txt').write_text('\n'.join(uncached), encoding='utf-8')
    print(json.dumps({'files': detection.get('total_files'), 'words': detection.get('total_words'),
                      'code': len(code_files), 'semantic_files': len(docs),
                      'uncached': uncached, 'skipped_sensitive': detection.get('skipped_sensitive', [])}, indent=2))


def finish():
    from graphify.build import build_from_json
    from graphify.cluster import cluster, score_all
    from graphify.analyze import god_nodes, surprising_connections, suggest_questions
    from graphify.report import generate
    from graphify.export import to_json
    from graphify.cache import save_semantic_cache
    from graphify.detect import save_manifest
    from graphify.diagnostics import diagnose_extraction, format_diagnostic_report
    from graphify.cli import _stamped_manifest_files
    def read(name):
        return json.loads((OUT / name).read_text(encoding='utf-8'))
    chunk = read('.graphify_chunk_01.json')
    assert isinstance(chunk.get('nodes'), list) and isinstance(chunk.get('edges'), list)
    uncached = (OUT / '.graphify_uncached.txt').read_text(encoding='utf-8').splitlines()
    for path in uncached:
        actual = len(Path(path).read_text(encoding='utf-8').splitlines())
        assert chunk.get('coverage', {}).get(path) == actual, f'Incomplete coverage: {path}'
    for item in chunk['nodes'] + chunk['edges'] + chunk.get('hyperedges', []):
        item['_origin'] = 'semantic'
    save_semantic_cache(chunk['nodes'], chunk['edges'], chunk.get('hyperedges', []),
                        root=str(ROOT), allowed_source_files=uncached, prompt_file=str(SPEC))
    cached = read('.graphify_cached.json')
    ast = read('.graphify_ast.json')
    seen = set()
    merged_nodes = []
    for node in ast['nodes'] + cached['nodes'] + chunk['nodes']:
        if node['id'] not in seen:
            seen.add(node['id'])
            merged_nodes.append(node)
    extraction = {'nodes': merged_nodes,
                  'edges': ast['edges'] + cached['edges'] + chunk['edges'],
                  'hyperedges': cached.get('hyperedges', []) + chunk.get('hyperedges', []),
                  'input_tokens': 0, 'output_tokens': 0}
    # Host-agent usage is not exposed by the delegation tool; zero means unreported,
    # not a claim that semantic extraction used no tokens. See verification.md.
    write('.graphify_extract.json', extraction)
    detection = read('.graphify_detect.json')
    graph = build_from_json(extraction, root=str(ROOT), directed=True)
    assert graph.number_of_nodes() > 0, 'Empty extraction'
    communities = cluster(graph)
    cohesion = score_all(graph, communities)
    labels = {}
    for cid, members in communities.items():
        candidates = sorted(members, key=lambda n: graph.degree(n), reverse=True)
        labels[cid] = ' / '.join(str(graph.nodes[n].get('label', n)) for n in candidates[:2])[:100]
    questions = suggest_questions(graph, communities, labels)
    wrote = to_json(graph, communities, str(OUT / 'graph.json'), community_labels=labels,
                    force=('--allow-renames' in sys.argv))
    assert wrote is not False, 'Graph shrink guard refused write'
    report = generate(graph, communities, cohesion, labels, god_nodes(graph),
                      surprising_connections(graph, communities), detection,
                      {'input': 0, 'output': 0}, str(ROOT), suggested_questions=questions)
    report += '\n\nSemantic extraction was performed by the host assistant. Exact token usage was not exposed; zero counters mean unreported, not zero-cost. This map covers documentation and implemented local frontend/backend sources. Graph relationships do not prove live hardware state; physical ESP32 integration remains unverified.\n'
    (OUT / 'GRAPH_REPORT.md').write_text(report, encoding='utf-8')
    write('.graphify_labels.json', {str(k): v for k, v in labels.items()})
    summary = diagnose_extraction(extraction, directed=True, root=str(ROOT))
    print(format_diagnostic_report(summary))
    corpus = detection.get('files', {})
    stamped = _stamped_manifest_files(corpus, extraction, ROOT)
    save_manifest(stamped, root=str(ROOT), scan_corpus={p for group in corpus.values() for p in group})
    write('build-summary.json', {'nodes': graph.number_of_nodes(), 'edges': graph.number_of_edges(),
                               'communities': len(communities), 'health': summary,
                               'semantic_usage': 'not exposed by host tool'})
    print(json.dumps({'nodes': graph.number_of_nodes(), 'edges': graph.number_of_edges(),
                      'communities': len(communities)}, indent=2))


if __name__ == '__main__':
    {'prepare': prepare, 'finish': finish}[sys.argv[1]]()
