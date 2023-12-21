FROM python:3.11.2-bullseye

# global settings
WORKDIR /app
ENV LANG=C.UTF-8

# application setings
# Makefileのコマンドをハンドリングする
ENV IN_CONTAINER=true
ENV PYTHONIOENCODING "utf-8"
# ENV PYTHONUNBUFFERED 1

RUN apt update -y && apt upgrade -y \
  && apt-get install --no-install-recommends -y curl tmux iputils-ping dnsutils

# install poetry
ENV POETRY_HOME=/etc/poetry
ENV PATH="${POETRY_HOME}/bin:${PATH}"
ENV POETRY_VERSION=1.4.2
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1
RUN curl -sSL https://install.python-poetry.org | python3 -
# 依存関係のインストール
COPY pyproject.toml* poetry.lock* ./
RUN poetry install --no-root
# 本体のインストール
COPY . /app
RUN poetry install --only-root

CMD ["python", "server.py"]
