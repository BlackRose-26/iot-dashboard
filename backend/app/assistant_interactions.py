"""System-grounded conversation examples and bounded full-utterance composition."""
from functools import lru_cache
import json
from pathlib import Path
import re
import unicodedata

INTERACTIONS = Path(__file__).resolve().parents[1] / 'data' / 'assistant-interactions.json'
BEHAVIORAL = INTERACTIONS.with_name('assistant-behavioral.json')
SPELLINGS = {'goodevening':'good evening','goodmorning':'good morning','goodafternoon':'good afternoon',
    'goodday':'good day','goodnight':'good night','thankyou':'thank you','thanksalot':'thanks a lot',
    'hellogoodevening':'hello good evening','hellogoodmorning':'hello good morning',
    'helo':'hello','hellow':'hello','mornin':'morning','evenin':'evening'}


def social_spelling(value):
    """Only known social spellings change; arbitrary request words stay intact."""
    def replace(match):
        word = match[0]
        if word in SPELLINGS: return SPELLINGS[word]
        if len(word)<=20:
            if re.fullmatch(r'he+l+o+',word): return 'hello'
            if re.fullmatch(r'hi+',word): return 'hi'
            if re.fullmatch(r'he+y+',word): return 'hey'
        return word
    return re.sub(r'\b[a-z]+\b',replace,value)


def interaction_text(value):
    value = unicodedata.normalize('NFKC',value).lower().replace('’', "'")
    return ' '.join(re.sub(r"[^\w\s']",' ',social_spelling(value)).split())


@lru_cache(maxsize=1)
def interaction_rows():
    return tuple(row for path in (INTERACTIONS,BEHAVIORAL)
                 for row in json.loads(path.read_text(encoding='utf-8'))['examples'])


def interaction_words():
    return {word for row in interaction_rows() if row['split']=='train' and row['kind']!='boundary'
            for word in re.findall(r'[a-z]+(?:-[a-z]+)?',row['question'].lower())}


def interaction_social(value):
    for row in interaction_rows():
        if row['split']=='train' and row['kind']=='social' and interaction_text(row['question'])==value:
            return row['target']['social'],row['language']
    return None


@lru_cache(maxsize=1)
def social_phrases():
    phrases = {}
    base = {
        'greeting':['hello','hi','hey','good morning','good afternoon','good evening','good day',
                    'morning','magandang umaga','magandang hapon','magandang gabi','magandang araw'],
        'wellbeing':['how are you','how are you doing','how are you today','kumusta ka','kamusta ka'],
        'thanks':['thanks','thank you','thanks a lot','thank you so much','salamat','maraming salamat'],
        'acknowledge':['okay','ok','got it','understood','sige','gets'],
        'farewell':['bye','goodbye','see you','see you later','good night','paalam'],
        'help':['help','help me','can you help me','could you help me','what can you do','patulong naman'],
        'identity':['who are you','what is your name','sino ka','anong pangalan mo'],
    }
    for act,values in base.items():
        for phrase in values: phrases[tuple(phrase.split())]=act
    # The original corpus supplies full social phrases; behavioral compound examples
    # remain examples rather than recursively becoming grammar fragments.
    for row in json.loads(INTERACTIONS.read_text(encoding='utf-8'))['examples']:
        if row['kind']=='social' and row['split']=='train':
            phrases[tuple(interaction_text(row['question']).split())]=row['target']['social']
    return tuple(sorted(phrases.items(),key=lambda item:len(item[0]),reverse=True))


