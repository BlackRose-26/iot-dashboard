"""Reviewed linguistic projection, independent of evaluation prompts.

No fuzzy matching or arbitrary dictionary imports: a person's name must never be
autocorrected into a metric. Unknown content remains unknown. These are public
concepts, common question grammar and bounded inflections, not labelled examples.
"""
import re
import unicodedata
from functools import lru_cache
import hashlib
import json
from pathlib import Path

LEXICON = Path(__file__).resolve().parents[1]/'data/assistant-language-lexicon.json'


@lru_cache(maxsize=1)
def lexical_resource():
    payload=LEXICON.read_bytes()
    data=json.loads(payload)
    words=set(data['english'])|set(data['tagalog'])
    if len(words)<20000 or any(not re.fullmatch(r'[a-z]{2,30}(?:-[a-z]{2,30})?',word) for word in words):
        raise ValueError('Invalid bundled public language vocabulary.')
    return frozenset(words),hashlib.sha256(payload).hexdigest()


@lru_cache(maxsize=1)
def tagalog_language_words():
    data=json.loads(LEXICON.read_text(encoding='utf-8'))
    return frozenset(data['tagalog'])-frozenset(data['english'])


# Canonical meanings rather than an ever-growing list of complete questions.
CONCEPTS = {
    'overview': 'recap rundown snapshot overview buod pangkalahatan',
    'summary': 'summaries summarize summarise summarization summarisation',
    'players': 'attendees entrants contestants competitors participants manlalaro kalahok',
    'registration': 'signup signups sign-up sign-ups enrolment enrollment pagpaparehistro pagpapalista',
    'registered': 'enrolled signed-up nakarehistro nakapagregister nakapagrehistro nagparehistro nagpalista',
    'completed': 'concluded concluded-rounds natapos nakatapos nakapaglaro',
    'queue': 'lineup waitlist wait-list pila pagpila nakapila naghihintay',
    'waiting': 'awaiting nag-aantay nagaantay nag-aabang nagaabang',
    'scores': 'scoreboard scoreboards puntos marka',
    'total': 'sum aggregate cumulative kabuuan kabuuang pinagsama pinagsamang',
    'average': 'avg arithmetic-mean karaniwan karaniwang',
    'highest': 'maximum max pinakamataas',
    'lowest': 'minimum min pinakamababa',
    'leaderboard': 'rankings standings talahanayan',
    'leading': 'front-runner frontrunner nangunguna',
    'level': 'stage antas hanay',
    'levels': 'stages tiers',
    'failures': 'mishaps misses bumagsak nabigo',
    'trend': 'timeline trajectory progression takbo',
    'activity': 'throughput volume aktibidad',
    'busiest': 'peak pinakamarami pinakamaraming',
    'machine': 'unit apparatus makina',
    'connectivity': 'reachability koneksyon koneksiyon pagkakakonekta',
    'connected': 'reachable konektado nakakonekta',
    'readiness': 'preparedness handa',
    'offline': 'disconnected',
    'gameplay': 'mechanics mekaniks paglalaro',
    'explain': 'elaborate clarify ipaliwanag paliwanag pakipaliwanag',
    'calculate': 'compute computation calculation kalkulahin kinakalkula pagkukuwenta pagkalkula',
    'definition': 'kahulugan ibig-sabihin',
    'show': 'display present tingnan makita ipakita patingin pakita',
    'check': 'inspect examine review suriin tignan',
    'how': 'pano papaano papano',
    'what': 'anong anu ano',
    'why': 'bakit',
    'when': 'kailan kelan',
    'many': 'karami karaming marami maraming',
    'remember': 'recall tandaan maalala',
    'memory': 'recollection alaala',
    'training': 'retraining fine-tuning finetuning',
    'architecture': 'components infrastructure setup',
}
ALIASES = {alias: canonical for canonical, values in CONCEPTS.items() for alias in values.split()}
AMBIGUOUS_WORDS = {'present','volume','unit','apparatus','snapshot','peak','marka','hanay','takbo','recall','setup','components'}
ALIASES = {word:meaning for word,meaning in ALIASES.items() if word not in AMBIGUOUS_WORDS}
ALIASES.update({word:'players' for word in ('attendee','entrant','contestant','competitor')})
ALIASES.update({word:'list' for word in ('lista','maglista','ilista')})
PUBLIC_TAGALOG_ADDITIONS = {'ilahad','isalaysay','isalarawan'}
POLITE_ROOTS = {'lista','tingnan','tignan','sabi','paliwanag','check','show','explain','suriin'}
# Keep existing metric nouns unchanged; only words absent from the original
# reviewed vocabulary need projection. In particular peak != current maximum.
GRAMMAR = set('''one ones actually absolutely additionally already anyway basically certainly currently
directly especially essentially eventually ever every exactly fairly finally firstly generally
however immediately indeed just latest lately merely mostly nearly necessarily obviously
otherwise overall particularly possibly probably quickly quite rather really recently regularly
roughly secondly simply slightly specifically still subsequently surely therefore thus totally
typically usually yet although because besides despite either else even except hence neither
nor once since unless until whenever whether whilst within throughout across along among around
behind below beneath beyond during into onto outside over past regarding towards under upon
via above inside together apart afterward afterwards ahead previously afterward simultaneously
seems seem looking wondering wonder mind let lets may might must shall ought have has had having
been being done whose whom whos whats thats theres heres lets id itd dont doesnt didnt isnt arent
wasnt werent couldnt wouldnt shouldnt wont cant im ive youre youve theyre theyve weve were
please kindly could would can need needs needed want wants wanted requesting request requested
provide provides provided obtain find finds found view views see sees saw take takes taking look
looks looking check checks checked checking read reads reading fetches retrieve retrieved
explanation explanations details detailed detail describe describes described describing
tell tells telling talk talks discussing discuss discussed question questions ask asks asked
asks asking help helps helped helping assist assists regarding concerning related relating
relevant particular respective respectively specific individual individuals each everyone
everybody someone anyone somebody anything something nothing whichever whatever whenever
themselves ourselves yourself yourselves itself himself herself myself their theirs ours yours
nonetheless rather else another other others several few fewer less least more most lot lots
long longer longest short shorter shortest little bit bits whole entire full complete actual
instead likewise also too including include includes included contains contain containing
following follow follows followed followup follow-up previous prior recent latest current
refresh refreshed refreshes updating updated updates ongoing active inactive available recorded
records recording saved stored observed observation observations reported reporting showing
remaining remainder relevant understandable understanding understand understood interpret
interpretation interpretations identify identification distinguish difference differences
different compare comparison comparing compared contrast contrasts versus compared
raw normalized normal normalised typical valid invalid eligible eligibility successful unsuccessfully
today yesterday tomorrow now later earlier tonight someday morning afternoon evening
conversation conversational polite friendly brief concise elaborate plainly plain sentence sentences
okay alright alrighty yup yep yeah nope sure understood correct right great excellent nice
salamat po opo ho oho naman nga lang muna sana naman pala kasi kase kaya yata daw raw
ayon bilang tungkol hinggil patungkol ukol para itong iyang iyong inyong kanilang sila silang
nila nilang tayo tayong kami kaming natin nating namin naming ako akong ikaw kayong kayo
mo mong ko kong ka kang ba bang kung kapag habang matapos pagkatapos bago noong noon
ngayon ngayong kanina kailan kelan saan nasaan dito diyan doon rito riyan roon talaga
lamang muli ulit rin din pati saka at tsaka ngunit pero subalit dahil sapagkat kahit
pwede puwede pwedeng puwedeng maaari maari posible posibilidad kailangan kailangang gusto
gustong nais naming gusto ko bang iyong nito niyan noon pa pala medyo sobrang mas pinaka
pakisuyo pakitingnan pakisabi sabihin malaman malalaman matukoy intindihin maintindihan
naiintindihan naintindihan unawain maunawaan makatulong tutulungan tulungan kasalukuyan
kasalukuyang ngayon kasali sumali sasali makasali lahat bawat bawat-isa kabuuang gaano
katagal dami daming bilang naitalang naitala nakatala nakatalang tingin makikita nakikita
nangyari nangyayari mayroon meron wala walang hindi di hindi-pa tapos natapos naman
'''.split())

