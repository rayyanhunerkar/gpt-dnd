SHELL := /bin/sh

VENV?=venv
ENV?=dev
BIN ?= $(VENV)/bin
PYTHON ?= $(BIN)/python
BASE_DIR = candidate-server
MESSAGE?=Migrating
API?=api
#include .env

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

#.PHONY: venv
#venv: ## Make a new virtual environment
#	python3 -m venv $(VENV) && source $(BIN)/activate && exec bash
#
#.PHONY: install
#install: ## Make venv and install requirements
#	$(BIN)/pip install -r requirements.txt

make-migrate: ## Generate migration files
	alembic revision --autogenerate -m '$(MESSAGE)'

migrate: ## runs the migrations
	alembic upgrade head

docker-make-migrate: ## generate migrations for docker
	docker exec -it $(API) alembic revision --autogenerate -m '$(MESSAGE)'

docker-migrate: ## runs the migrations for docker
	docker exec -it $(API) alembic upgrade head

docker-migrate-base-downgrade: ## runs the migrations for docker
	docker exec -it $(API) alembic downgrade base

up-build: ## builds the dockerfile and ups the services
	docker-compose up -d --build

e2e-up: ## ups the docker services
	docker-compose up -d

api-up: ## ups the api service
	docker-composer up -d $(API)

test-async: ## tests asynchronously
	docker exec -it api coverage run --concurrency=greenlet tests --test

teardown: ## tearsdown the docker services
	docker-compose down
