#!/usr/bin/make

help:
	@echo "make"
	@echo "    install"
	@echo "        Install all packages of poetry project locally."	
	@echo "    formatter"
	@echo "        Apply black formatting to code."
	@echo "    mypy"
	@echo "        Apply type checking."
	@echo "    lint"
	@echo "        Lint code with ruff, and check if black formatter should be applied."
	@echo "    lint-watch"
	@echo "        Lint code with ruff in watch mode."
	@echo "    lint-fix"
	@echo "        Lint code with ruff and try to fix."	

install:
	cd backend/app && \
	poetry shell && \
	poetry install

formatter:
	poetry run black .

mypy:	
	poetry run mypy .

lint:
	poetry run ruff . && poetry run black --check .

lint-watch:
	poetry run ruff . --watch

lint-fix:	
	poetry run ruff . --fix
