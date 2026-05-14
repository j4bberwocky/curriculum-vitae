# Curriculum Vitae

Repository per gestire il mio CV. Single source of truth: [`cv.yaml`](cv.yaml). Due target di build automatici:

- **PDF** in stile Awesome-CV → [`tommaso-cortonesi-cv.pdf`](tommaso-cortonesi-cv.pdf) alla root (versionato)
- **Sito web statico** responsive → pubblicato su GitHub Pages

Specifica funzionale: [`specs/01-init/SPEC.md`](specs/01-init/SPEC.md). Schema dati: [`specs/01-init/DATA.md`](specs/01-init/DATA.md). Piano di lavoro: [`specs/01-init/TASKS.md`](specs/01-init/TASKS.md).

## Struttura

```text
cv.yaml                      # single source of truth
cv-latex/                    # renderer + template Awesome-CV per il PDF
  render.py
  template.tex.j2
  check_pages.py             # guard "max 2 pagine"
  awesome-cv.cls             # vendored, patchato (vedi DATA.md / TASKS.md T4)
  fontawesome.sty
  fonts/
cv-web/                      # renderer + template per il sito
  render.py
  template.html.j2
  static/style.css           # CSS mobile-first
specs/                       # specifiche e piani di lavoro
.github/workflows/           # CI: build PDF + deploy sito
Makefile                     # orchestratore dei build
requirements.txt             # PyYAML, Jinja2, pypdf
tommaso-cortonesi-cv.pdf     # output PDF (versionato)
```

## Prerequisiti

- Python 3 (testato su 3.13)
- [`tectonic`](https://tectonic-typesetting.github.io/) — engine LaTeX di default, single binary che scarica i pacchetti on-demand:

  ```sh
  brew install tectonic
  ```

  Per usare un altro engine (`pdflatex`, `xelatex`, ...) basta averlo in PATH e impostare `LATEX_ENGINE`, es. `LATEX_ENGINE=pdflatex make pdf`.

## Build locale

I target Make creano automaticamente un virtualenv `.venv/` alla prima invocazione e installano le dipendenze.

```sh
make all         # PDF + check pagine + sito (catena completa)
make pdf         # solo PDF -> tommaso-cortonesi-cv.pdf alla root
make site        # solo sito -> cv-web/dist/ (copia anche il PDF dentro dist/)
make check-pages # verifica che il PDF non superi 2 pagine
make clean       # rimuove cv-latex/build, cv-web/dist, tommaso-cortonesi-cv.pdf
make distclean   # rimuove anche .venv/
```

Per anteprima del sito in locale:

```sh
cd cv-web/dist && python3 -m http.server 8000
# poi apri http://127.0.0.1:8000/
```

## Modificare il CV

Il contenuto vive interamente in [`cv.yaml`](cv.yaml); la struttura attesa è in [`specs/01-init/DATA.md`](specs/01-init/DATA.md). Niente validazione: se manca un campo atteso, la build si rompe (scelta esplicita della SPEC).

**Bump della versione**: campo `version` in fondo a `cv.yaml`, semver `major.minor.patch`. Convenzione: patch = typo/riformulazioni, minor = nuova esperienza/certificazione, major = repositioning. La versione compare nel footer del PDF e del sito accanto alla data di build (`YYYY-MM`).

**Nascondere un campo dall'output** (es. email, phone) senza perderne il valore: commentarlo nello YAML. Convenzione documentata in [DATA.md](specs/01-init/DATA.md#convenzione-commenta-per-non-pubblicare).

## CI / Pubblicazione

Due workflow su `main`:

- [`.github/workflows/build-pdf.yml`](.github/workflows/build-pdf.yml) — su cambi a `cv.yaml` o `cv-latex/**` ricompila il PDF con tectonic e lo committa indietro alla root (con `[skip ci]` per evitare loop).
- [`.github/workflows/deploy-site.yml`](.github/workflows/deploy-site.yml) — su cambi a `cv.yaml`, `cv-web/**` o al PDF builda il sito e fa deploy su GitHub Pages via `actions/deploy-pages`.

Setup repository richiesto una sola volta:

- **Settings → Actions → Workflow permissions**: "Read and write permissions" (perché build-pdf committa il PDF indietro).
- **Settings → Pages → Source**: "GitHub Actions".

Sito pubblicato: `https://j4bberwocky.github.io/curriculum-vitae/` (attivo dopo il primo deploy verde).
