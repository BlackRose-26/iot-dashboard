"""Plot recorded results only; never predicts, selects or drops test cases."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT=Path(__file__).resolve().parent


def plot():
    names=['holdout-v1.json','holdout-v1-regression-v10.json','holdout-v1-regression-v11.json']
    reports=[json.loads((ROOT/'results'/name).read_text(encoding='utf-8')) for name in names]
    assert all(r['metrics']['n']==325 for r in reports)
    assert reports[0]['model']==reports[2]['model']
    topics=list(reports[0]['metrics']['per_intent'])
    labels=['Overview','Players','Queue','Cabinet','Scores','Levels','Activity trend','Ranking','Definition','System knowledge','Social','Follow-up','Unsupported / safety']
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
    fig,ax=plt.subplots(figsize=(11,9),dpi=180)
    colors=['#b7c0ca','#74869b','#285c93']
    stages=['Original first-use measurement','v10 consumed-set regression','v11 consumed-set regression']
    positions=np.arange(len(topics))
    for index,(report,color,stage) in enumerate(zip(reports,colors,stages,strict=True)):
        metrics=report['metrics']
        counts=[metrics['per_intent'][topic]['accepted'] for topic in topics]
        assert all(metrics['per_intent'][topic]['n']==25 for topic in topics)
        assert sum(counts)==metrics['accepted']
        bars=ax.barh(positions+(index-1)*0.25,counts,height=0.22,color=color,
                     label=f"{stage}: {metrics['accepted']}/325 ({metrics['accepted_accuracy']:.2%})",zorder=3)
        ax.bar_label(bars,labels=[str(n) for n in counts],padding=3,fontsize=8,color='#263446')
    ax.set_yticks(positions,labels)
    ax.invert_yaxis()
    ax.set_xlim(0,27)
    ax.set_xticks(range(0,26,5))
    ax.set_xlabel('Accepted intent/context matches out of 25 per primary intent')
    ax.grid(axis='x',color='#e3e7ec',zorder=0)
    ax.tick_params(axis='y',length=0)
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.suptitle('Stack Intelligence: preserved baseline and consumed-set regressions',x=0.08,y=0.98,ha='left',fontsize=15,fontweight='bold')
    ax.legend(loc='lower left',bbox_to_anchor=(0,1.01),frameon=False,fontsize=9)
    fig.text(0.08,0.025,'Same 325 synthetic cases, gold labels and scorer; all failures remain counted. Reuse is regression, not new unseen accuracy.\nv11: 135 valid-request clarifications; 24/25 unsupported cases rejected; 1 false acceptance. Hardware not evaluated.',fontsize=9,color='#455467')
    fig.subplots_adjust(left=0.21,right=0.96,top=0.85,bottom=0.11)
    path=ROOT/'language-repair-regression.png'
    fig.savefig(path,facecolor='white')
    plt.close(fig)
    print(path)


if __name__=='__main__': plot()