CONTRACTIONS = {
    "what's": 'what is', "who's": 'who is', "how's": 'how is', "where's": 'where is',
    "that's": 'that is', "there's": 'there is', "here's": 'here is', "it's": 'it is',
    "I'm": 'i am', "i'm": 'i am', "you're": 'you are', "we're": 'we are', "they're": 'they are',
    "can't": 'can not', "don't": 'do not', "doesn't": 'does not', "didn't": 'did not',
    "isn't": 'is not', "aren't": 'are not', "wasn't": 'was not', "weren't": 'were not',
    "couldn't": 'could not', "wouldn't": 'would not', "shouldn't": 'should not',
    "let's": 'let us', "i'd": 'i would', "i've": 'i have', "you've": 'you have',
}
PUBLIC_WORDS = GRAMMAR | set(CONCEPTS) | set(ALIASES)


def linguistic_text(question):
    value = unicodedata.normalize('NFKC', question).lower().replace('’', "'").replace('‘', "'")
    # Do not remove digits, URLs, punctuation or identifier material before the
    # privacy/control guards inspect it.
    return re.sub(r"\b[a-z]+['’][a-z]+\b", lambda m: CONTRACTIONS.get(m[0], m[0]), value)


# Closed combinations of supported metrics, plus inflected public query terms.
METRIC_COMPOUNDS = {measure+'-'+noun: (measure, noun)
                    for measure in ('average','total','highest','lowest') for noun in ('score','points')}
QUERY_FORMS = {'pangkalahatang':'overview','pakibuod':'summary','sumaling':'players','sinong':'who',
               'nangungunang':'leading','kinukuwenta':'calculate','naaalala':'remember',
               'pagsamahin':'total','smallest':'lowest','ilarawan':'describe','pakibilang':'count',
               'pinakamatagal':'longest','saang':'which','kumpara':'compare','bagong':'new',
               'unang':'first','balita':'update','lider':'leading','partisipasyon':'participation',
               'defeat':'loss','sinuman':'anyone'}


def project_words(value, vocabulary):
    # Unicode words remain visible to the unknown-subject guard, never silently
    # disappear in an otherwise-English analytical request.
    words = re.findall(r"[^\W\d_]+(?:[-'][^\W\d_]+)*", value, re.UNICODE)
    projected = []
    for word in words:
        folded=''.join(c for c in unicodedata.normalize('NFKD',word) if not unicodedata.combining(c))
        if word not in vocabulary and folded in vocabulary: word=folded
        if word in METRIC_COMPOUNDS:
            projected.extend(METRIC_COMPOUNDS[word])
            continue
        word = QUERY_FORMS.get(word,word)
        if word.startswith('paki') and word[4:] in POLITE_ROOTS:
            word=word[4:]
        if word.endswith("'s") and word[:-2] in {'game','event','cabinet','machine','system','dashboard','queue','player','participant','today','yesterday','level','score','leaderboard'}:
            word = word[:-2]
        if word in ALIASES:
            word = ALIASES[word]
        elif word not in vocabulary:
            # Only unambiguous English inflections of approved stems. No fuzzy
            # name matching, arbitrary stemming or generic Tagalog prefix stripping.
            candidates = [word[:-3]+'y'] if word.endswith('ies') else []
            if word.endswith('s') and not word.endswith('ss'): candidates.append(word[:-1])
            if word.endswith('ing'): candidates.extend([word[:-3],word[:-3]+'e'])
            if word.endswith('ed'): candidates.extend([word[:-2],word[:-1]])
            word = next((stem for stem in candidates if stem in vocabulary), word)
        projected.append(ALIASES.get(word,word))
    return projected
