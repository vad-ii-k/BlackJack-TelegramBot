FROM python:3.11-alpine
ENV BOT_NAME=$BOT_NAME

WORKDIR /usr/src/app/"${BOT_NAME:-tg_bot}"

# Installing curl for poetry
RUN apk -U add curl

# Installing poetry
RUN curl -sSL https://install.python-poetry.org | python
ENV PATH=/root/.local/bin:$PATH

# Installing project dependencies from pyproject.toml
RUN python -m venv /venv
ENV PATH=/venv/bin:$PATH \
    VIRTUAL_ENV=/venv
COPY pyproject.toml ./
# Will install into the /venv virtualenv
RUN poetry install --no-root
