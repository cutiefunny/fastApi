FROM python:latest

WORKDIR /usr/src/fastapi

COPY ./main.py /usr/src/fastapi
COPY ./requirements.txt /usr/src/fastapi

RUN pip install -r requirements.txt

CMD uvicorn --host=0.0.0.0 --port 8000 main:app