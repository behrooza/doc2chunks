# doc2chunks

[![CI](https://github.com/behrooza/doc2chunks/actions/workflows/ci.yml/badge.svg)](https://github.com/behrooza/doc2chunks/actions/workflows/ci.yml)

Converts PDF and DOCX documents into clean Markdown, and split them into ready-to-use text chunks for LLM and
RAG pipelines, behind a small REST API.

## What doc2chunks does

1. Upload a PDF or DOCX (max 10 Mb)
2. It converts the document to Markdown.
3. It splits the Markdown into chunks of a size and overlap given by the user.

## Quick start

Requires Python 3.11 or newer.

```
git clone https://github.com/behrooza/doc2chunks.git
cd doc2chunks
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e .
uvicorn doc2chunks.api:app
```

Access the API in your browser uaing http://127.0.0.1:8000/docs

## Example

```
curl -X POST "http://127.0.0.1:8000/v1/conversions?chunk_size=500&overlap=50" -F "file=@tests/fixtures/sample.pdf"
```

Response:

```json
{"filename":"sample.pdf","markdown":"# Hello doc2chunks \n\nThis is a sample test. \n\n","chunks":["# Hello doc2chunks \n\nThis is a sample test. \n\n"]}
```

## API

`POST /v1/convert`

| Parameter    | Where | Default | Meaning                            |
|--------------|-------|---------|------------------------------------|
| `file`       | body  | –       | the document to convert            |
| `chunk_size` | query | 1000    | characters per chunk               |
| `overlap`    | query | 100     | characters shared between chunks   |

| Status | Meaning                          |
|--------|----------------------------------|
| 200    | success                          |
| 413    | file larger than 10 MB           |
| 415    | unsupported file type            |
| 422    | invalid chunk settings           |

## Development

```
pip install -e ".[dev]"
pytest
ruff check .
mypy src
```

All three run automatically on every pull request (GitHub Actions).

## Roadmap

- OCR for scanned PDFs
- Table extraction
- Embeddings and a `/v1/query` endpoint (basic RAG)

## License

MIT