FROM python:3.11.4-alpine

WORKDIR /usr/src/app/bj_21_bot

ENV PATH=/venv/bin:/root/.local/bin:$PATH
ENV VIRTUAL_ENV=/venv

RUN apk --no-cache add curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apk del curl && \
    python -m venv /venv

COPY . .

RUN poetry install --no-interaction --no-ansi --no-root --without=dev
