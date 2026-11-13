from pathlib import Path

from fastapi.testclient import TestClient

from doc2chunks.api import app

client = TestClient(app)
FIXTURES = Path(__file__).parent / "fixtures"


def test_convert_pdf_returns_markdown_and_chunks() -> None:
    with open(FIXTURES/ "sample.pdf", "rb") as f:
        response = client.post("/v1/conversions", files={"file": ("sample.pdf", f, "application/pdf")})
        assert response.status_code == 200
        body = response.json()
        assert "Hello doc2chunks" in body["markdown"]
        assert len(body["chunks"]) >= 1


def test_convert_docx_returns_markdown_and_chunks() -> None:
    with open(FIXTURES/ "sample.docx", "rb") as f:
        response = client.post("/v1/conversions", files={"file": ("sample.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")})
        assert response.status_code == 200
        body = response.json()
        assert "# Hi doc2chunks" in body["markdown"]
        assert len(body["chunks"]) >= 1


def test_rejects_non_pdf() -> None:
    response = client.post("/v1/conversions", files = {"file": ("note.txt", b"Hello", "text/plain")})
    assert response.status_code == 415


def test_rejects_large_file() -> None:
    large_data = b"x" * (10 * 1024 * 1024 + 1)  # 10 MB + 1 byte
    response = client.post("/v1/conversions", files = {"file": ("large.pdf", large_data, "application/pdf")})
    assert response.status_code == 413


def test_rejects_bad_chunk_settings() -> None:
    with open(FIXTURES/ "sample.pdf", "rb") as f:
        response = client.post("/v1/conversions?chunk_size=0&overlap=0", files={"file": ("sample.pdf", f, "application/pdf")},) 
    assert response.status_code == 422