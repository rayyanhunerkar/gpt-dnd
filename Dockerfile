# syntax = docker/dockerfile

FROM python:3.11-slim-buster as builder
ENV POETRY_VERSION=1.2.2
WORKDIR /builder
COPY poetry.lock /builder/
COPY pyproject.toml /builder/
RUN apt update && \
    apt install \
    curl \
    gcc \
    libpq-dev -y \
    && pip install "poetry==$POETRY_VERSION"\
    && python -m venv /venv
RUN poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin

FROM python:3.11-slim-buster as app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt update && apt install libpq-dev -y
RUN pip install alembic coverage
COPY --from=builder /venv/lib/python3.11/site-packages/  /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY . /app/
