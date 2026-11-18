"""Fetch public reference corpora locally. Never loads or uploads application data."""
import hashlib
import json
from pathlib import Path
import tarfile

import httpx

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / '.tools' / 'nlp-datasets'


def fetch(client, url, path, limit=45_000_000):
    digest, size = hashlib.sha256(), 0
    partial = path.with_suffix(path.suffix+'.part')
    with client.stream('GET',url) as response, partial.open('wb') as output:
        response.raise_for_status()
        for part in response.iter_bytes():
            size += len(part)
            if size>limit: raise ValueError('Public dataset exceeds the download limit.')
            output.write(part)
            digest.update(part)
    partial.replace(path)
    return {'url':url,'sha256':digest.hexdigest(),'bytes':size}


def main():
    DEST.mkdir(parents=True,exist_ok=True)
    manifest = {'purpose':'Public reference/evaluation corpora, never runtime facts or automatic training.', 'sources':[]}
    with httpx.Client(timeout=60,follow_redirects=True,trust_env=False) as client:
        commit_response=client.get('https://api.github.com/repos/clinc/oos-eval/commits/master')
        commit_response.raise_for_status()
        commit=commit_response.json()['sha']
        if len(commit)!=40 or any(c not in '0123456789abcdef' for c in commit): raise ValueError('Invalid upstream revision.')
        base='https://raw.githubusercontent.com/clinc/oos-eval/'+commit
        source=fetch(client,base+'/data/data_full.json',DEST/'clinc150-full.json',5_000_000)
        source.update(name='CLINC150',revision=commit,license='CC-BY-3.0',role='Out-of-domain evaluation only; game-specific relabelling requires review.')
        source['license_file']=fetch(client,base+'/LICENSE',DEST/'CLINC150-LICENSE.txt',100_000)
        data=json.loads((DEST/'clinc150-full.json').read_text())
        counts={key:len(rows) for key,rows in data.items()}
        source['partitions']=counts
        # Keep upstream labels/splits intact; do not mistake its banking/travel intents for game intents.
        manifest['sources'].append(source)
        source=fetch(client,'https://amazon-massive-nlu-dataset.s3.amazonaws.com/amazon-massive-dataset-1.1.tar.gz',DEST/'massive-1.1.tar.gz')
        source.update(name='MASSIVE 1.1',license='CC-BY-4.0',role='English/Tagalog language reference; not a Taglish or game-domain gold set.')
        counts={}
        with tarfile.open(DEST/'massive-1.1.tar.gz','r:gz') as archive:
            for member in archive:
                name=Path(member.name).name
                if not member.isfile() or name not in ('en-US.jsonl','tl-PH.jsonl','LICENSE'): continue
                if member.size>20_000_000: raise ValueError('Unexpected corpus member size.')
                content=archive.extractfile(member).read()
                if name=='LICENSE': (DEST/'MASSIVE-LICENSE.txt').write_bytes(content);continue
                output=DEST/('massive-'+name)
                partitions={}
                with output.open('w',encoding='utf-8') as target:
                    for line in content.decode('utf-8').splitlines():
                        row=json.loads(line)
                        # Drop worker identifiers, annotations, judgments and slot/person metadata.
                        sample={key:row[key] for key in ('id','locale','partition','intent','utt')}
                        partitions[sample['partition']]=partitions.get(sample['partition'],0)+1
                        target.write(json.dumps(sample,ensure_ascii=False)+'\n')
                counts[name]=partitions
        if set(counts)!= {'en-US.jsonl','tl-PH.jsonl'}: raise ValueError('Required locales are missing.')
        source['selected_partitions']=counts
        manifest['sources'].append(source)
    (DEST/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__': main()
