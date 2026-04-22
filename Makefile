PYTHON ?= python3
ENNEGRAM_CLI ?= ennegram_cli.py
ENNEGRAM_TARGET_ROOT ?= /Users/kostadis.roussos/Documents/CampaignGenerator
ENNEGRAM_DATA_ROOT ?= /Users/kostadis.roussos/Documents/EnnegramData/CampaignGenerator
ENNEGRAM_WIKI_ROOT ?=
QUERY ?= architecture
MAX_RESULTS ?= 3
ENTRY_ID ?= architecture
VERDICT ?= partial
NOTE ?= Needs update
SOURCE_URI ?=
WIKI_ENTRY ?= caveats
TITLE ?=
TAIL ?= 20
EVENT_TYPE ?=
IMPORT_FILE ?=
MARK_SYNCED ?=

.PHONY: en-help en-init en-ingest en-recall en_r en-code en-validate en-correct en-promote en-memory-log en-sync-mempalace

en-help:
	@echo "Ennegram helper targets"
	@echo "  ENNEGRAM_TARGET_ROOT='$(ENNEGRAM_TARGET_ROOT)'"
	@echo "  ENNEGRAM_DATA_ROOT='$(ENNEGRAM_DATA_ROOT)'"
	@echo "  ENNEGRAM_WIKI_ROOT='$(ENNEGRAM_WIKI_ROOT)' (optional; defaults to <data-root>/wiki)"
	@echo "  make en-init"
	@echo "  make en-ingest"
	@echo "  make en-recall QUERY='auth caveats' [MAX_RESULTS=5]"
	@echo "  make en_r QUERY='auth caveats' [MAX_RESULTS=5]"
	@echo "  make en-code QUERY='where is chunking implemented' [MAX_RESULTS=5]"
	@echo "  make en-validate"
	@echo "  make en-correct ENTRY_ID=architecture VERDICT=partial NOTE='Missing caveat' [SOURCE_URI='ennegram/wiki/architecture.md']"
	@echo "  make en-promote WIKI_ENTRY=caveats NOTE='What I found' [TITLE='Chunking finding'] [SOURCE_URI='SESSION_DOC_PIPELINE.md']"
	@echo "  make en-memory-log [TAIL=20] [EVENT_TYPE=recall]"
	@echo "  make en-sync-mempalace [IMPORT_FILE='ennegram/reports/pulled.json'] [MARK_SYNCED=1]"

en-init:
	@if [ -n "$(ENNEGRAM_WIKI_ROOT)" ]; then \
		ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) init --data-root "$(ENNEGRAM_DATA_ROOT)" --wiki-root "$(ENNEGRAM_WIKI_ROOT)"; \
	else \
		ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) init --data-root "$(ENNEGRAM_DATA_ROOT)"; \
	fi

en-ingest:
	ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) ingest

en-recall:
	ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) recall "$(QUERY)" --max-results $(MAX_RESULTS)

en_r:
	ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) r "$(QUERY)" --max-results $(MAX_RESULTS)

en-code:
	ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) r "$(QUERY)" --mode code --max-results $(MAX_RESULTS)

en-validate:
	ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) validate

en-correct:
	@if [ -n "$(SOURCE_URI)" ]; then \
		ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) correct "$(ENTRY_ID)" --verdict "$(VERDICT)" --note "$(NOTE)" --source-uri "$(SOURCE_URI)"; \
	else \
		ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) correct "$(ENTRY_ID)" --verdict "$(VERDICT)" --note "$(NOTE)"; \
	fi

en-promote:
	@if [ -n "$(TITLE)" ] && [ -n "$(SOURCE_URI)" ]; then \
		ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) promote "$(WIKI_ENTRY)" --note "$(NOTE)" --title "$(TITLE)" --source-uri "$(SOURCE_URI)"; \
	elif [ -n "$(TITLE)" ]; then \
		ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) promote "$(WIKI_ENTRY)" --note "$(NOTE)" --title "$(TITLE)"; \
	elif [ -n "$(SOURCE_URI)" ]; then \
		ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) promote "$(WIKI_ENTRY)" --note "$(NOTE)" --source-uri "$(SOURCE_URI)"; \
	else \
		ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) promote "$(WIKI_ENTRY)" --note "$(NOTE)"; \
	fi

en-memory-log:
	@if [ -n "$(EVENT_TYPE)" ]; then \
		ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) memory-log --tail $(TAIL) --event-type "$(EVENT_TYPE)"; \
	else \
		ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) memory-log --tail $(TAIL); \
	fi

en-sync-mempalace:
	@if [ -n "$(IMPORT_FILE)" ] && [ -n "$(MARK_SYNCED)" ]; then \
		ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) sync-mempalace --import-file "$(IMPORT_FILE)" --mark-synced; \
	elif [ -n "$(IMPORT_FILE)" ]; then \
		ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) sync-mempalace --import-file "$(IMPORT_FILE)"; \
	elif [ -n "$(MARK_SYNCED)" ]; then \
		ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) sync-mempalace --mark-synced; \
	else \
		ENNEGRAM_TARGET_ROOT="$(ENNEGRAM_TARGET_ROOT)" $(PYTHON) $(ENNEGRAM_CLI) sync-mempalace; \
	fi
