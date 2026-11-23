"""Plot measured routing outputs only; no model calls, database access or invented values."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix

HERE = Path(__file__).resolve().parent


def measured(name):
    report = json.loads((HERE/'results'/name).read_text(encoding='utf-8'))
    cases = report['cases']
    expected = [row['expected'] for row in cases]
    predicted = [row['predicted'] for row in cases]
    correct = sum(a == b for a,b in zip(expected,predicted))
    assert len(cases) == report['n'] and correct == report['correct']
    return report, float(accuracy_score(expected,predicted))


def main():
    groups = [('Reused regression', 'regression-before.json', 'regression-after.json'),
              ('Synthetic validation', 'validation-before.json', 'validation-after.json')]
    fig,axes = plt.subplots(1,2,figsize=(10,5),sharey=True)
    summary = {'scope':'Measured routing stage; synthetic development data, not blind real-user or factual-answer accuracy.', 'groups':[]}
    for axis,(title,before,after) in zip(axes,groups):
        old,old_score = measured(before)
        new,new_score = measured(after)
        assert old['dataset_sha256'] == new['dataset_sha256']
        assert [(r['id'],r['expected']) for r in old['cases']] == [(r['id'],r['expected']) for r in new['cases']]
        bars = axis.bar(['Before','After'],[old_score*100,new_score*100],color=['#a0a9b5','#3d6b92'],width=.58)
        for bar,score,report in zip(bars,[old_score,new_score],[old,new]):
            axis.annotate(f"{report['correct']}/{report['n']} ({score*100:.2f}%)",
                          (bar.get_x()+bar.get_width()/2,bar.get_height()),ha='center',xytext=(0,6),textcoords='offset points')
        axis.set_title(title)
        axis.set_ylim(0,115)
        axis.set_yticks(range(0,101,20))
        axis.spines[['top','right']].set_visible(False)
        axis.grid(axis='y',alpha=.2)
        axis.set_axisbelow(True)
        summary['groups'].append({'name':title,'n':old['n'],'before_correct':old['correct'],
                                 'after_correct':new['correct'],'before_accuracy':old_score,'after_accuracy':new_score,
                                 'dataset_sha256':old['dataset_sha256']})
    axes[0].set_ylabel('Exact topic/subtype accuracy (%)')
    fig.suptitle('Stack Intelligence: measured routing improvement',fontsize=14)
    fig.text(.5,.935,'Synthetic development sets; not real-user or factual-answer accuracy.',ha='center',fontsize=9)
    fig.text(.5,.02,'Same frozen case IDs and labels. Validation informed development. Model weights were not trained.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.05,1,.93))
    fig.savefig(HERE/'routing-accuracy.png',dpi=180)
    plt.close(fig)
    report,_ = measured('validation-after.json')
    labels = sorted({r['expected'] for r in report['cases']} | {r['predicted'] for r in report['cases']})
    matrix = confusion_matrix([r['expected'] for r in report['cases']],[r['predicted'] for r in report['cases']],labels=labels)
    fig,axis = plt.subplots(figsize=(11,9))
    axis.imshow(matrix,cmap='Blues',vmin=0)
    axis.set_xticks(range(len(labels)),labels,rotation=60,ha='right')
    axis.set_yticks(range(len(labels)),labels)
    for y,row in enumerate(matrix):
        for x,value in enumerate(row):
            if value:
                axis.text(x,y,str(value),ha='center',va='center',color='white' if value>matrix.max()/2 else 'black')
    axis.set(xlabel='Predicted topic/subtype',ylabel='Expected topic/subtype',title='Synthetic validation: actual routing counts (n=24)')
    fig.tight_layout()
    fig.savefig(HERE/'routing-confusion.png',dpi=180)
    plt.close(fig)
    (HERE/'comparison.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
