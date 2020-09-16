FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN groupadd -r -g 2000 mygrp && useradd -u 2000 -r -g mygrp myuser

COPY app .

USER myuser

CMD [ "python", "./main_async.py" ]