# TODO: Add exception checking
# TODO: Use wrong uuids as input

import os
import nltk
import sqlite3
from uuid import uuid4
from dotenv import load_dotenv
from fastapi import APIRouter, File, UploadFile
from nltk.tokenize.treebank import TreebankWordDetokenizer

load_dotenv()
DATABASE_IMGE = os.environ['DATABASE_IMGE']
DATABASE_TEXT = os.environ['DATABASE_TEXT']

# ---------------------------------------

router = APIRouter(tags=['Text'])

@router.post('/text')
def create_text(corpus: str):
    uuid = str(uuid4())
    with sqlite3.connect(DATABASE_TEXT) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO texts 
            VALUES (?, ?)''', (uuid, corpus, ))
        conn.commit()
    return {'uuid': uuid}

@router.get('/text/{uuid}')
def read_text(uuid: str):
    with sqlite3.connect(DATABASE_TEXT) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT corpus 
            FROM texts 
            WHERE text_id=?''', (uuid, ))
        corpus = cursor.fetchone()
        conn.commit()
    return {'corpus': corpus}

@router.put('/text/{uuid}')
def update_text(uuid: str, corpus:str = None):
    with sqlite3.connect(DATABASE_TEXT) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE texts 
            SET corpus=? 
            WHERE text_id=?''', (corpus, uuid))
        conn.commit()
    return {'uuid': uuid}

@router.delete('/text/{uuid}')
def delete_text(uuid: str):
    with sqlite3.connect(DATABASE_TEXT) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM texts 
            WHERE text_id=?''', (uuid, ))
        conn.commit()
    return {'uuid': uuid}

@router.get('/text/{uuid}/transform')
def transform_text(uuid: str):
    with sqlite3.connect(DATABASE_TEXT) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT corpus 
            FROM texts 
            WHERE text_id=?''', (uuid, ))
        corpus = cursor.fetchone()
        conn.commit()
    anonymized_corpus = anonymize_proper_noun(corpus[0])
    return {'corpus': anonymized_corpus}

@router.get('/texts')
def read_texts():
    with sqlite3.connect(DATABASE_TEXT) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * 
            FROM texts''')
        corpora = cursor.fetchall()
        conn.commit()
    return {'corpora': corpora}

# ---------------------------------------

def anonymize_proper_noun(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    new_tokens = [
        word if pos != 'NNP' else '<NNP>'
        for word, pos in tagged
    ]
    detokenizer = TreebankWordDetokenizer()
    return detokenizer.detokenize(new_tokens)