import csv,json,tempfile,unittest
from pathlib import Path
from fastapi.testclient import TestClient
from app.data import load_dataset
from app.main import create_app
from train import train

class ClassifierTests(unittest.TestCase):
    def test_duplicates_and_conflicts(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'data.csv'
            path.write_text('label,text\nham,Meet now\nham, meet  NOW \nspam,Win prize\nham,Win prize\n')
            rows,stats=load_dataset(path)
            self.assertEqual(len(rows),1)
            self.assertEqual(stats['duplicate_rows_removed'],1)
            self.assertEqual(stats['conflicting_rows_removed'],2)
    def test_malformed_dataset_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'data.csv'
            for row in ['ham','ham,hello,unexpected']:
                path.write_text('label,text\n'+row+'\n')
                with self.assertRaises(ValueError):load_dataset(path)
    def test_missing_model_and_blank_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            client=TestClient(create_app(Path(tmp)/'absent.joblib'))
            self.assertEqual(client.post('/predict',json={'text':'hello'}).status_code,503)
            self.assertEqual(client.post('/predict',json={'text':'   '}).status_code,422)
            self.assertEqual(client.post('/predict',json={'text':'x'*5001}).status_code,422)
            self.assertEqual(client.get('/').status_code,200)
    def test_training_and_api_end_to_end(self):
        # Synthetic data tests execution only; not evidence of predictive quality.
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'data.csv';out=Path(tmp)/'results'
            with path.open('w',newline='') as stream:
                writer=csv.writer(stream);writer.writerow(['label','text'])
                for i in range(40):
                    writer.writerow(['ham',f'family meeting tomorrow number {i}'])
                    writer.writerow(['spam',f'win cash prize offer number {i}'])
            report=train(path,out)
            self.assertEqual(sum(report['split'][s] for s in ['train','validation','test']),80)
            hashes=json.loads((out/'split_hashes.json').read_text())
            self.assertFalse(set(hashes['train']) & set(hashes['test']))
            self.assertFalse(set(hashes['validation']) & set(hashes['test']))
            result=TestClient(create_app(out/'model.joblib')).post('/predict',json={'text':'family meeting tomorrow'})
            self.assertEqual(result.status_code,200)
            self.assertIn(result.json()['label'],['ham','spam'])
            self.assertTrue((out/'REPORT.md').is_file())

if __name__=='__main__': unittest.main()
