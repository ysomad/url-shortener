FROM python:3.9.6-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY app/ requirements.txt /usr/src/app/

# install dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc libc-dev python3-dev default-libmysqlclient-dev

RUN pip install --no-cache-dir -r ./requirements.txt
