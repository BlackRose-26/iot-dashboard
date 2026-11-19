"""Generate standard scikit-learn/Matplotlib accuracy plots from measured labels.

Install matplotlib and scikit-learn in an analysis environment, then run this
file. It reads the recorded evaluation, not the live application database.
"""
from collections import defaultdict
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
import sklearn

ROOT=Path(__file__).resolve().parent
evaluation=json.loads((ROOT/'intent-routing-evaluation.json').read_text(encoding='utf-8'))
cases=evaluation['cases']
assert len(cases)==evaluation['n']==21
assert len({row['id'] for row in cases})==len(cases)
truth=[row['expected'] for row in cases]
predictions=[row['predicted'] for row in cases]
overall=float(accuracy_score(truth,predictions))
correct=int(accuracy_score(truth,predictions,normalize=False))
assert correct==evaluation['correct']
groups=defaultdict(list)
for row in cases:groups[row['category']].append(row)
categories=['Event and queue queries','System explanations','Metric definitions']
values=[];counts=[]
for name in categories:
    rows=groups[name]
    values.append(float(accuracy_score([r['expected'] for r in rows],[r['predicted'] for r in rows]))*100)
    counts.append((sum(r['correct'] for r in rows),len(rows)))

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.titlesize':13,
                     'axes.labelsize':11,'savefig.facecolor':'white'})
fig,axes=plt.subplots(1,2,figsize=(12,5.2),gridspec_kw={'width_ratios':[.8,1.55]})
fig.suptitle('NLP Intent-Routing Accuracy',fontsize=18,fontweight='bold',y=.965)
fig.text(.5,.88,f"Local {evaluation['model']} | Existing project test split | n = {len(cases)}",ha='center',fontsize=10.5)
for ax in axes:
    ax.set_ylim(0,112)
    ax.set_yticks(range(0,101,20))
    ax.set_ylabel('Accuracy (%)')
    ax.grid(axis='y',color='#dddddd',linewidth=.7)
    ax.set_axisbelow(True)
    ax.spines[['top','right']].set_visible(False)
axes[0].bar(['Overall'],[100*overall],color='tab:blue',width=.46)
axes[0].text(0,100*overall+3,f'{100*overall:.1f}%\n({correct}/{len(cases)})',ha='center',va='bottom',fontsize=12,fontweight='bold')
axes[0].set_title('Exact topic and subtype')
axes[1].bar(range(3),values,color='tab:blue',width=.55)
axes[1].set_xticks(range(3),['Event and queue\nqueries','System\nexplanations','Metric\ndefinitions'])
for index,(value,(passed,total)) in enumerate(zip(values,counts)):
    axes[1].text(index,value+3,f'{value:.1f}%\n({passed}/{total})',ha='center',va='bottom',fontsize=11)
axes[1].set_title('Accuracy by question category')
fig.text(.5,.095,'Accuracy = correct predicted labels / evaluated questions × 100',ha='center',fontsize=10.5)
fig.text(.5,.042,'Small synthetic developer-reviewed test set; measures the router before backend semantic corrections.',ha='center',fontsize=9,color='#505050')
fig.subplots_adjust(left=.075,right=.975,bottom=.245,top=.77,wspace=.38)
fig.savefig(ROOT/'nlp-accuracy.png',dpi=240)
plt.close(fig)

fig,ax=plt.subplots(figsize=(8,4.6))
bars=ax.bar(['Correct','Incorrect'],[correct,len(cases)-correct],color=['tab:blue','tab:orange'],width=.5)
ax.set_ylim(0,len(cases)+3)
ax.set_yticks(range(0,len(cases)+1,3))
ax.set_ylabel('Number of test questions')
ax.set_title(f'Intent-Router Prediction Results — Accuracy {100*overall:.1f}%')
ax.grid(axis='y',color='#dddddd',linewidth=.7);ax.set_axisbelow(True)
ax.spines[['top','right']].set_visible(False)
ax.bar_label(bars,padding=5,fontsize=12)
fig.text(.5,.035,f'Existing synthetic test split: n={len(cases)}; exact topic and relevant subtype matching.',ha='center',fontsize=9,color='#505050')
fig.tight_layout(rect=(0,.08,1,1));fig.savefig(ROOT/'nlp-accuracy-counts.png',dpi=240);plt.close(fig)

summary={'metric':'accuracy_score','component':evaluation['component'],'accuracy':overall,
         'accuracy_percent':round(100*overall,2),'correct':correct,'total':len(cases),
         'by_category':{name:{'accuracy_percent':round(value,2),'correct':pair[0],'total':pair[1]}
            for name,value,pair in zip(categories,values,counts)},
         'sklearn_version':sklearn.__version__,'matplotlib_version':matplotlib.__version__,
         'limits':evaluation['limits']}
(ROOT/'accuracy-metrics.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
