# Walkthrough
1. Read DATASET.md. Explain ham vs spam and why the data may not reflect current scams.
2. Read app/data.py. Explain deduplication before splitting and conflicting labels.
3. Read train.py. Explain TF-IDF, train/validation/test roles, majority baseline and macro-F1.
4. Inspect results/metrics.json and errors.csv. Categorize every error (up to 20) manually.
5. Run the local UI and tests. Explain why the API does not return a confidence percentage.

## Two independent changes
- Add character n-gram candidates and choose them using validation only; do not claim an unbiased new result from the already observed test set.
- Create a genuinely new, independently labeled evaluation set and record errors, class balance and limitations. Keep this set separate from training.

## Interview questions
What is data leakage? Why macro-F1 instead of accuracy? Why compare to a majority predictor? Why can two near-identical spam templates leak across splits? How does a linear SVM differ from Logistic Regression? Why is a score not necessarily a probability? What conclusions cannot be drawn from one split?

## Research report next steps
This package includes a baseline report, not a peer-reviewed paper. Add related work, human error analysis, multiple training seeds on fixed validation design, and a carefully defined new experiment under faculty guidance. Explain any novelty honestly; changing a library setting alone is not a novel contribution.
