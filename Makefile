# setup virtual environment for simulation

VENV_NAME := ../.dj_sim
VENV_ACTIVATE := $(VENV_NAME)/bin/activate

.PHONY: setup activate install run all

setup:
	python3 -m virtualenv $(VENV_NAME)

activate:
	@echo "Run 'source $(VENV_NAME)/bin/activate' to activate the virtual environment."

install:
	. $(VENV_ACTIVATE) && pip install -r requirements.txt

run:
	. $(VENV_ACTIVATE) && python manage.py runserver

migrate:
	python manage.py makemigrations && python manage.py migrate

all: setup install
	@echo "Run 'make activate' and 'source $(VENV_NAME)/bin/activate' to activate the virtual environment."
