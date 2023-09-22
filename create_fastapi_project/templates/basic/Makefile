#!/usr/bin/make

include .env

help:
	@echo "make"
	@echo "    install"
	@echo "        Install all packages of poetry project locally."
	@echo "    run-app"
	@echo "        Run app locally without docker."
	@echo "    run-dev-build"
	@echo "        Run development docker compose and force build containers."
	@echo "    run-dev"
	@echo "        Run development docker compose."
	@echo "    stop-dev"
	@echo "        Stop development docker compose."
	@echo "    run-prod"
	@echo "        Run production docker compose."
	@echo "    stop-prod"
	@echo "        Run production docker compose."	
	@echo "    formatter"
	@echo "        Apply black formatting to code."
	@echo "    mypy"
	@echo "        Check typing."		
	@echo "    lint"
	@echo "        Lint code with ruff, and check if black formatter should be applied."
	@echo "    lint-watch"
	@echo "        Lint code with ruff in watch mode."
	@echo "    lint-fix"
	@echo "        Lint code with ruff and try to fix."	
	
install:
	cd backend/app && poetry install && cd ..

run-app:
	cd backend/app && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 && cd ..


run-dev-build:
	docker compose -f docker-compose-dev.yml up --build

run-dev:
	docker compose -f docker-compose-dev.yml up

stop-dev:
	docker compose -f docker-compose-dev.yml down

run-prod:
	docker compose up --build

stop-prod:
	docker compose down

formatter:
	cd backend/app && \
	poetry run black app

mypy:
	cd backend/app && \
	poetry run mypy .

lint:
	cd backend/app && \
	poetry run ruff app && poetry run black --check app

lint-watch:
	cd backend/app && \
	poetry run ruff app --watch

lint-fix:
	cd backend/app && \
	poetry run ruff app --fix
