# EUDI Standards Graph
#   make start    serve the page and open it in the browser
#   make refresh  fetch the public issues (needs gh) and rebuild site/graph.json
#   make serve    serve the page without opening a browser
#   make stop     stop a server left running on PORT
 
PORT ?= 8000
URL  := http://localhost:$(PORT)/
PY   := $(shell command -v python3 2>/dev/null || command -v python)
 
# Opens the browser from WSL, macOS or Linux, whichever is available
OPEN := $(shell command -v wslview || command -v explorer.exe || command -v open || command -v xdg-open)
 
.DEFAULT_GOAL := help
.PHONY: help start serve refresh stop
 
help:
	@grep -E '^#   make' Makefile | sed 's/^#   //'
 
start: site/graph.json
	@echo "Serving $(URL)  (Ctrl+C to stop)"
	@( sleep 1; $(OPEN) "$(URL)" >/dev/null 2>&1 || echo "Open $(URL) in your browser" ) &
	@$(PY) -m http.server $(PORT) --directory site
 
serve: site/graph.json
	@echo "Serving $(URL)  (Ctrl+C to stop)"
	@$(PY) -m http.server $(PORT) --directory site
 
site/graph.json:
	@$(MAKE) refresh
 
refresh:
	bash scripts/refresh.sh
 
stop:
	-@pkill -f "http.server $(PORT)" && echo "Stopped" || echo "Nothing running on $(PORT)"
 