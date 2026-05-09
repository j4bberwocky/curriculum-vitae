# TASKS — 01-init

Decomposizione del lavoro descritto in [SPEC.md](SPEC.md). I task sono ordinati per dipendenza e dimensionati a 1–2 ore l'uno.

## Scelte tecniche

Scelte non vincolate dalla SPEC, fissate qui per il piano implementativo.

1. **Linguaggio del renderer** (sia PDF che Web): **Python 3 + Jinja2 + PyYAML**. Motivazione: KISS, parsing YAML e templating in un'unica toolchain leggera, niente build system pesante.
2. **Generatore sito statico**: **template HTML/CSS scritti a mano + Jinja2**, niente SSG (no Hugo/Zola/Eleventy). Motivazione: il sito è single-page, ogni dipendenza in più è over-engineering rispetto alla SPEC.
3. **Build orchestrator locale**: **Makefile** con `make pdf`, `make site`, `make all`, `make clean`.
4. **Engine LaTeX locale**: **`tectonic`** (single binary, scarica i pacchetti on-demand, già installato sulla macchina di sviluppo). Override via env var `LATEX_ENGINE`.
5. **Compilazione LaTeX in CI**: **`xu-cheng/latex-action`** (GitHub Action che porta TeX Live, già usata in molti repo CV). Da rivalutare in T10 se conviene allineare la CI a tectonic.
6. **Deploy GitHub Pages**: **`actions/deploy-pages`** ufficiale (no branch `gh-pages`, deploy diretto da artifact).
7. **Discrepanze fra SPEC.md e CLAUDE.md** (Zola, `content/cv.yaml`, JSON Schema): la SPEC è autoritativa, CLAUDE.md va riallineato (vedi T13).

---

## T1 — MVP end-to-end ugly ma funzionante

**Descrizione**: scaffolding del repo + `cv.yaml` minimale + due renderer banali che producono PDF e sito da quel file, eseguibili in locale.

**File toccati**:
- `cv.yaml` (nuovo, contenuto minimale: 1 esperienza, 1 education, 1 skill)
- `cv-latex/render.py` (nuovo, legge yaml → `.tex` con `\documentclass{article}`, niente Awesome-CV)
- `cv-latex/template.tex.j2` (nuovo, template Jinja minimale)
- `cv-web/render.py` (nuovo, legge yaml → `index.html` senza CSS)
- `cv-web/template.html.j2` (nuovo, template Jinja minimale)
- `Makefile` (nuovo, target `pdf`, `site`, `all`, `clean`)
- `requirements.txt` (nuovo, `PyYAML`, `Jinja2`)
- `.gitignore` (aggiornato per `cv-latex/build/`, `cv-web/dist/`, `__pycache__/`, `*.aux`, `*.log`, `*.out`)

**Done**:
- `make pdf` produce `tommaso-cortonesi-cv.pdf` nella root del repo
- `make site` produce `cv-web/dist/index.html` apribile in browser con i dati di `cv.yaml`
- entrambi i comandi sono idempotenti e non lasciano artefatti spuri nella root

---

## T2 — Popolare `cv.yaml` con i dati reali

**Descrizione**: estrarre i dati dal CV esistente in `_old/Awesome_CV/resume_eng/` e portarli in `cv.yaml` rispettando la struttura della SPEC.

**File toccati**:
- `cv.yaml` (popolato con personal, summary, experiences, education, skills reali)

**Done**:
- `cv.yaml` contiene tutte le esperienze, education e skills presenti in `_old/Awesome_CV.pdf`
- date nel formato `YYYY-MM` / `YYYY` / `"present"`
- `make pdf` e `make site` continuano a funzionare con i dati reali (anche se brutti graficamente)

---

## T3 — Campo `version` e documentazione struttura

**Descrizione**: aggiungere il campo `version` (semver `major.minor.patch`) gestito a mano in `cv.yaml` e documentare la struttura attesa.

**File toccati**:
- `cv.yaml` (aggiunto `version: 0.1.0` o simile)
- `specs/01-init/DATA.md` (nuovo, breve descrizione delle sezioni e dei tipi attesi — solo prosa, niente JSON Schema)

**Done**:
- `cv.yaml` ha un campo `version` valido semver
- `DATA.md` descrive ogni sezione (`personal`, `summary`, `experiences`, `education`, `skills`, `version`) con tipi e esempi
- `DATA.md` esplicita: nessuna validazione automatica, la pipe si rompe se mancano campi attesi

---

## T4 — Integrazione template Awesome-CV nel PDF

**Descrizione**: portare class/sty/font da `_old/Awesome_CV/` in `cv-latex/` e mappare i campi YAML alle macro Awesome-CV (`\name`, `\position`, `\cventry`, `\cvskill`, ecc.).

**File toccati**:
- `cv-latex/awesome-cv.cls` (copiato da `_old/Awesome_CV/`)
- `cv-latex/fontawesome.sty` (copiato)
- `cv-latex/fonts/` (copiato)
- `cv-latex/template.tex.j2` (riscritto su base Awesome-CV)
- `cv-latex/render.py` (eventuali aggiustamenti su escaping LaTeX)

**Done**:
- il PDF generato è visivamente coerente con `_old/Awesome_CV.pdf`
- nessun warning bloccante in fase di compilazione
- il PDF apre correttamente e mostra tutti i dati di `cv.yaml`

---

## T5 — Vincolo "PDF max 2 pagine"

**Descrizione**: verificare il numero di pagine e regolare margini/font/contenuto del template fino a stare in 2 pagine con i dati reali.

