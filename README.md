# SMS Message Classifier

Release 1.0 within its documented scope. See [release and operating notes](RELEASE.md).
A Python portfolio experiment comparing Logistic Regression and Linear SVM, with unigram/bigram TF-IDF features, on the public UCI SMS Spam Collection. Includes a browser demo, inference API, tests, and measured results.

## Run (Python 3.11+)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python prepare_data.py
python train.py
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```
Open http://127.0.0.1:8001 or /docs. Example inputs: "Can we meet tomorrow afternoon?" and "Congratulations! Claim your cash prize now." Predictions are observations, not guarantees.

## Evaluation, not just a demo
Normalized exact duplicates are removed before stratified splitting. Groups with conflicting labels are dropped. Split: 70% training, 15% validation, 15% held-out test, seed 42. TF-IDF learns vocabulary only within fitted training pipelines. Model/feature choice uses validation macro-F1; the selected pipeline is refitted on train+validation and tested once. A majority-class baseline demonstrates why accuracy alone can mislead on imbalanced data.

Read results/REPORT.md, metrics.json, errors.csv, and split_hashes.json. Re-running with different versions can slightly change results. Do not repeatedly tune against the test results; use a fresh holdout for new experiments.

## Tests
```bash
python -m unittest discover -s tests -v
```
Integration tests use synthetic messages only to test execution. Published metrics use the real UCI dataset downloaded with prepare_data.py.

## Limitations and safe use
Not original research, not a security product, not an LLM. Older English SMS does not represent current scams. Near-duplicate templates may remain even after exact deduplication. No multilingual evaluation or statistical-significance claim. API has no authentication/rate limiting: run locally only. No confidence score is returned because an SVM margin is not a calibrated probability. Never load someone else's joblib model; serialized artifacts can execute code. Retrain the model locally instead.

## Dataset and evaluation
See DATASET.md for dataset attribution and STUDENT_GUIDE.md for the implementation walkthrough. Manual error categorization and broader evaluation remain future work.
