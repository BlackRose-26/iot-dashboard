"""Build a public word-only vocabulary. No test cases, chat or project examples.

Build-only dependency: nltk==3.9.2 and its public WordNet corpus. The application
uses the resulting JSON; it never downloads data or imports NLTK at runtime.
"""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unicodedata
import urllib.parse
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parents[1]
PAGE='https://kaikki.org/dictionary/Tagalog/index.html'
ALLOWED_POS={'adj','adv','verb','noun','pron','det','article','prep','conj','particle','intj','contraction'}


def digest(path):
    with path.open('rb') as stream: return hashlib.file_digest(stream,'sha256').hexdigest()


def word_form(value):
    if value!=value.lower(): return None
    value=''.join(c for c in unicodedata.normalize('NFKD',value) if not unicodedata.combining(c))
    return value if re.fullmatch(r'[a-z]{2,30}(?:-[a-z]{2,30})?',value) else None


class Links(HTMLParser):
    def __init__(self): super().__init__();self.urls=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a': self.urls.extend(v for k,v in attrs if k=='href' and v and v.endswith('.jsonl'))


def build():
    import nltk
    nltk.data.path.insert(0,str(ROOT/'.tools/nltk_data'))
    from nltk.corpus import wordnet as wn
    output=ROOT/'backend/data/assistant-language-lexicon.json'
    if output.exists(): raise ValueError('Lexicon already exists. Never rebuild a frozen predictor implicitly.')
    cache=ROOT/'.tools/public-language'
    cache.mkdir(parents=True,exist_ok=True)
    parser=Links()
    page=urllib.request.urlopen(PAGE,timeout=30).read().decode('utf-8')
    parser.feed(page)
    url=urllib.parse.urljoin(PAGE,next(u for u in parser.urls if 'Tagalog' in u))
    raw=cache/'Tagalog.jsonl'
    if not raw.exists():
        size=0
        with urllib.request.urlopen(url,timeout=45) as source,raw.with_suffix('.download').open('wb') as target:
            while block:=source.read(1024*1024):
                size+=len(block)
                if size>200*1024*1024: raise ValueError('Public dictionary exceeds the declared download bound.')
                target.write(block)
        raw.with_suffix('.download').replace(raw)
    english=set();excluded=set()
    for synset in wn.all_synsets():
        private_role = synset.lexname()=='noun.person' or bool(synset.instance_hypernyms())
        for lemma in synset.lemmas():
            value=lemma.name()
            if private_role or value!=value.lower():
                excluded.add(value.lower());continue
            if term:=word_form(value): english.add(term)
    english-=excluded
    tagalog=set();names=set()
    for line in raw.open(encoding='utf-8'):
        row=json.loads(line)
        if row.get('lang_code')!='tl': continue
        value=row.get('word','')
        if row.get('pos')=='name' or value!=value.lower():
            if term:=word_form(value.lower()): names.add(term)
            continue
        if row.get('pos') not in ALLOWED_POS: continue
        if term:=word_form(value): tagalog.add(term)
        for form in row.get('forms',[]):
            if term:=word_form(form.get('form','')): tagalog.add(term)
    tagalog-=names
    assert len(english)>20000 and len(tagalog)>3000
    wordnet_zip=ROOT/'.tools/nltk_data/corpora/wordnet.zip'
    metadata={'purpose':'Public word forms only, never intent labels or evaluation examples.',
              'wordnet':{'version':wn.get_version(),'source':'https://wordnet.princeton.edu/',
                         'archive_sha256':digest(wordnet_zip),'license':'WordNet-3.0'},
              'tagalog':{'source':PAGE,'download':url,'source_sha256':digest(raw),
                         'license':'CC-BY-SA-4.0; source Wiktionary via Kaikki/Wiktextract'},
              'filter':'Lowercase bounded ASCII word forms; proper names, WordNet person/instance entries and Tagalog proper-name entries removed. No definitions, glosses, sentences or examples.',
              'english':sorted(english),'tagalog':sorted(tagalog)}
    output.write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with zipfile.ZipFile(wordnet_zip) as archive:
        (ROOT/'backend/data/WORDNET-LICENSE.txt').write_bytes(archive.read('wordnet/LICENSE'))
    print(json.dumps({'english':len(english),'tagalog':len(tagalog),'asset_sha256':digest(output),'tagalog_source_sha256':digest(raw)}))


V2_OUTPUT='backend/data/assistant-language-lexicon-v2.json'


