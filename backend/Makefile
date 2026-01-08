# Backend Makefile
# Usage: make <target>

.PHONY: help start test setup clean logs

PYTHON = .venv\Scripts\python.exe
PIP = .venv\Scripts\pip.exe
FLASK = .venv\Scripts\flask.exe

help:
	@echo Backend API - Available Commands
	@echo ===============================
	@echo.
	@echo   make start          - Start Flask server
	@echo   make test           - Test canvas processor
	@echo   make setup          - Setup virtual environment
	@echo   make clean          - Clean temporary files
	@echo   make install        - Install dependencies
	@echo   make logs           - Show recent logs
	@echo.

start:
	@echo Starting Flask server on http://localhost:8080
	@if not exist .venv (echo Error: Virtual environment not found. Run 'make setup' first. && exit 1)
	set FLASK_APP=app && set FLASK_ENV=development && $(FLASK) run --port 8080

test:
	@echo Testing canvas processor...
	@if not exist .venv (echo Error: Virtual environment not found. Run 'make setup' first. && exit 1)
	$(PYTHON) app\canvas_processor.py ..\test-photos\boba.jpg 20

setup:
	@echo Setting up virtual environment...
	@if exist .venv (echo Virtual environment already exists) else (python -m venv .venv)
	@echo Installing dependencies...
	$(PIP) install -r requirements.txt
	@echo Setup complete!

install:
	@echo Installing/updating dependencies...
	@if not exist .venv (echo Error: Virtual environment not found. Run 'make setup' first. && exit 1)
	$(PIP) install -r requirements.txt

clean:
	@echo Cleaning temporary files...
	@if exist temp rmdir /s /q temp
	@if exist output rmdir /s /q output
	@if exist __pycache__ rmdir /s /q __pycache__
	@if exist app\__pycache__ rmdir /s /q app\__pycache__
	@echo Clean complete!

logs:
	@echo Recent backend activity:
	@if exist logs type logs\*.log

# Development shortcuts
dev: start
s: start
t: test

