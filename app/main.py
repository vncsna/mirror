import os
from pathlib import Path
from fastapi import FastAPI
from dotenv import load_dotenv
from routers import texts, images

load_dotenv()
DATABASE_PATH = os.environ['DATABASE_PATH']
DATABASE_SQLT = os.environ['DATABASE_SQLT']

app = FastAPI(
    title='Mirror (World)',
    description='''
    Minor API experiment for data anonymization,
    providing blurring (pixelating) faces and name replacement.'''
)

app.include_router(texts.router)
app.include_router(images.router)

@app.get('/', tags=['Root'])
def read_root():
    return {'message': 'Welcome to Mirror World!! Please acess /docs'}

@app.post('/clean', tags=['Root'])
def clean_database():
    datapath = Path('./database/')
    for filepath in datapath.rglob('*'):
        filepath.unlink()
    return {'status': 'done'}