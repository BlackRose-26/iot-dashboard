# NLP accuracy evaluation

Measured accuracy: **57.1% (12/21)** for the local Ollama intent router before backend semantic corrections.

- `nlp-accuracy.png`: standard Matplotlib overall and category accuracy plots, calculated using scikit-learn `accuracy_score`.
- `nlp-accuracy-counts.png`: correctly and incorrectly predicted test-label counts.
- `accuracy-metrics.json`: computed accuracy values and plotting-library versions.
- `intent-routing-evaluation.json`: expected/predicted labels, case IDs, timing and corpus hash.
- `plot_accuracy.py`: reproducible plotting source; requires matplotlib and scikit-learn.
- `dashboard-dark-synthetic.png`: previous actual browser screenshot with synthetic simulator results.

Accuracy = exact matching predicted topics and relevant subtypes / all 21 evaluated questions. Ground-truth labels were frozen in the existing test split of `backend/data/assistant-routing.json` before evaluation. These rows are excluded from retrieved examples; no exact normalized test-input duplicate was found among retrieved training rows. Private examples were disabled. No database records or model-weight training were used.

This is a small synthetic, developer-reviewed test set. It is not blind real-user accuracy, scoring/overlap accuracy, or end-to-end factual-answer accuracy. The separate 44/44 corrected regression suite remains a regression pass rate and is not substituted for this accuracy result. Rules and backend corrections are outside the measured router component.

Metric definition: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html
