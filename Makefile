.PHONY: run install clean

VENV_DIR ?= .env
PYTHON = python
REQUIREMENTS = requirements.txt

export FLASK_APP=main.py

run:
	clear
	$(VENV_DIR)/bin/$(PYTHON) -m flask run --host=0.0.0.0

init:
	clear
	rm -rf $(VENV_DIR)
	@$(MAKE) $(VENV_DIR)
	dropdb --if-exists restless
	createdb restless
	psql restless < restless.db

clean:
	find . -iname "*.pyc" -delete
	find . -iname "*.pyo" -delete
	find . -iname "__pycache__" -delete

pep8:
	clear
	$(VENV_DIR)/bin/flake8 main.py

$(VENV_DIR):
	virtualenv $(VENV_DIR)
	if [ -a $(REQUIREMENTS) ] ; \
	then \
		$(VENV_DIR)/bin/pip install -r requirements.txt ; \
	else \
		$(VENV_DIR)/bin/pip install flake8 ; \
		$(VENV_DIR)/bin/pip freeze > requirements.txt ; \
	fi;
