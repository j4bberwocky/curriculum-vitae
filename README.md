# Curriculum Vitae

Repository per gestire il mio CV. Single source of truth: [`cv.yaml`](cv.yaml). Due target di build automatici:

- **PDF** in stile Awesome-CV → [`tommaso-cortonesi-cv.pdf`](tommaso-cortonesi-cv.pdf) alla root (versionato)
- **Sito web statico** responsive → pubblicato su GitHub Pages

Schema dati (contratto di `cv.yaml`): [`DATA.md`](DATA.md).

## Struttura

```text
.github/workflows/
  build-deploy.yml           # CI: pipeline unica (test + build PDF + deploy sito)
cv-latex/                    # renderer + template Awesome-CV per il PDF
  fonts/                     # Roboto + Source Sans Pro
  awesome-cv.cls             # vendored, patchato (vedi CLAUDE.md)
  check_pages.py             # guard "max 2 pagine"
  fontawesome.sty            # vendored, legacy
  render.py
  template.tex.j2
cv-web/                      # renderer + template per il sito
  static/
    style.css                # CSS mobile-first
  render.py
  template.html.j2
tests/                       # unit test dei renderer (pytest)
CLAUDE.md                    # guida per assistenti AI
cv.yaml                      # single source of truth
DATA.md                      # schema/contratto di cv.yaml (no validazione)
Makefile                     # orchestratore dei build
mise.toml                    # toolchain: python + uv
pyproject.toml               # dipendenze Python (PyYAML, Jinja2, pypdf) + dev (pytest)
README.md                    # questo file
tommaso-cortonesi-cv.pdf     # output PDF (versionato)
uv.lock                      # lockfile delle dipendenze
```

## Prerequisiti

- [`mise`](https://mise.jdx.dev/) — gestisce la toolchain Python (python 3.13 + `uv`). Da `mise.toml`:

  ```sh
  mise install   # installa python + uv
  ```

- [`tectonic`](https://tectonic-typesetting.github.io/) — engine LaTeX di default, single binary che scarica i pacchetti on-demand (non gestito da mise):

  ```sh
  brew install tectonic
  ```

  Per usare un altro engine (`pdflatex`, `xelatex`, ...) basta averlo in PATH e impostare `LATEX_ENGINE`, es. `LATEX_ENGINE=pdflatex make pdf`.

## Build locale

I target Make sincronizzano le dipendenze con `uv sync` (crea la `.venv/` e installa da `pyproject.toml` / `uv.lock`) alla prima invocazione.

```sh
make all         # PDF + check pagine + sito (catena completa)
make pdf         # solo PDF -> tommaso-cortonesi-cv.pdf alla root
make site        # solo sito -> cv-web/dist/ (copia anche il PDF dentro dist/)
make check-pages # verifica che il PDF non superi 2 pagine
make test        # unit test dei renderer (pytest)
make clean       # rimuove cv-latex/build, cv-web/dist, tommaso-cortonesi-cv.pdf
make distclean   # rimuove anche .venv/
```

Per anteprima del sito in locale:

```sh
cd cv-web/dist && python3 -m http.server 8000
# poi apri http://127.0.0.1:8000/
```

## Modificare il CV

Il contenuto vive interamente in [`cv.yaml`](cv.yaml); la struttura attesa è in [`DATA.md`](DATA.md). Niente validazione: se manca un campo atteso, la build si rompe (scelta esplicita).

**Bump della versione**: campo `version` in fondo a `cv.yaml`, semver `major.minor.patch`. Convenzione: patch = typo/riformulazioni, minor = nuova esperienza/certificazione, major = repositioning. La versione compare nel footer del PDF e del sito accanto alla data di build (`YYYY-MM`).

**Nascondere un campo dall'output** (es. email, phone) senza perderne il valore: commentarlo nello YAML. Convenzione documentata in [DATA.md](DATA.md#convenzione-commenta-per-non-pubblicare).

## CI / Pubblicazione

Un unico workflow su `main`: [`.github/workflows/build-deploy.yml`](.github/workflows/build-deploy.yml). Su cambi a `cv.yaml`, `cv-latex/**`, `cv-web/**` o alla toolchain esegue una pipeline sequenziale nello stesso run:

1. ricompila il PDF con tectonic e lo committa indietro alla root (con `[skip ci]` per evitare loop, dato che il PDF non è tra i path trigger);
2. builda il sito (che include il PDF appena rigenerato) e fa deploy su GitHub Pages via `actions/deploy-pages`.

Pipeline unica = il sito pubblica sempre il PDF della revisione corrente (niente race tra workflow separati).

Setup repository richiesto una sola volta:

- **Settings → Actions → Workflow permissions**: "Read and write permissions" (perché il workflow committa il PDF rigenerato indietro alla root).
- **Settings → Pages → Source**: "GitHub Actions".

Sito pubblicato: `https://j4bberwocky.github.io/curriculum-vitae/` (attivo dopo il primo deploy verde).
