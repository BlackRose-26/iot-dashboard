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


if __name__=='__main__': build()
