#!/usr/bin/env python3
"""Fail if tommaso-cortonesi-cv.pdf exceeds the 2-page limit from SPEC."""
import sys
from pathlib import Path

from pypdf import PdfReader

MAX_PAGES = 2
PDF_PATH = Path(__file__).resolve().parent.parent / "tommaso-cortonesi-cv.pdf"


def main():
    if not PDF_PATH.exists():
        sys.exit(f"error: {PDF_PATH} not found; run `make pdf` first")
    pages = len(PdfReader(str(PDF_PATH)).pages)
    print(f"PDF pages: {pages} (limit: {MAX_PAGES})")
    if pages > MAX_PAGES:
        sys.exit(f"error: PDF exceeds {MAX_PAGES} pages")


if __name__ == "__main__":
    main()
