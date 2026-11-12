import pytest

from doc2chunks.chunking import chunk_text


def test_short_text_in_one_chunk() -> None:
    assert chunk_text("abs", size = 10, overlap = 0) == ["abs"]


def test_split_without_overlap() -> None:
    assert chunk_text("abcdefghij", size = 3, overlap = 0) == ["abc", "def", "ghi", "j"]


def test_split_with_overlap() -> None:
    assert chunk_text("abcdefghij", size = 3, overlap = 1) == ["abc", "cde", "efg", "ghi", "ij"]


@pytest.mark.parametrize("size, overlap", [(0,0), (5,5), (5,6), (5,-1)])
def test_invalid_arguments_raise(size: int, overlap: int) -> None:
    with pytest.raises(ValueError):
        chunk_text("abcdefghij", size = size, overlap = overlap)
