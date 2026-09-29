import os
from pathlib import Path
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, field_validator

class Message(BaseModel):
    text: str = Field(min_length=1,max_length=5000)
    @field_validator('text')
    @classmethod
    def nonblank(cls,value):
        if not value.strip(): raise ValueError('Message cannot be blank')
        return value


def create_app(model_path=None):
    application=FastAPI(title='SMS Message Classifier',version='1.0.0')
    path=Path(model_path or os.environ.get('SMS_MODEL','results/model.joblib'))
    model=None
    @application.get('/',response_class=HTMLResponse)
    def home(): return (Path(__file__).parent/'index.html').read_text(encoding='utf-8')
    @application.post('/predict')
    def predict(message: Message):
        nonlocal model
        if model is None:
            if not path.is_file(): raise HTTPException(503,'Train the model first: python train.py')
            # Only load artifacts produced locally by this project; joblib is unsafe for untrusted files.
            model=joblib.load(path)
        label=str(model.predict([message.text])[0])
        return {'label':label,'meaning':'spam' if label=='spam' else 'legitimate message','warning':'Experimental prediction; do not use for security decisions.'}
    return application

app=create_app()
