import tempfile
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel

from doc2chunks.chunking import chunk_text
from doc2chunks.convert import docx_to_markdown, pdf_to_markdown

app = FastAPI(title="doc2chunks API", version = "0.1.0")

MAX_BYTES = 10 * 1024 * 1024  # 10 MB

class ConvertResponse(BaseModel):
    filename: str
    markdown: str
    chunks: list[str]

@app.post("/v1/convert", response_model = ConvertResponse)
async def convert(
        file: UploadFile, chunk_size: int=1000, overlap: int=100) -> ConvertResponse:
    """Convert a PDF or DOCX file to markdown and split it into chunks."""
    data = await file.read()

    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="File too large: The input file must be smaller than 10 MB.")

    # Process the file and generate markdown and chunks
    name = file.filename or ""
    if not name.lower().endswith((".pdf", ".docx")):
        raise HTTPException(status_code=415, detail="Invalid file type: Only PDF and DOCX files are supported.")

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "upload.pdf"
        path.write_bytes(data)
        if name.lower().endswith(".pdf"):
            markdown = pdf_to_markdown(path)
        else:
            markdown = docx_to_markdown(path)

    try:
        chunks = chunk_text(markdown, size = chunk_size, overlap = overlap) 
    except ValueError as error:
        raise HTTPException(status_code = 422, detail = str(error)) from error

    return ConvertResponse(filename = name, markdown = markdown, chunks = chunks)