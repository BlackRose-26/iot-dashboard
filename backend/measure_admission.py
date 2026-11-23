"""Measure the admission stage (local gates + live model scope check) on DEVELOPMENT data.

Development regression only: it reads backend/nlp_lab/data/*-development.json, never the
holdout or evaluation sets, and does not route intents or query analytics. A supported
question counts as admitted when it passes the local gates and the model scope check;
an out-of-scope question counts as correctly held when either stage stops it.
    python measure_admission.py --output ../.tools/evaluations/admission-<name>.json
"""
import argparse
import asyncio
import json
from collections import Counter
from pathlib import Path

from app import assistant
from app.assistant import ScopePlan, model_json, normalize, scope_payload
from types import SimpleNamespace

DATA = Path(__file__).resolve().parent/'nlp_lab/data'


async def stage(settings, question):
    safe, blocked = normalize(question)
    if blocked: return blocked
    if safe['has_unrecognized_words']: return 'unrecognized_context'
    if not safe.get('requires_scope_check'): return 'admitted_local'
    reply = await model_json(settings, scope_payload(settings, safe, None), timeout=60)
    scope = ScopePlan.model_validate_json(reply['message']['content']).scope
    return 'admitted_model' if scope in ('system', 'social') else 'model_unsupported'


async def main(output):
    if output.exists(): raise ValueError('Choose a new output path; measurements are immutable.')
    # Only the local model endpoint is needed: no database, keys or private memory.
    settings = SimpleNamespace(ollama_url='http://127.0.0.1:11434', ollama_model='qwen3:4b-instruct')
    await model_json(settings, {'model': settings.ollama_model, 'messages': [{'role': 'user', 'content': 'ok'}],
                                'stream': False, 'options': {'num_ctx': 4096, 'num_predict': 1}}, timeout=180)  # warm up
    rows = [case.split('|', 3) for case in json.loads((DATA/'balanced-development.json').read_text(encoding='utf-8'))['cases']]
    ood = [q for qs in json.loads((DATA/'ood-development.json').read_text(encoding='utf-8'))['families'].values() for q in qs]
    results = []
    for family, intent, language, question in rows:
        results.append({'set': 'unsupported' if intent == 'unsupported' else 'supported', 'intent': intent,
                        'language': language, 'outcome': await stage(settings, question)})
    for question in ood:
        results.append({'set': 'out_of_scope', 'intent': 'unsupported', 'language': None,
                        'outcome': await stage(settings, question)})
    summary = {}
    for name in ('supported', 'unsupported', 'out_of_scope'):
        group = [r for r in results if r['set'] == name]
        admitted = sum(r['outcome'].startswith('admitted') for r in group)
        summary[name] = {'n': len(group), 'admitted': admitted, 'outcomes': dict(Counter(r['outcome'] for r in group))}
    report = {'kind': 'development admission regression (not held-out accuracy)',
              'scope_examples': len(getattr(assistant, 'SCOPE_EXAMPLES', [])),
              'lexicon': assistant.lexical_resource()[1], 'summary': summary, 'cases': results}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    asyncio.run(main(parser.parse_args().output))
