"""Unit test degli helper puri del renderer LaTeX (`cv-latex/render.py`).

`render.py` non è un package importabile (è uno script con delimitatori e un
`main()` guardato da `__main__`); lo carico per path con importlib così evito
sia il name-collision con `cv-web/render.py` sia l'esecuzione di `main()`.
"""
import importlib.util
from pathlib import Path

_RENDER_PATH = Path(__file__).resolve().parent.parent / "cv-latex" / "render.py"
_spec = importlib.util.spec_from_file_location("cv_latex_render", _RENDER_PATH)
render = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(render)


# --- latex_escape -----------------------------------------------------------

def test_latex_escape_none_is_empty():
    assert render.latex_escape(None) == ""


def test_latex_escape_special_chars():
    assert render.latex_escape("R&D 50% _x_ #1 $5") == r"R\&D 50\% \_x\_ \#1 \$5"


def test_latex_escape_dashes_mapped():
    assert render.latex_escape("2020—present") == "2020---present"
    assert render.latex_escape("pp. 10–20") == "pp. 10--20"


def test_latex_escape_coerces_non_string():
    assert render.latex_escape(2025) == "2025"


def test_latex_escape_plain_text_untouched():
    assert render.latex_escape("Solution Architect") == "Solution Architect"


# --- enrich_personal --------------------------------------------------------

def test_enrich_personal_splits_name():
    p = render.enrich_personal({"name": "Tommaso Cortonesi"})
    assert p["first_name"] == "Tommaso"
    assert p["last_name"] == "Cortonesi"


def test_enrich_personal_derives_handles():
    p = render.enrich_personal({
        "linkedin": "linkedin.com/in/tommaso-cortonesi",
        "github": "github.com/j4bberwocky",
    })
    assert p["linkedin_user"] == "tommaso-cortonesi"
    assert p["github_user"] == "j4bberwocky"


def test_enrich_personal_single_word_name():
    p = render.enrich_personal({"name": "Mononym"})
    assert p["first_name"] == "Mononym"
    assert p["last_name"] == ""


def test_enrich_personal_omits_handles_when_absent():
    p = render.enrich_personal({"name": "Tommaso Cortonesi"})
    assert "linkedin_user" not in p
    assert "github_user" not in p


def test_enrich_personal_none_input():
    p = render.enrich_personal(None)
    assert p["first_name"] == ""
    assert p["last_name"] == ""
