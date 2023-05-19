# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system
RUN pipenv install
COPY . /code/
