FROM python:3.11-alpine

LABEL Author="S-Zaur"

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

RUN mkdir /app

WORKDIR /app

COPY ./app /app

RUN apk add firefox

RUN adduser -D user

USER user
