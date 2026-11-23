"""Independent-review collection. Empty slots are never counted as test cases."""
from collections import Counter
import json
from pathlib import Path
import re

from nlp_lab.data import TOPICS
from app.assistant_training import TrainingTarget


def collection(path):
    path.parent.mkdir(parents=True,exist_ok=True)
    payload={'status':'collection_pending','required_filled_cases':325,
             'instructions':'Supply new public/synthetic questions only. No real identifiers, private records or credentials. An independent reviewer must approve labels before freezing/evaluation. Empty slots are not a dataset.',
             'entries':[{'id':f'fresh-{topic}-{i+1:02d}','quota_topic':topic,'question':'',
                         'target':None,'previous':None,'language':None,'family':'',
                         'author_code':'','reviewer_code':'','privacy_checked':False,'review_status':'pending'}
                        for topic in TOPICS for i in range(25)]}
    with path.open('x',encoding='utf-8') as stream: json.dump(payload,stream,indent=2)
    return {'filled':0,'required':325,'status':payload['status']}


def validate(packet):
    entries=packet['entries']
    if len(entries)!=325 or any(not row['question'].strip() for row in entries):
        raise ValueError('325 filled questions are required; blank collection slots are not cases.')
    if len({row['id'] for row in entries})!=len(entries): raise ValueError('Duplicate case IDs.')
    if any(not row['author_code'] or not row['reviewer_code'] or row['author_code']==row['reviewer_code'] or
           not row['privacy_checked'] or row['review_status']!='approved' or not row['family'] for row in entries):
        raise ValueError('Independent authorship/review attestation, family and privacy approval are required.')
    counts=Counter()
    for row in entries:
        if re.search(r'\d{4,}|[\w.+-]+@[\w.-]+|https?://|-----BEGIN',row['question'],re.I):
            raise ValueError('Use public/synthetic wording without private-looking values or URLs.')
        target=TrainingTarget.model_validate(row['target'])
        counts[target.topic]+=1
        if row['language'] not in ('en','taglish'): raise ValueError('Language annotation required.')
    if any(not 20<=counts[t]<=50 for t in TOPICS): raise ValueError('Each primary intent needs 20–50 reviewed cases.')
    return counts
