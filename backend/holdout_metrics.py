"""Count all frozen cases, including rejected valid requests and infrastructure errors."""
from collections import Counter, defaultdict
import math


def wilson(correct,total):
    if total<=0: return None
    z=1.959963984540054
    p=correct/total;den=1+z*z/total
    center=(p+z*z/(2*total))/den
    radius=z*math.sqrt(p*(1-p)/total+z*z/(4*total*total))/den
    return [max(0,center-radius),min(1,center+radius)]


def summarize(cases,topics):
    groups=defaultdict(list)
    for row in cases: groups[row['expected_topic']].append(row)
    per={}
    for topic in topics:
        rows=groups[topic];tp=sum(r['predicted_topic']==topic for r in rows)
        fp=sum(r['predicted_topic']==topic and r['expected_topic']!=topic for r in cases)
        precision=tp/(tp+fp) if tp+fp else 0
        recall=tp/len(rows) if rows else 0
        f1=2*precision*recall/(precision+recall) if precision+recall else 0
        accepted=sum(r['accepted'] for r in rows)
        per[topic]={'n':len(rows),'primary_correct':tp,'accepted':accepted,'precision':precision,'recall':recall,'f1':f1,
                    'accepted_accuracy':accepted/len(rows) if rows else None,
                    'accepted_wilson95':wilson(accepted,len(rows))}
    n=len(cases);accepted=sum(r['accepted'] for r in cases)
    strict=sum(r['exact_label'] for r in cases)
    primary=sum(r['expected_topic']==r['predicted_topic'] for r in cases)
    return {'n':n,'accepted':accepted,'accepted_accuracy':accepted/n if n else None,'accepted_wilson95':wilson(accepted,n),
            'exact_label_correct':strict,'exact_label_accuracy':strict/n if n else None,
            'primary_correct':primary,'primary_accuracy':primary/n if n else None,
            'macro_f1':sum(row['f1'] for row in per.values())/len(topics),
            'per_intent':per,
            'by_language':{language:{'n':sum(r['language']==language for r in cases),
                           'accepted':sum(r['accepted'] and r['language']==language for r in cases)} for language in ('en','taglish')},
            'confusion':[{'expected':a,'predicted':b,'n':count} for (a,b),count in Counter((r['expected_topic'],r['predicted_topic']) for r in cases).items()],
            'unsupported_false_accepts':sum(r['expected_topic']=='unsupported' and r['status'] not in ('refused','needs_clarification') for r in cases),
            'valid_request_clarifications':sum(r['expected_topic']!='unsupported' and r['status']=='needs_clarification' for r in cases),
            'unavailable_or_errors':sum(r['status'] in ('unavailable','error') for r in cases),
            'interval_note':'Wilson intervals assume independent cases; paired language/family cases can be correlated. They do not establish real-user performance.'}
