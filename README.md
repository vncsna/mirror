## mirror

Minor API experiment for data anonymization, providing blurring (pixelating) faces and name replacement. I've developed this project to understand some commands of FastAPI and SQLite.

## usage

- `git clone`
- `cd mirror/app`
- `uvicorn main:app --reload`
- open `localhost:8000/docs`

## docker

`docker build -t mirror .`
`docker run -d --name wonderland -p 80:80 mirror`
- open `localhost/docs`
