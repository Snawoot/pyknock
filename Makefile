PYTHON = python
VENVMOD = virtualenv
RM = rm

PRJ_DIR = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
VENV ?= $(PRJ_DIR)venv

install: $(VENV) setup.py
	$(VENV)/bin/pip install -U .

$(VENV):
	$(PYTHON) -m $(VENVMOD) $(VENV)
	$(VENV)/bin/pip install -U wheel

uninstall: $(VENV)
	$(VENV)/bin/pip uninstall -y pyknock

clean:
	$(RM) -rf $(VENV)

pkg:
	$(PYTHON) setup.py sdist bdist_wheel
