# Struttura di `cv.yaml`

Documento descrittivo della forma attesa del file [`cv.yaml`](cv.yaml). **Non è uno schema formale**: non c'è validazione automatica, se manca un campo atteso o cambia tipo i renderer in [`cv-latex/`](cv-latex/) e [`cv-web/`](cv-web/) si rompono — scelta esplicita ("YAGNI/KISS, niente validazione").

Le sezioni di primo livello sono sei: `personal`, `summary`, `experiences`, `education`, `skills`, `version`.

## `personal` (oggetto)

Dati anagrafici e di contatto. I campi sono tutti opzionali, ma quelli omessi vanno gestiti dai template (al momento `name`, `title`, `email` sono usati, gli altri verranno inseriti man mano).

| Campo      | Tipo   | Esempio                              |
|------------|--------|--------------------------------------|
| `name`     | string | `Tommaso Cortonesi`                  |
| `title`    | string | `Solution Architect`                 |
| `email`    | string | `tommaso.cortonesi@gmail.com`        |
| `phone`    | string | `+39 328 8731860`                    |
| `linkedin` | string | `linkedin.com/in/tommaso-cortonesi`  |
| `github`   | string | `github.com/j4bberwocky`             |
| `website`  | string | `www.example.com`                    |

## `summary` (string)

Paragrafo di apertura. In YAML usare il block scalar `>` per scrivere il testo su più righe e farlo collassare in un unico paragrafo:

```yaml
summary: >
  Solution Architect with a background in Java and AWS...
```

## `experiences` (lista di oggetti)

Esperienze lavorative ordinate dalla più recente alla più vecchia.

| Campo              | Tipo              | Note                                       |
|--------------------|-------------------|--------------------------------------------|
| `company`          | string            | nome azienda o azienda — progetto          |
| `role`             | string            | ruolo ricoperto                            |
| `location`         | string            | città, paese                               |
| `start_date`       | data (vedi sotto) |                                            |
| `end_date`         | data o `present`  |                                            |
| `summary`          | string            | **opzionale** — riga introduttiva (sotto)  |
| `responsibilities` | lista di string   | bullet points                              |

Il campo `summary` è opzionale: una frase breve di contesto sul ruolo, renderizzata in corsivo sopra i `responsibilities` (nel PDF e nel sito). Se assente viene saltata (i template usano `{% if %}`). Per nasconderla senza perderne il valore vale la stessa [convenzione "commenta per non pubblicare"](#convenzione-commenta-per-non-pubblicare). Usare il block scalar `>` per scriverla su più righe.

Esempio:

```yaml
experiences:
  - company: CCH Tagetik
    role: Lead Application & Product Architect
    location: Lucca, Italy
    start_date: 2025
    end_date: present
    summary: >        # opzionale
      One-line context about the role and its scope.
    responsibilities:
      - Architectural Design: ...
      - Technical Leadership: ...
```

## `education` (lista di oggetti)

Titoli di studio e certificazioni. Stesso schema, ordinato dal più recente.

| Campo         | Tipo   | Note                                         |
|---------------|--------|----------------------------------------------|
| `institution` | string | università o ente certificatore              |
| `degree`      | string | titolo o nome certificazione                  |
| `date`        | data   | una sola data (anno o anno-mese)             |

## `skills` (lista di oggetti)

Competenze raggruppate per topic.

| Campo         | Tipo   | Esempio                                  |
|---------------|--------|------------------------------------------|
| `topic`       | string | `Programming Languages`                  |
| `description` | string | `Java, Go, Python (basic)`               |

## `version` (string)

Versione del **contenuto** del CV (non del software che lo genera). Formato semver `major.minor.patch`, gestita a mano. Convenzione che applichiamo:

- **patch**: typo, riformulazioni, piccoli aggiornamenti di skill o tecnologie.
- **minor**: nuova esperienza, nuova certificazione, summary riscritto.
- **major**: cambio sostanziale di posizionamento (es. shift di carriera).

Compare nel footer del PDF e del sito insieme alla data di build in formato `YYYY-MM`.

```yaml
version: 0.1.0
```

## Formato delle date

Per ogni campo data sono ammessi:

- `YYYY-MM` — es. `2023-09`
- `YYYY` — es. `2010`
- `present` — solo come `end_date` di un'esperienza in corso

I valori vengono passati ai template come stringhe e renderizzati così come sono. Non c'è parsing né validazione, la responsabilità del formato è sull'autore del file.

## Note operative

- I caratteri unicode "—" (em-dash) e "–" (en-dash) sono mappati dal renderer LaTeX a `---` / `--` — possono essere usati liberamente nei valori.
- I caratteri speciali LaTeX (`& % $ # _ { } ~ ^ \\`) sono escaped automaticamente dal filtro `latex_escape`.
- I valori HTML sono auto-escaped da Jinja, quindi entità come `&` vengono trasformate in `&amp;`.
- Niente markup nei valori (no markdown, no HTML inline): i renderer trattano tutto come testo.

## Convenzione "commenta per non pubblicare"

Per togliere un campo dall'output (PDF e sito) senza perderne il valore, basta commentarlo nello YAML:

```yaml
personal:
  name: Tommaso Cortonesi
  # email: tommaso.cortonesi@gmail.com   # unpublished
  # phone: +39 328 8731860               # unpublished
  linkedin: linkedin.com/in/tommaso-cortonesi
```

I renderer trattano i campi opzionali con un `{% if %}` Jinja, quindi un campo assente viene saltato senza errori. Per rimetterlo in vita: si tolgono i `#`. Vale per qualsiasi campo `personal.*` opzionale (`email`, `phone`, `linkedin`, `github`, `website`, ...).
