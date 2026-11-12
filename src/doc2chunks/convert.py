from pathlib import Path

import pymupdf4llm
from docx import Document


def pdf_to_markdown(path: Path) -> str:
    """Convert a PDF file to a markdown text."""
    return str(pymupdf4llm.to_markdown(str(path)))

def docx_to_markdown(path: Path) -> str:
    """Convert a DOCX file to a markdown text."""
    doc = Document(str(path))

    lines = []
    for paragraph in doc.paragraphs:
        if (paragraph.style) and (paragraph.style.name.startswith("Heading")):
            level = int(paragraph.style.name.split()[-1])
            lines.append("#" * level + " " + paragraph.text)
        else:
            lines.append(paragraph.text)
    return "\n\n".join(lines)