def wordnet_rows(archive):
    """Parse WordNet 3.0 data files directly (same corpus as v1; NLTK not required)."""
    for pos in ('noun','verb','adj','adv'):
        for line in archive.read(f'wordnet/data.{pos}').decode('latin-1').splitlines():
            if line.startswith('  '): continue
            parts=line.split()
            lexfile,count=int(parts[1]),int(parts[3],16)
            lemmas=[re.sub(r'\(.*\)$','',parts[4+2*i]) for i in range(count)]
            pointer_index=4+2*count
            pointers=[parts[pointer_index+1+4*i] for i in range(int(parts[pointer_index]))]
            yield pos,lexfile,lemmas,'@i' in pointers


def build_v2():
    """v2 (24 November 2026): keep a word when at least one of its senses is ordinary.

    v1 removed a word entirely if ANY sense was a person/instance or capitalised, which
    dropped everyday words such as head, power, sort, better, add, down and far. v2 still
    removes words whose every sense is a person, instance or proper name, adds WordNet's
    irregular inflections (ran, meant, oldest) and keeps Tagalog common words that only
    share a spelling with some proper-name entry. Inputs are local: the same WordNet
    archive and the cached Kaikki file recorded by v1. No glosses, examples or labels.
    """
    output=ROOT/V2_OUTPUT
    if output.exists(): raise ValueError('Lexicon v2 already exists. Never rebuild a frozen predictor implicitly.')
    wordnet_zip=ROOT/'.tools/nltk_data/corpora/wordnet.zip'
    raw=ROOT/'.tools/public-language/Tagalog.jsonl'
    if not wordnet_zip.is_file() or not raw.is_file(): raise ValueError('Local WordNet archive or cached Kaikki file is missing.')
    ordinary=set()
    with zipfile.ZipFile(wordnet_zip) as archive:
        for pos,lexfile,lemmas,instance in wordnet_rows(archive):
            private_role=(pos=='noun' and lexfile==18) or instance  # lexfile 18 = noun.person
            for value in lemmas:
                if private_role or value!=value.lower(): continue
                if term:=word_form(value.replace('_','-')): ordinary.add(term)
        irregular=set()
        for pos in ('noun','verb','adj','adv'):
            for line in archive.read(f'wordnet/{pos}.exc').decode('latin-1').splitlines():
                form,*bases=line.split()
                if (term:=word_form(form)) and any(base in ordinary for base in bases): irregular.add(term)
        version=archive.read('wordnet/README').decode('latin-1')
    english=ordinary|irregular
    tagalog=set();names=set()
    for line in raw.open(encoding='utf-8'):
        row=json.loads(line)
        if row.get('lang_code')!='tl': continue
        value=row.get('word','')
        if row.get('pos')=='name':
            # Personal/place names are title case (Maria); all-caps acronyms (ADD) are not names.
            if value[:1].isupper() and value[1:]==value[1:].lower() and (term:=word_form(value.lower())): names.add(term)
            continue
        if value!=value.lower() or row.get('pos') not in ALLOWED_POS: continue  # abbreviations are skipped, not names
        if term:=word_form(value): tagalog.add(term)
        for form in row.get('forms',[]):
            if term:=word_form(form.get('form','')): tagalog.add(term)
    names-=tagalog  # a name spelling never removes a common Tagalog word
    # Filipino given names that are also rare English words (e.g. maria) stay unknown,
    # so "score of Maria" is still held for clarification instead of answered generally.
    # Words that v1 already accepted (ago, casino) are never removed by this rule.
    v1=json.loads((ROOT/'backend/data/assistant-language-lexicon.json').read_text(encoding='utf-8'))
    names-=set(v1['english'])|set(v1['tagalog'])
    english-=names
    assert len(english)>60000 and len(tagalog)>3000 and not names&(english|tagalog)
    metadata={'purpose':'Public word forms only, never intent labels or evaluation examples.',
              'version':2,
              'wordnet':{'version':'3.0' if 'WordNet 3.0' in version else 'unknown','source':'https://wordnet.princeton.edu/',
                         'archive_sha256':digest(wordnet_zip),'license':'WordNet-3.0'},
              'tagalog':{'source':PAGE,'source_sha256':digest(raw),
                         'license':'CC-BY-SA-4.0; source Wiktionary via Kaikki/Wiktextract'},
              'filter':'Lowercase bounded ASCII word forms. A word is kept when at least one sense is ordinary; '
                       'words whose every WordNet sense is a person/instance or capitalised are removed, as are '
                       'Tagalog spellings found only as proper names. WordNet irregular inflections of kept words '
                       'are added. No definitions, glosses, sentences or examples.',
              'english':sorted(english),'tagalog':sorted(tagalog)}
    output.write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'english':len(english),'irregular':len(irregular),'tagalog':len(tagalog),
                      'asset_sha256':digest(output),'tagalog_source_sha256':digest(raw)}))


if __name__=='__main__':
    import sys
    build_v2() if '--v2' in sys.argv else build()
