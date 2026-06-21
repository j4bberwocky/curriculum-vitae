# CLAUDE.md

Guida per assistenti AI che lavorano su questo repository.

## Cosa è

CV gestito con [`cv.yaml`](cv.yaml) **alla root** come single source of truth. Da quel file si generano due output indipendenti:

- **PDF** in stile Awesome-CV → `tommaso-cortonesi-cv.pdf` alla root (versionato).
- **Sito statico responsive** → `cv-web/dist/` (deploy GitHub Pages).

## Stack

- **Python 3** (Jinja2 + PyYAML + pypdf) per il rendering. Niente Hugo/Zola/Eleventy: i template HTML sono scritti a mano.
- **tectonic** come engine LaTeX di default (override via env var `LATEX_ENGINE`). Bundle remoto, nessuna installazione TeX Live.
- **Awesome-CV class** vendored in `cv-latex/awesome-cv.cls` (versione 2015 con patch — vedi sotto).
- **Toolchain via `mise`** (`mise.toml`): mise gestisce python 3.13 + `uv`; `uv` gestisce le dipendenze (`pyproject.toml` + `uv.lock`). I target Make eseguono `uv sync` al primo run (crea la `.venv/`). `tectonic` NON è gestito da mise (brew in locale, curl in CI).

Schema dati (contratto di `cv.yaml`): [`DATA.md`](DATA.md) alla root. La spec funzionale originale e il piano di lavoro storico T1–T13 non sono più nell'albero: vivono nella git history (rimossi nel consolidamento `specs/`).

## Convenzioni e vincoli

- **Niente validazione dello YAML**: scelta esplicita della SPEC. Se manca un campo atteso, il render fallisce. Non aggiungere JSON Schema o validator.
- **PDF ≤ 2 pagine**: vincolo della SPEC enforced da `make check-pages` (script `cv-latex/check_pages.py` con `pypdf`). `make all` lo chiama dopo `make pdf`.
- **Date** in `cv.yaml`: `YYYY-MM`, `YYYY`, o `"present"`. Passate come stringhe ai template, niente parsing.
- **Profilo solo software architect, solo inglese, no foto, no info di contatto sensibili pubblicate**. Per nascondere un campo (es. `email`, `phone`) senza perderne il valore: commentarlo nello YAML. I template usano `{% if %}` su tutti i campi opzionali. Convenzione in [DATA.md](DATA.md#convenzione-commenta-per-non-pubblicare).
- **`version` in `cv.yaml`** (semver, manuale): patch = typo, minor = nuova esperienza/certificazione, major = repositioning. Footer di PDF e sito mostrano `v{version} — {YYYY-MM}` con la data di build calcolata al render.

## Build commands

```sh
make all          # pdf + check-pages + site
make pdf          # tommaso-cortonesi-cv.pdf alla root
make site         # cv-web/dist/ (incluso copia del PDF dentro dist/)
make check-pages  # fail se PDF > 2 pagine
make test         # unit test dei renderer (pytest)
make clean        # rimuove build artifacts
make distclean    # rimuove anche .venv/
```

## Layout del repo

```
.github/workflows/
  build-deploy.yml            # pipeline unica: test + build PDF + commit + deploy sito
cv-latex/
  fonts/                      # Roboto + Source Sans Pro
  awesome-cv.cls              # vendored 2015, PATCHATO (vedi sotto)
  check_pages.py
  fontawesome.sty             # vendored, legacy
  render.py                   # YAML → cv.tex → PDF (subprocess su tectonic)
  template.tex.j2             # Jinja con delimitatori CUSTOM: << >> e <% %>
cv-web/
  static/
    style.css                 # mobile-first, 1 media query @720px
  render.py                   # YAML → index.html + copia static/ in dist/
  template.html.j2            # Jinja default delimitatori {{ }} e {% %}
tests/                        # unit test dei renderer (pytest)
CLAUDE.md                     # questa guida
cv.yaml                       # SoT
DATA.md                       # schema/contratto di cv.yaml (no validazione)
Makefile
mise.toml                     # toolchain: python + uv
pyproject.toml                # dipendenze Python (+ dev: pytest)
README.md
tommaso-cortonesi-cv.pdf      # output PDF (versionato)
uv.lock                       # lockfile delle dipendenze
```

## Gotcha — `awesome-cv.cls`

Il cls vendored proviene da `_old/Awesome_CV/` (versione 2015 v1.3) ed è **patchato** con tre fix backportati dall'upstream:

1. `\acvSectionContentTopSkip` — referenziato e mai definito → aggiunto come `\newcommand`.
2. `\paragraphstyle` — originale prendeva un argomento ma `cvparagraph` lo invoca senza; ridefinito come style switch senza argomento.
3. `\setbool{istart}` → `\setbool{isstart}` (7 occorrenze) — typo originale del cls Awesome-CV, latente finché `\@mobile` o `\@email` erano definiti.

Se vuoi aggiornare il cls alla master upstream, attenzione: usa `fontawesome6` che **non è nel bundle di tectonic**. Restando sul cls 2015 patchato continuiamo a usare `fontawesome` (legacy) che è disponibile.

## Gotcha — delimitatori Jinja in LaTeX

`cv-latex/template.tex.j2` usa delimitatori **custom**: `<< var >>` per espressioni e `<% block %>` per blocchi. Motivo: LaTeX usa `{` e `}` ovunque, i delimitatori default di Jinja (`{{ }}`, `{% %}`) collidono. Il template HTML usa invece i default Jinja.

## Gotcha — `LATEX_ENGINE`

Default `tectonic`. La CLI di tectonic è diversa da pdflatex: `render.py` ha un branch su `Path(ENGINE).name == "tectonic"`. Se aggiungi un nuovo engine, allinea il branch.

## Memory hygiene

La memoria persistente in `~/.claude/projects/.../memory/` contiene un `project_context.md` che potrebbe essere vecchio. Stato attuale: `cv.yaml` alla root, Python+Jinja per il sito (no Zola), nessuna validazione, toolchain mise+uv, CI in un workflow unico (`build-deploy.yml`), schema in `DATA.md` alla root (cartella `specs/` rimossa, storia in git).
