from pathlib import Path

from doc2chunks.convert import pdf_to_markdown

FIXTURES = Path(__file__).parent/"fixtures"


def test_pdf_to_markdown_contains_text() -> None:
    markdown =  pdf_to_markdown(FIXTURES/"sample.pdf")
    assert "Hello doc2chunks" in markdown