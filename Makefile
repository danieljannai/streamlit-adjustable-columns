# Makefile for streamlit-expandable-columns development

.PHONY: help install install-dev test test-unit test-e2e lint format clean build upload

help:
	@echo "Available commands:"
	@echo "  install      Install package for production"
	@echo "  install-dev  Install package for development with all dependencies"
	@echo "  test         Run all tests"
	@echo "  test-unit    Run unit tests only"
	@echo "  test-e2e     Run end-to-end tests only"
	@echo "  lint         Run linting checks"
	@echo "  format       Format code with black and isort"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build package"
	@echo "  upload       Upload package to PyPI"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pip install -r requirements-dev.txt
	playwright install

test:
	pytest -v -m "not e2e"

test-unit:
	pytest -v -m "unit"

test-e2e:
	pytest -v -m "e2e" --browser firefox --browser chromium

lint:
	# flake8 streamlit_expandable_columns tests
	black --check streamlit_expandable_columns tests
	isort --check-only streamlit_expandable_columns tests

format:
	black streamlit_expandable_columns tests
	isort streamlit_expandable_columns tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python setup.py sdist bdist_wheel

upload: build
	twine upload dist/*

# Frontend development
frontend-install:
	cd streamlit_expandable_columns/frontend && npm install

frontend-build:
	cd streamlit_expandable_columns/frontend && npm run build

frontend-dev:
	cd streamlit_expandable_columns/frontend && npm start 