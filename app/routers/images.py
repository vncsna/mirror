# TODO: Add exception checking
# TODO: Use wrong uuids as input

import os
import cv2
import shutil
import numpy as np
from enum import Enum
from uuid import uuid4
from pathlib import Path
from dotenv import load_dotenv
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

load_dotenv()
DATABASE_IMGE = os.environ['DATABASE_IMGE']
DATABASE_TEXT = os.environ['DATABASE_TEXT']
HAAR_CLF_PATH = os.environ['HAAR_CLF_PATH']

CASCADE_CLASSIFIER = cv2.CascadeClassifier(HAAR_CLF_PATH)

# ---------------------------------------

class FilterName(str, Enum):
    blur = "blur"
    cover = "cover"
    pixelate = "pixelate"

# ---------------------------------------

router = APIRouter(tags=['Image'])

@router.post('/image')
def create_image(image: UploadFile = File(...)):
    uuid = uuid4()
    with open(f'{DATABASE_IMGE}/{uuid}.png', 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)
    return {'uuid': uuid}

@router.get('/image/{uuid}')
def read_image(uuid: str):
    filepath = Path(f'{DATABASE_IMGE}/{uuid}.png')
    return FileResponse(filepath)

@router.put('/image/{uuid}')
def update_image(uuid: str, image: UploadFile = File(...)):
    with open(f'{DATABASE_IMGE}/{uuid}.png', 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)
    return {'uuid': uuid}

@router.delete('/image/{uuid}')
def delete_image(uuid: str):
    filepath = Path(f'{DATABASE_IMGE}/{uuid}.png')
    filepath.unlink()
    return {'uuid': uuid}

@router.get('/image/{uuid}/{filter_}')
def transform_image(uuid: str, filter_: FilterName):
    filepath = f'{DATABASE_IMGE}/{uuid}.png'
    image = cv2.imread(str(filepath))
    
    if filter_ == FilterName.blur:
        anonymized_image = anonymize_faces(image, blur)
    elif filter_ == FilterName.cover:
        anonymized_image = anonymize_faces(image, cover)
    elif filter_ == FilterName.pixelate:
        anonymized_image = anonymize_faces(image, pixelate)
    
    new_filepath = f'{DATABASE_IMGE}/{uuid}-{filter_}.png'
    cv2.imwrite(new_filepath, anonymized_image)
    return FileResponse(new_filepath)

@router.get('/images')
def read_images():
    uuids = Path(f'{DATABASE_IMGE}').glob('*')
    uuids = [uuid.stem for uuid in uuids]
    return {'uuids': uuids}

# ---------------------------------------

def blur(img, factor=3.0):
    # auto determine the size of blurring kernel
    (h, w) = img.shape[:2]
    kW = int(w / factor)
    kH = int(h / factor)

    # ensure that width and height are odd
    kW = kW if kW % 2 != 0 else kW - 1
    kH = kH if kH % 2 != 0 else kH - 1

    # apply a gaussian blue to image
    return cv2.GaussianBlur(img, (kW, kH), 0)

def cover(img):
    return np.zeros_like(img)

def pixelate(img):
    height, width = img.shape[:2]
    
    # downscale image
    output = cv2.resize(
        img, (6, 6), interpolation=cv2.INTER_LINEAR)
    
    # upscale image
    output = cv2.resize(
        output, (width, height), interpolation=cv2.INTER_NEAREST)
    
    return output

def anonymize_faces(img, filtr):
    # transform color to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # detect region of interest with
    # a haar cascade feature classifier
    faces = CASCADE_CLASSIFIER.detectMultiScale(gray, 1.1, 4)
    
    # loop faces and apply filter
    for (x0, y0, width, height) in faces:
        face = img[x0:x0 + width, y0:y0 + height, :]
        img[x0:x0 + width, y0:y0 + height, :] = filtr(face)
    
    return img