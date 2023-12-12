FROM python:3.11-alpine

LABEL Author="S-Zaur"

ENV PYTHONUNBUFFERED 1

RUN apk add build-base
RUN apk add libffi-dev
RUN apk add firefox

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

RUN mkdir /app

RUN mkdir /var/lib/zaurcloud

WORKDIR /app

COPY ./app /app