def composed_social(value):
    """Consume every word using known phrases; unknown tails never become small talk."""
    words = tuple(value.split())
    if not words or len(words)>60: return None
    @lru_cache(maxsize=None)
    def parse(index, count):
        if index==len(words): return () if count else None
        if count>6: return None
        for phrase,act in social_phrases():
            end=index+len(phrase)
            if words[index:end]==phrase:
                rest=parse(end,count+1)
                if rest is not None: return (act,)+rest
        # Courtesy endings never change the social act ("thank you for your help",
        # "salamat po sa inyong pagtulong sa akin", "good evening to you").
        for phrase in (('po',),('please',),('assistant',),('stack','intelligence'),('stack','moko','baby'),('there',),('and',),('also',),
                       ('to','you'),('to','all'),('for','your','help'),('for','helping','me'),('for','helping'),('for','the','help'),
                       ('sa','akin'),('sa','iyo'),('sa','inyo'),('sa','inyong','pagtulong'),('sa','iyong','tulong'),
                       ('sa','tulong','mo'),('sa','tulong','ninyo')):
            end=index+len(phrase)
            if words[index:end]==phrase:
                rest=parse(end,count)
                if rest is not None: return rest
        return None
    acts=parse(0,0)
    if not acts: return None
    # A substantive social act such as help/thanks takes precedence over a greeting.
    act=next((a for a in reversed(acts) if a!='greeting'),'greeting')
    language='taglish' if set(words)&{'po','magandang','kumusta','kamusta','salamat','sige','paalam','patulong','sino'} else 'en'
    return act,language


def strip_social_prefaces(value):
    value=social_spelling(value)
    original=value
    pattern=r'^(?:hello|hi|hey|good morning|good afternoon|good evening|good day|thank you|thanks|maraming salamat|salamat)(?: there)?(?: po)?[\s,!:;.]+?'
    for _ in range(8):
        remaining=re.sub(r'^\W*','',re.sub(pattern,'',value,count=1))
        if remaining==value: break
        value=remaining
    return value or original


COMMON_RESPONSES = {
    'greeting': ("Hi! I'm Stack Intelligence. How can I help with Stack Moko Baby?",
                 'Hello po! Ako si Stack Intelligence. Ano ang gusto mong malaman tungkol sa Stack Moko Baby?'),
    'wellbeing': ("I'm here and ready to help with your event. What would you like to check?",
                  'Nandito ako at handang tumulong sa event. Ano ang gusto mong tingnan?'),
    'help': ('I can help with Stack Moko Baby gameplay, QR registration, the queue, scores, dashboard and cabinet observations. Where would you like to start?',
             'Pwede kitang tulungan sa gameplay, QR registration, pila, scores, dashboard at cabinet observations ng Stack Moko Baby. Saan tayo magsisimula?'),
    'identity': ("I'm Stack Intelligence, your Stack Moko Baby assistant for system questions and recorded event data.",
                 'Ako si Stack Intelligence, ang assistant mo sa Stack Moko Baby para sa system at recorded event data.'),
    'thanks': ("You're welcome! Let me know if you need anything else for the event.",
               'Walang anuman! Sabihin mo lang kung may kailangan ka pa tungkol sa event.'),
    'acknowledge': ('Got it. We can continue with your last system question or look at another part of the event.',
                    'Sige! Pwede nating ituloy ang huling system question o tingnan ang ibang bahagi ng event.'),
    'farewell': ("See you! I'll be here when you need help with Stack Moko Baby.",
                 'Sige, ingat! Nandito lang ako kung kailangan mo ng tulong sa Stack Moko Baby.'),
}


def greeting_answer(value, fallback, language):
    names={'good morning':('Good morning','Magandang umaga'),'magandang umaga':('Good morning','Magandang umaga'),
           'good afternoon':('Good afternoon','Magandang hapon'),'magandang hapon':('Good afternoon','Magandang hapon'),
           'good evening':('Good evening','Magandang gabi'),'magandang gabi':('Good evening','Magandang gabi')}
    matches=list(re.finditer(r'\b(?:'+ '|'.join(names)+r')\b',value))
    if not matches: return fallback
    opening=names[matches[-1][0]][1 if language=='taglish' else 0]
    return opening+'! '+('Ako si Stack Intelligence. Ano ang gusto mong malaman tungkol sa Stack Moko Baby?' if language=='taglish' else
                          "I'm Stack Intelligence. How can I help with Stack Moko Baby?")
