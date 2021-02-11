# TODO: Add faces recognition support

import os
import shutil
from uuid import uuid4
from pathlib import Path
from dotenv import load_dotenv
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

load_dotenv()
DATABASE_PATH = os.environ['DATABASE_PATH']
DATABASE_SQLT = os.environ['DATABASE_SQLT']

router = APIRouter(tags=['Image'])

# ---------------------------------------

@router.post('/image')
def create_image(image: UploadFile = File(...)):
  id = uuid4()
  with open(f'database/{id}.png', 'wb') as buffer:
    shutil.copyfileobj(image.file, buffer)
  return {'id': image_id}

@router.get('/image/{id}')
def read_image(id: str):
  return FileResponse(f'./database/{id}.png')

@router.put('/image/{id}')
def update_image(id: str):
  pass

@router.delete('/image/{id}')
def delete_image(id: str):
  imagepath = Path(f'./database/{id}.png')
  imagepath.unlink()
  return {'id': id}

# ---------------------------------------

@router.get('/image/{id}/{method}')
def transform_image(id: str, method:str):
  pass

# ---------------------------------------

@router.get('/images')
def read_images():
  pass