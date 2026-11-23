"""Render the consumed holdout's recorded counts without resampling or inference."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent


def main():
    report=json.loads((HERE/'results/holdout-v1.json').read_text(encoding='utf-8'))
    metrics=report['metrics'];rows=metrics['per_intent']
    labels=list(rows)
    counts=[rows[label]['accepted'] for label in labels]
    assert metrics['n']==325 and sum(counts)==metrics['accepted']
    assert all(row['n']==25 for row in rows.values())
    fig,axis=plt.subplots(figsize=(10,7))
    positions=list(range(len(labels)))
    bars=axis.barh(positions,counts,color=['#4c647b' if label!='unsupported' else '#899684' for label in labels])
    axis.set_yticks(positions,labels)
    axis.invert_yaxis()
    axis.set(xlim=(0,29),xticks=range(0,26,5),xlabel='Accepted intent/context matches out of 25')
    for bar,count in zip(bars,counts):
        axis.text(count+.35,bar.get_y()+bar.get_height()/2,f'{count}/25',va='center')
    axis.spines[['top','right']].set_visible(False)
    axis.grid(axis='x',alpha=.18);axis.set_axisbelow(True)
    fig.suptitle(f"First-use synthetic holdout: {metrics['accepted']}/{metrics['n']} ({metrics['accepted_accuracy']*100:.2f}%)",fontsize=14)
    fig.text(.5,.02,'25 cases per primary intent. Predictor frozen; no test-based repairs. Real-user accuracy remains unmeasured.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.05,1,.94))
    fig.savefig(HERE/'holdout-v1-intents.png',dpi=180)
    plt.close(fig)
    print('Rendered all 13 intent groups, including zero-match groups, from the frozen result.')


if __name__=='__main__':
    main()
