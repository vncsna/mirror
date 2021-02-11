FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt /opt/app/requirements.txt

WORKDIR /opt/app

RUN pip install -r requirements.txt

COPY ./app /opt/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
