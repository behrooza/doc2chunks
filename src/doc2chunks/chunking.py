def chunk_text(text:str, size:int, overlap:int) -> list[str]:
    """Split a text into chunks of a given size with a given overlap."""
    if size <= 0:
        raise ValueError("size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap must be greater than or equal to 0")
    if overlap >= size:
        raise ValueError("overlap must be less than size")

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        start += size - overlap
    return chunks