"""Select a model on validation data; evaluate only that model on held-out test data."""
import argparse, csv, hashlib, json, platform
from pathlib import Path
import joblib
import numpy as np
import sklearn
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, f1_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from app.data import load_dataset


def train(data_path, out_dir):
    rows, stats=load_dataset(data_path)
    labels=[r['label'] for r in rows]
    train_rows, holdout=train_test_split(rows,test_size=.30,random_state=42,stratify=labels)
    validation,test=train_test_split(holdout,test_size=.5,random_state=42,stratify=[r['label'] for r in holdout])
    assert not ({r['key'] for r in train_rows} & {r['key'] for r in validation+test})
    assert not ({r['key'] for r in validation} & {r['key'] for r in test})
    x_train=[r['text'] for r in train_rows];y_train=[r['label'] for r in train_rows]
    x_val=[r['text'] for r in validation];y_val=[r['label'] for r in validation]
    candidates={};scores={}
    for name, model in [('logistic',LogisticRegression(max_iter=1000,random_state=42)),('svm',LinearSVC(random_state=42))]:
        for ngrams in [(1,1),(1,2)]:
            key=f'{name}_ngrams_{ngrams[1]}'
            pipe=Pipeline([('tfidf',TfidfVectorizer(ngram_range=ngrams,min_df=2,max_features=20000)),('classifier',model)])
            pipe.fit(x_train,y_train)
            candidates[key]=pipe
            scores[key]=float(f1_score(y_val,pipe.predict(x_val),average='macro'))
    selected=max(scores,key=scores.get)
    # Refit selected pipeline on train+validation before the one final evaluation.
    final=candidates[selected]
    combined=train_rows+validation
    final.fit([r['text'] for r in combined],[r['label'] for r in combined])
    x_test=[r['text'] for r in test];y_test=[r['label'] for r in test]
    prediction=final.predict(x_test)
    baseline=DummyClassifier(strategy='most_frequent').fit(np.zeros((len(combined),1)),[r['label'] for r in combined])
    baseline_pred=baseline.predict(np.zeros((len(test),1)))
    report={'dataset':stats,'split':{'train':len(train_rows),'validation':len(validation),'test':len(test),'seed':42},
        'versions':{'python':platform.python_version(),'sklearn':sklearn.__version__},
        'dataset_sha256':hashlib.sha256(Path(data_path).read_bytes()).hexdigest(),
        'validation_macro_f1':scores,'selected_model':selected,
        'test_macro_f1':float(f1_score(y_test,prediction,average='macro')),
        'test_accuracy':float(accuracy_score(y_test,prediction)),
        'majority_baseline_macro_f1':float(f1_score(y_test,baseline_pred,average='macro')),
        'classification_report':classification_report(y_test,prediction,output_dict=True,zero_division=0),
        'confusion_matrix_labels':['ham','spam'],'confusion_matrix':confusion_matrix(y_test,prediction,labels=['ham','spam']).tolist(),
        'limitations':['Old English-language SMS dataset; not representative of current scams or support tickets.', 'Normalized exact duplicates removed; near-duplicate template leakage can remain.', 'One split seed; do not infer statistical significance.', 'This is a benchmark prototype, not a security product.']}
    out=Path(out_dir);out.mkdir(parents=True,exist_ok=True)
    joblib.dump(final,out/'model.joblib')
    (out/'metrics.json').write_text(json.dumps(report,indent=2))
    errors=[{'actual':row['label'],'predicted':str(pred),'text':row['text']} for row,pred in zip(test,prediction) if row['label'] != pred]
    with (out/'errors.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=['actual','predicted','text']);writer.writeheader();writer.writerows(errors)
    # Persist membership hashes so split disjointness can be audited without exposing messages.
    membership={name:[hashlib.sha256(row['key'].encode()).hexdigest() for row in group] for name,group in [('train',train_rows),('validation',validation),('test',test)]}
    (out/'split_hashes.json').write_text(json.dumps(membership,indent=2))
    lines=['# Experimental report: SMS classification','', 'This is a reproducible baseline experiment, not an original research paper.','',
        f"Selected on validation data: **{selected}**.",f"Held-out macro-F1: **{report['test_macro_f1']:.4f}**; accuracy: **{report['test_accuracy']:.4f}**.",
        f"Majority baseline macro-F1: **{report['majority_baseline_macro_f1']:.4f}**.",'','## Validation comparisons','', '| Candidate | Macro-F1 |','|---|---|']
    lines.extend(f'| {name} | {score:.4f} |' for name,score in scores.items())
    lines.extend(['','## Method','Normalized exact-text duplicates and conflicting labels are removed before a stratified 70/15/15 split. TF-IDF is fitted only inside the training pipeline. Four candidates are compared on validation macro-F1. The winner is refitted on train+validation, then tested once. See metrics.json for class-level results and confusion matrix.','','## Error review',f'{len(errors)} incorrect predictions are in errors.csv. Review every error (up to 20), assigning observed failure categories; this human analysis has not been completed by the student.','','## Limitations']+report['limitations']+['','## Dataset citation','Almeida, T. & Hidalgo, J. (2011). SMS Spam Collection. UCI Machine Learning Repository. https://doi.org/10.24432/C5CC84. Dataset licensed CC BY 4.0 per UCI.'])
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n')
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--data',default='data/messages.csv');parser.add_argument('--output',default='results')
    args=parser.parse_args();print(json.dumps(train(args.data,args.output),indent=2))
