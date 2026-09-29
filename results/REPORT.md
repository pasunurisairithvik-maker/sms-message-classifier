# Experimental report: SMS classification

This is a reproducible baseline experiment, not an original research paper.

Selected on validation data: **svm_ngrams_2**.
Held-out macro-F1: **0.9662**; accuracy: **0.9858**.
Majority baseline macro-F1: **0.4669**.

## Validation comparisons

| Candidate | Macro-F1 |
|---|---|
| logistic_ngrams_1 | 0.8815 |
| logistic_ngrams_2 | 0.8731 |
| svm_ngrams_1 | 0.9388 |
| svm_ngrams_2 | 0.9560 |

## Method
Normalized exact-text duplicates and conflicting labels are removed before a stratified 70/15/15 split. TF-IDF is fitted only inside the training pipeline. Four candidates are compared on validation macro-F1. The winner is refitted on train+validation, then tested once. See metrics.json for class-level results and confusion matrix.

## Error review
11 incorrect predictions are in errors.csv. Review every error (up to 20), assigning observed failure categories; this human analysis has not been completed by the student.

## Limitations
Old English-language SMS dataset; not representative of current scams or support tickets.
Normalized exact duplicates removed; near-duplicate template leakage can remain.
One split seed; do not infer statistical significance.
This is a benchmark prototype, not a security product.

## Dataset citation
Almeida, T. & Hidalgo, J. (2011). SMS Spam Collection. UCI Machine Learning Repository. https://doi.org/10.24432/C5CC84. Dataset licensed CC BY 4.0 per UCI.
