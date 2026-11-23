"""Plot retained local DEVELOPMENT counts; no generated or estimated accuracy."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / 'results/offline-lab-20261120.json').read_text(encoding='utf-8'))
names = ['ollama-v11', 'tfidf-original', 'tfidf-normalized', 'e5-frozen-linear', 'setfit-multilingual']
labels = ['Ollama adapter', 'TF-IDF original', 'TF-IDF normalized', 'Frozen E5', 'Trained SetFit']
items = [data['candidates'][name] for name in names]
fig, axes = plt.subplots(1, 3, figsize=(16, 6.2), constrained_layout=True)
fig.suptitle('Stack Intelligence · local development experiment', fontsize=18, weight='bold')
y = np.arange(len(names))
for ax in axes:
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.spines[['top', 'right', 'left']].set_visible(False)
    ax.set_axisbelow(True)
    ax.grid(axis='x', alpha=.18)
    ax.tick_params(axis='y', length=0)
a = [c['balanced_development']['primary_correct'] for c in items]
b = [c['balanced_development']['exact_correct'] for c in items]
axes[0].barh(y-.17, a, height=.3, color='#456780', label='Primary topic')
axes[0].barh(y+.17, b, height=.3, color='#a5bac8', label='Exact label incl. subtype')
axes[0].set(title='Correct labels / 130 questions', xlim=(0, 145), xlabel='Measured count')
for i, (x, z) in enumerate(zip(a, b)):
    axes[0].text(x+2, i-.17, str(x), va='center', fontsize=9)
    axes[0].text(z+2, i+.17, str(z), va='center', fontsize=9)
axes[0].legend(loc='lower right', fontsize=8)
counts = [c['balanced_development']['answered_valid_n'] for c in items]
axes[1].barh(y, counts, color='#456780', height=.5)
axes[1].set(title='Answer-policy coverage / 120 supported', xlim=(0, 132), xlabel='Answered supported questions')
for i, x in enumerate(counts):
    axes[1].text(x+2, i, str(x), va='center', fontsize=10)
before = [c['context_stress']['primary_correct_before'] for c in items]
after = [c['context_stress']['primary_correct_after'] for c in items]
axes[2].barh(y-.17, before, height=.3, color='#456780', label='Original input')
axes[2].barh(y+.17, after, height=.3, color='#b37658', label='Unrelated prior topic added')
axes[2].set(title='Context stress: primary correct / 120', xlim=(0, 132), xlabel='Same questions, paired diagnostic')
for i, (x, z) in enumerate(zip(before, after)):
    axes[2].text(x+2, i-.17, str(x), va='center', fontsize=9)
    axes[2].text(z+2, i+.17, str(z), va='center', fontsize=9)
axes[2].legend(loc='lower right', fontsize=8)
fig.supxlabel('Synthetic development data · 10 cases per intent · not independent unseen accuracy or factual-answer accuracy', fontsize=11)
target = HERE / 'offline-lab-comparison.png'
fig.savefig(target, dpi=180, facecolor='white')
plt.close(fig)
print(target)
