#!/usr/bin/env python3
"""T1 MVP: render cv.yaml -> tommaso-cortonesi-cv.pdf using basic LaTeX."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

REPO_ROOT = Path(__file__).resolve().parent.parent
LATEX_DIR = Path(__file__).resolve().parent
BUILD_DIR = LATEX_DIR / "build"
CV_YAML = REPO_ROOT / "cv.yaml"
OUTPUT_PDF = REPO_ROOT / "tommaso-cortonesi-cv.pdf"
ENGINE = os.environ.get("LATEX_ENGINE", "tectonic")


def latex_escape(value):
    if value is None:
        return ""
    s = str(value)
    s = (
        s.replace("\\", r"\textbackslash{}")
        .replace("&", r"\&")
        .replace("%", r"\%")
        .replace("$", r"\$")
        .replace("#", r"\#")
        .replace("_", r"\_")
        .replace("{", r"\{")
        .replace("}", r"\}")
        .replace("~", r"\textasciitilde{}")
        .replace("^", r"\textasciicircum{}")
    )
    return s.replace("—", "---").replace("–", "--")


def main():
    if shutil.which(ENGINE) is None:
        sys.exit(
            f"error: '{ENGINE}' non trovato in PATH; installa tectonic "
            "(`brew install tectonic`) oppure imposta LATEX_ENGINE su un altro engine"
        )

    data = yaml.safe_load(CV_YAML.read_text())

    env = Environment(
        loader=FileSystemLoader(str(LATEX_DIR)),
        variable_start_string="<<",
        variable_end_string=">>",
        block_start_string="<%",
        block_end_string="%>",
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
        keep_trailing_newline=True,
    )
    env.filters["e"] = latex_escape

    template = env.get_template("template.tex.j2")
    rendered = template.render(**data)

    BUILD_DIR.mkdir(exist_ok=True)
    tex_path = BUILD_DIR / "cv.tex"
    tex_path.write_text(rendered)

    engine_name = Path(ENGINE).name
    if engine_name == "tectonic":
        cmd = [ENGINE, "-c", "minimal", "cv.tex"]
    else:
        cmd = [ENGINE, "-interaction=nonstopmode", "-halt-on-error", "cv.tex"]
    result = subprocess.run(cmd, cwd=BUILD_DIR)
    if result.returncode != 0:
        sys.exit(f"error: {ENGINE} ha fallito (rc={result.returncode})")

    shutil.copy2(BUILD_DIR / "cv.pdf", OUTPUT_PDF)
    print(f"OK: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
