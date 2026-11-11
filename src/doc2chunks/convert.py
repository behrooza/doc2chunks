from pathlib import Path

import pymupdf4llm


def pdf_to_markdown(path: Path) -> str:
    """Convert a PDF file to a markdown text."""
    return str(pymupdf4llm.to_markdown(str(path)))
