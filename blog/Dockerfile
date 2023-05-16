FROM python:3.10-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -yqq --no-install-recommends gcc g++ file python3-dev musl-dev libffi-dev libev-dev zip curl libjpeg-dev && \
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        ~/.cache/pip/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

RUN pip install --upgrade pip setuptools wheel

WORKDIR /code/
ENV PYTHONPATH /code/
COPY . /code/


RUN python3 -m venv venv
RUN . venv/bin/activate
RUN pip install -r requirements/dev_local.txt
