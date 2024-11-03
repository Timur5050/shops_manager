FROM python:3.12-alpine3.18
LABEL maintainer="stukantimur811@gmail.com"

ENV PYTHONDONTWRITEBYCODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /APP

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .