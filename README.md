# Curriculum Vitae

Repository per gestire il mio CV con [`cv.yaml`](cv.yaml) come single source of truth e due target di build:

- **PDF** (LaTeX) → [`tommaso-cortonesi-cv.pdf`](tommaso-cortonesi-cv.pdf) alla root
- **Sito web statico** → `cv-web/dist/` (in futuro pubblicato su GitHub Pages)

Specifica funzionale: [`specs/01-init/SPEC.md`](specs/01-init/SPEC.md). Piano di lavoro: [`specs/01-init/TASKS.md`](specs/01-init/TASKS.md).

## Stato

**T1 (MVP) completato.** Pipeline end-to-end funzionante ma volutamente brutta: template `article` LaTeX di base e HTML senza CSS. Awesome-CV, sito responsive, footer con versione/data e GitHub Actions arrivano nei task successivi.

## Struttura

```text
cv.yaml                      # single source of truth
cv-latex/                    # renderer + template per il PDF
  render.py
  template.tex.j2
cv-web/                      # renderer + template per il sito
  render.py
  template.html.j2
specs/                       # specifiche e piani di lavoro
Makefile                     # orchestratore dei build
requirements.txt             # PyYAML, Jinja2
tommaso-cortonesi-cv.pdf     # output PDF (versionato)
```

## Prerequisiti

- Python 3 (testato su 3.13)
- [`tectonic`](https://tectonic-typesetting.github.io/) — engine LaTeX di default, single binary che scarica i pacchetti on-demand:

  ```sh
  brew install tectonic
  ```

  Per usare un altro engine (`pdflatex`, `xelatex`, ...) basta avere il binario in PATH e impostare `LATEX_ENGINE` (vedi sotto).

## Build locale

Tutti i comandi creano automaticamente un virtualenv `.venv/` al primo invocazione e installano le dipendenze.

```sh
make all      # PDF + sito
make pdf      # solo PDF -> tommaso-cortonesi-cv.pdf
make site     # solo sito -> cv-web/dist/index.html
make clean    # rimuove build artifacts
make distclean# rimuove anche .venv
```

Per usare un engine LaTeX diverso da `tectonic`:

```sh
LATEX_ENGINE=pdflatex make pdf
```

## Modificare il CV

Il contenuto vive interamente in [`cv.yaml`](cv.yaml). La struttura attesa è descritta nella SPEC; non c'è validazione, se mancano campi attesi il render fallisce.
