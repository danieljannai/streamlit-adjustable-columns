# Makefile for streamlit-expandable-columns development

.PHONY: help install install-dev test test-unit test-e2e lint format clean build upload bump-patch bump-minor bump-major

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
	@echo "  bump-patch   Bump patch version and push to git"
	@echo "  bump-minor   Bump minor version and push to git"
	@echo "  bump-major   Bump major version and push to git"

install:
	pip install -e .

install-dev: frontend-install
	pip install -e ".[dev]"
	pip install -r requirements-dev.txt
	playwright install

test: frontend-build
	pytest -v -m "not e2e"

test-unit: frontend-build
	pytest -v -m "unit"

test-e2e: frontend-build
	pytest -v -m "e2e" --browser firefox --browser chromium

lint:
	flake8 streamlit_expandable_columns tests --max-line-length=88
	black --check streamlit_expandable_columns tests
	isort --check-only streamlit_expandable_columns tests

format:
	black streamlit_expandable_columns tests
	isort streamlit_expandable_columns tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf streamlit_expandable_columns/frontend/node_modules/
	rm -rf streamlit_expandable_columns/frontend/build/
	rm -rf streamlit_expandable_columns/frontend/dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python setup.py sdist bdist_wheel

upload: build
	twine upload dist/*

# Version management
bump-patch:
	bump-my-version bump patch
	git push --follow-tags

bump-minor:
	bump-my-version bump minor
	git push --follow-tags

bump-major:
	bump-my-version bump major
	git push --follow-tags

# Frontend development
frontend-install:
	cd streamlit_expandable_columns/frontend && npm install

frontend-build: frontend-install
	cd streamlit_expandable_columns/frontend && npm run build

frontend-dev:
	cd streamlit_expandable_columns/frontend && npm start 