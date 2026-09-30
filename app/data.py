"""Deduplicate normalized text before stratified splitting."""
import csv
import re
from collections import defaultdict

def normalize(text): return re.sub(r"\s+", " ", text.strip().lower())

def load_dataset(path):
    groups=defaultdict(list)
    with open(path,encoding='utf-8',newline='') as stream:
        reader=csv.DictReader(stream)
        if reader.fieldnames != ['label','text']:
            raise ValueError('CSV columns must be label,text')
        total=0
        for row in reader:
            total+=1
            if set(row) != {'label','text'} or not isinstance(row.get('text'),str) or row['label'] not in {'ham','spam'} or not normalize(row['text']):
                raise ValueError('Each row needs a ham/spam label and nonempty text')
            groups[normalize(row['text'])].append(row)
    rows=[]; conflicts=0
    for key, values in groups.items():
        if len({v['label'] for v in values}) > 1:
            conflicts += len(values)
            continue
        rows.append({'text':values[0]['text'],'label':values[0]['label'],'key':key})
    rows.sort(key=lambda row:row['key'])
    return rows, {'original_rows':total,'unique_rows':len(rows),'conflicting_rows_removed':conflicts,'duplicate_rows_removed':total-len(rows)-conflicts}