**File toccati**:
- `cv-latex/template.tex.j2` (eventuali tweak su `\geometry`, font size, spacing)
- `Makefile` (target `make check-pages` opzionale che usa `pdfinfo` per contare le pagine)

**Done**:
- `pdfinfo tommaso-cortonesi-cv.pdf | grep Pages` restituisce ≤ 2
- nessun contenuto di `cv.yaml` viene tagliato per stare in 2 pagine

---

## T6 — Versione e data di build nel PDF

**Descrizione**: footer del PDF con versione (da `cv.yaml`) e data build in formato `YYYY-MM` (calcolata al render).

**File toccati**:
- `cv-latex/render.py` (legge `version`, calcola `build_date`, le passa al template)
- `cv-latex/template.tex.j2` (footer con `\fancyfoot` o equivalente Awesome-CV)

**Done**:
- in fondo a entrambe le pagine del PDF appare qualcosa come `v0.1.0 — 2026-05`
- il valore di `version` letto è esattamente quello in `cv.yaml`
- la data è quella di esecuzione di `make pdf`

---

## T7 — Sito web responsive

**Descrizione**: aggiungere CSS mobile-first al template HTML in modo che il sito sia leggibile su smartphone e desktop.

**File toccati**:
- `cv-web/template.html.j2` (struttura semantica con sezioni)
- `cv-web/static/style.css` (nuovo, CSS mobile-first con 1 media query desktop)
- `cv-web/render.py` (copia `static/` in `dist/`)

**Done**:
- il sito è leggibile a 360px e a 1280px senza overflow orizzontali
- CSS è incluso nel sito buildato e i file statici stanno in `cv-web/dist/`

---

## T8 — Versione e data di build nel sito

**Descrizione**: footer del sito con versione (da `cv.yaml`) e data build `YYYY-MM`.

**File toccati**:
- `cv-web/render.py` (passa `version` e `build_date` al template)
- `cv-web/template.html.j2` (footer con i due valori)

**Done**:
- footer del sito mostra `v0.1.0 — 2026-05`
- valori coerenti con quelli del PDF se buildati nello stesso mese

---

## T9 — Link al PDF dal sito

**Descrizione**: aggiungere link cliccabile a `tommaso-cortonesi-cv.pdf` (alla root del sito pubblicato) nel footer del sito.

**File toccati**:
- `cv-web/template.html.j2` (link `<a href="tommaso-cortonesi-cv.pdf">`)
- `Makefile` (target `make site` copia il PDF dalla root in `cv-web/dist/`)

**Done**:
- in `cv-web/dist/` accanto a `index.html` esiste `tommaso-cortonesi-cv.pdf`
- cliccando il link nel footer si apre/scarica il PDF

---

## T10 — GitHub Action: build del PDF

**Descrizione**: workflow che, su push su `main`, compila il PDF con LaTeX e committa il `tommaso-cortonesi-cv.pdf` aggiornato alla root.

**File toccati**:
- `.github/workflows/build-pdf.yml` (nuovo)

**Done**:
- push su `main` che modifica `cv.yaml` o `cv-latex/**` triggera il workflow
- il workflow committa il PDF aggiornato (via `git commit -am` con bot GitHub Actions) o lo pubblica come artifact + commit
- il PDF in repo è sempre allineato all'ultima `cv.yaml`

---

## T11 — GitHub Action: deploy sito su GitHub Pages

**Descrizione**: workflow che, su push su `main`, builda il sito e lo pubblica su GitHub Pages.

**File toccati**:
- `.github/workflows/deploy-site.yml` (nuovo, usa `actions/configure-pages`, `actions/upload-pages-artifact`, `actions/deploy-pages`)

**Done**:
- il sito è raggiungibile all'URL GitHub Pages del repo
- il sito mostra i dati dell'ultima `cv.yaml` mergiata su `main`
- il link al PDF nel footer punta al PDF deployato accanto al sito

---

## T12 — README

**Descrizione**: scrivere `README.md` che spiega cos'è il repo, come modificare il CV, come buildare in locale, link al sito pubblicato.

**File toccati**:
- `README.md` (popolato)

**Done**:
- `README.md` contiene: scopo, struttura cartelle, comandi `make pdf`/`make site`, prerequisiti (Python, pdflatex), URL del sito pubblicato, come bumpare `version`

---

## T13 — Riallineare `CLAUDE.md` alla SPEC

**Descrizione**: rimuovere da `CLAUDE.md` i riferimenti che non sono nella SPEC (Zola, `content/cv.yaml`, JSON Schema validation) e riflettere la struttura reale del repo.

**File toccati**:
- `CLAUDE.md`

**Done**:
- `CLAUDE.md` cita: `cv.yaml` alla root, pipeline LaTeX (Awesome-CV) + pipeline web statica, niente Zola, niente JSON Schema, niente validazione
- comandi documentati corrispondono al `Makefile` reale

---

## Riepilogo dipendenze

```
T1 (MVP)
 ├── T2 (dati reali) ──┐
 ├── T3 (version+DATA) ─┼── T6 (version PDF) ── T10 (CI PDF)
 ├── T4 (Awesome-CV) ──┘                              │
 │     └── T5 (2 pagine)                              │
 ├── T7 (responsive) ──┐                              │
 ├── T8 (version web) ─┼── T11 (CI Pages) ────────────┘
 └── T9 (link PDF) ────┘
T12 (README) — dopo T10/T11
T13 (CLAUDE.md) — dopo T1, raffinabile alla fine
```
