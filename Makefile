.PHONY: build install up exec ps down pysen test
#################################################################################
# GLOBALS                                                                       #
#################################################################################

# コンテナ内から実行されたらRUN_CONTEXT変数を空で宣言し、それ以外はコンテナにアクセスする
ifeq ($(IN_CONTAINER), true)
	RUN_CONTEXT :=
else
	RUN_CONTEXT := docker-compose exec sub
endif

# 便利
ARG =
#################################################################################
# DOCKER-COMMAND                                                                #
#################################################################################
ps:
	docker-compose ps

build:
	docker-compose build $(ARG)

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

exec:
	docker-compose exec sub bash

logs:
	docker-compose logs $(ARG)

build-prod:
	docker build --platform linux/amd64 -f Dockerfile.prod . -t $(ARG)

up-prod:
	docker run -itd --name rag_prod $(ARG)
	docker exec -it rag_prod bash

install:
	$(RUN_CONTEXT) poetry install

install-cpu:
	$(RUN_CONTEXT) poetry install --with cpu

own:
	$(RUN_CONTEXT) poetry install --only-root

#################################################################################
# SCRIPT-COMMANDS                                                               #
#################################################################################
# どう使うかはちょっと検討
DEBUG =-m pdb

test:
	poetry run pytest

fix: ruff-fix black

ruff-fix:
	poetry run ruff --fix .

black:
	poetry run black .

lint: black-check ruff-check mypy

ruff-check:
	poetry run ruff check .

black-check:
	poetry run black --check .

mypy:
	poetry run mypy . --config-file ./pyproject.toml
