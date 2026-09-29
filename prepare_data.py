"""Download public UCI archive and convert original records into a CSV."""
import csv,io,urllib.request,zipfile
from pathlib import Path
URL='https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip'
def prepare(archive):
    text=zipfile.ZipFile(io.BytesIO(archive)).read('SMSSpamCollection').decode('utf-8')
    Path('data').mkdir(exist_ok=True)
    with open('data/messages.csv','w',encoding='utf-8',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(['label','text'])
        for line in text.splitlines():
            if line: writer.writerow(line.split('\t',1))
if __name__=='__main__':
    with urllib.request.urlopen(URL,timeout=30) as response: prepare(response.read())
    print('Saved data/messages.csv; attribution is in DATASET.md')
