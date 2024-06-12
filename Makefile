# source .dj_sim/bin/activate

VENV_NAME := .dj_sim
VENV_ACTIVATE := $(VENV_NAME)/bin/activate

.PHONY: setup activate install

setup:
	python3 -m virtualenv ../$(VENV_NAME)
activate:
	source $(VENV_ACTIVATE)
install:
	# source $(VENV_ACTIVATE);
	pip install -r requirements.txt

all: setup activate install
