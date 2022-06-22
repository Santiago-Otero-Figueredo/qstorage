FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /qstorage

WORKDIR /qstorage

COPY . .
COPY secrets.docker.json secrets.json

RUN pip3 install -r requirements/base.pip

EXPOSE 8000

CMD /qstorage/start.sh