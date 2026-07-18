FROM python:3.12-alpine AS base

RUN mkdir -p /usr/src/app
RUN mkdir -p /output
WORKDIR /usr/src/app

RUN pip install --no-cache-dir setuptools build

COPY telegramer /usr/src/app/telegramer
COPY setup.py /usr/src/app/setup.py
COPY LICENSE /usr/src/app/LICENSE

RUN python setup.py bdist_egg && python -m build
