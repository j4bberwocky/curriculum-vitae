VENV ?= .venv
PYTHON := $(VENV)/bin/python

.PHONY: all pdf site check-pages test install clean distclean

all: pdf check-pages site

test: $(PYTHON)
	$(PYTHON) -m pytest -q

pdf: $(PYTHON)
	$(PYTHON) cv-latex/render.py

site: $(PYTHON)
	$(PYTHON) cv-web/render.py
	@if [ -f tommaso-cortonesi-cv.pdf ]; then \
		cp tommaso-cortonesi-cv.pdf cv-web/dist/; \
		echo "  copied tommaso-cortonesi-cv.pdf to cv-web/dist/"; \
	else \
		echo "  WARN: tommaso-cortonesi-cv.pdf not found at repo root; site link will 404 until you run make pdf"; \
	fi

check-pages: $(PYTHON)
	$(PYTHON) cv-latex/check_pages.py

install: $(PYTHON)

$(PYTHON): pyproject.toml
	uv sync
	@touch $(PYTHON)

clean:
	rm -rf cv-latex/build cv-web/dist
	rm -f tommaso-cortonesi-cv.pdf

distclean: clean
	rm -rf $(VENV)
