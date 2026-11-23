"""Measured counts for a consumed development history ablation."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / 'results/history-lab-20261120.json').read_text(encoding='utf-8'))
values = [data['reference_frozen_e5']] + [v['original'] for v in data['candidates'].values()]
stress = [data['reference_frozen_e5_stress']['primary_correct_after']] + [v['context_stress']['primary_correct'] for v in data['candidates'].values()]
labels = ['Original E5 reference', 'History augmentation', 'Current question only', 'Question only + augmentation']
fig, axes = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)
fig.suptitle('Stack Intelligence · history-shortcut development regression', fontsize=15, weight='bold')
y = np.arange(4)
for ax in axes:
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.spines[['top', 'right', 'left']].set_visible(False)
    ax.set_axisbelow(True)
    ax.grid(axis='x', alpha=.2)
    ax.tick_params(axis='y', length=0)
axes[0].barh(y-.16, [v['primary_correct'] for v in values], height=.28, color='#456780', label='Primary topic')
axes[0].barh(y+.16, [v['exact_correct'] for v in values], height=.28, color='#a5bac8', label='Exact label incl. subtype')
for i, v in enumerate(values):
    axes[0].text(v['primary_correct']+1, i-.16, str(v['primary_correct']), va='center', fontsize=9)
    axes[0].text(v['exact_correct']+1, i+.16, str(v['exact_correct']), va='center', fontsize=9)
axes[0].set(title='Correct labels / 130 questions', xlim=(0, 140), xlabel='Measured count')
axes[0].legend(loc='lower right', fontsize=8)
axes[1].barh(y, stress, height=.5, color='#b37658')
for i, n in enumerate(stress):
    axes[1].text(n+1, i, str(n), va='center', fontsize=9)
axes[1].set(title='Unrelated prior context\nPrimary correct / 120', xlim=(0, 130), xlabel='Same paired questions, not new cases')
fig.supxlabel('Consumed synthetic development data · no independent unseen accuracy claim · no production promotion', fontsize=10)
target = HERE / 'history-lab-comparison.png'
fig.savefig(target, dpi=180, facecolor='white', bbox_inches='tight', pad_inches=.2)
plt.close(fig)
print(target)
