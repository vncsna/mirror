import os
import sqlite3
from uuid import uuid4
from dotenv import load_dotenv
from fastapi import APIRouter, File, UploadFile

load_dotenv()
DATABASE_PATH = os.environ['DATABASE_PATH']
DATABASE_SQLT = os.environ['DATABASE_SQLT']

router = APIRouter(tags=['Text'])

# ---------------------------------------

@router.post('/text')
def create_text(text: str):
    text_id = str(uuid4())
    conn = sqlite3.connect(DATABASE_URI)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO texts VALUES (?, ?)', (text_id, text, ))
    conn.commit()
    conn.close()
    return {'text_id': text_id}

@router.get('/text/{text_id}')
def read_text(text_id:str):
    conn = sqlite3.connect(DATABASE_URI)
    cursor = conn.cursor()
    cursor.execute('SELECT corpus FROM texts WHERE text_id=?', (text_id, ))
    conn.commit()
    conn.close()
    return {'text_id': text_id}

@router.put('/text/{id}')
def update_text():
    pass

@router.delete('/text/{id}')
def delete_text():
    pass

# ---------------------------------------

@router.get('/text/{id}/transform')
def transform_text():
    pass

# ---------------------------------------

@router.get('/texts')
def read_texts():
    conn = sqlite3.connect(DATABASE_URI)
    cursor = conn.cursor()
    rows = [row for row in cursor.execute('SELECT * FROM texts')]
    cursor.execute('SELECT * FROM texts')
    conn.commit()
    conn.close()
    return rows