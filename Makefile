PYTHON   := $(HOME)/workspace/venv/bin/python
MQL      := $(HOME)/.local/bin/mql
DB_DIR   := $(CURDIR)/db
SCHEMA   := schema/vendergood.mql
CORPUS   := corpus/sentences.jsonl

.PHONY: all load reload query test clean-db help

all: help

help:
	@echo "Vendergood Emdros targets:"
	@echo "  make load     — apply schema + load corpus (first run)"
	@echo "  make reload   — drop database, reapply schema, reload corpus"
	@echo "  make test     — run loader smoke tests"
	@echo "  make query CONSTRAINT='root_2 <> \"\"'"
	@echo "               — SELECT + GET FEATURES query"

load: $(DB_DIR)/vendergood

$(DB_DIR)/vendergood: $(SCHEMA) $(CORPUS)
	@mkdir -p $(DB_DIR)
	cd $(DB_DIR) && $(MQL) -b 3 ../$(SCHEMA)
	cd $(DB_DIR) && $(PYTHON) ../tools/load_corpus.py | $(MQL) -b 3 > /dev/null
	@echo "Database loaded: $(DB_DIR)/vendergood"

reload: clean-db load

clean-db:
	rm -f $(DB_DIR)/vendergood

test:
	$(PYTHON) -m pytest tools/tests/test_load.py -q

query:
ifndef CONSTRAINT
	$(error CONSTRAINT is required: make query CONSTRAINT='mood_suffix = "alt"')
endif
	$(PYTHON) tools/query.py $(CONSTRAINT)
