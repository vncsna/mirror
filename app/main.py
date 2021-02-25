import os
import sqlite3
from pathlib import Path
from fastapi import FastAPI
from dotenv import load_dotenv
from routers import texts, images

load_dotenv()
DATABASE_IMGE = os.environ['DATABASE_IMGE']
DATABASE_TEXT = os.environ['DATABASE_TEXT']

app = FastAPI(
    title='Mirror (World)',
    description='''
    Minor API experiment for data anonymization,
    providing blurring (pixelating) faces and name tagging.'''
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

# ---------------------------------------

# Create image folder
Path(DATABASE_IMGE).mkdir(parents=True, exist_ok=True)

# Create database
with sqlite3.connect(DATABASE_TEXT) as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS texts 
        (text_id TEXT PRIMARY KEY, corpus TEXT NOT NULL)''')
    conn.commit()