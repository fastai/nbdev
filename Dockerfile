FROM python:3.6-slim-stretch

RUN pip install packaging
RUN pip install -e .