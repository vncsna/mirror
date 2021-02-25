import os
import shutil
from uuid import uuid4
from pathlib import Path
from dotenv import load_dotenv
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

load_dotenv()
DATABASE_IMGE = os.environ['DATABASE_IMGE']
DATABASE_TEXT = os.environ['DATABASE_TEXT']

router = APIRouter(tags=['Image'])

# ---------------------------------------

@router.post('/image')
def create_image(image: UploadFile = File(...)):
    uuid = uuid4()
    with open(f'database/uuid.png', 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)
    return {'id': uuid}

@router.get('/image/{uuid}')
def read_image(uuid: str):
    return FileResponse(f'./database/uuid.png')

@router.put('/image/{uuid}')
def update_image(uuid: str):
    pass

@router.delete('/image/{uuid}')
def delete_image(uuid: str):
    imagepath = Path(f'./database/uuid.png')
    imagepath.unlink()
    return {'id': id}

# ---------------------------------------

@router.get('/image/{uuid}/{method}')
def transform_image(uuid: str, method:str):
    pass

# ---------------------------------------

@router.get('/images')
def read_images():
    pass

# ---------------------------------------

def blur(img, factor=3.0):
    # auto determine the size of blurring kernel
    (h, w) = image.shape[:2]
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

def visualize(img):
    return Image.fromarray(img, mode='RGB')

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
    
    # transform color space to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    return img