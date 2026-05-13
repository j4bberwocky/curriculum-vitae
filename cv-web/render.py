#!/usr/bin/env python3
"""Render cv.yaml -> cv-web/dist/index.html and copy static assets."""
import shutil
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

REPO_ROOT = Path(__file__).resolve().parent.parent
WEB_DIR = Path(__file__).resolve().parent
STATIC_DIR = WEB_DIR / "static"
DIST_DIR = WEB_DIR / "dist"
CV_YAML = REPO_ROOT / "cv.yaml"


def main():
    data = yaml.safe_load(CV_YAML.read_text())

    env = Environment(
        loader=FileSystemLoader(str(WEB_DIR)),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=True,
    )

    template = env.get_template("template.html.j2")
    rendered = template.render(**data)

    DIST_DIR.mkdir(exist_ok=True)
    if STATIC_DIR.is_dir():
        for item in STATIC_DIR.iterdir():
            target = DIST_DIR / item.name
            if item.is_dir():
                shutil.copytree(item, target, dirs_exist_ok=True)
            else:
                shutil.copy2(item, target)

    output = DIST_DIR / "index.html"
    output.write_text(rendered)
    print(f"OK: {output}")


if __name__ == "__main__":
    main()
