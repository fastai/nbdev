FROM python:3.6-slim-stretch

COPY . /
RUN pip install packaging
RUN pip install -e .