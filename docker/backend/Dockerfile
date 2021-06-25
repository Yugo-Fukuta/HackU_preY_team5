FROM python:3.8

ADD requirements.txt /usr/src/app/backend/

WORKDIR /usr/src/app/backend/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --ignore-installed