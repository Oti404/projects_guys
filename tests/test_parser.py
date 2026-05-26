import os
import pytest
from ai_module.parser import parse_cv

SAMPLE_PDF = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "sample_cv.pdf")


def test_parse_real_pdf_returns_text():
    if not os.path.exists(SAMPLE_PDF):
        pytest.skip("sample_cv.pdf nu exista in data/raw/")
    text = parse_cv(SAMPLE_PDF)
    assert isinstance(text, str)
    assert len(text) > 50
    assert not text.startswith("Error")


def test_parse_missing_file_returns_error():
    result = parse_cv("fisier_inexistent.pdf")
    assert result.startswith("Error")


def test_parse_unsupported_extension_returns_error():
    result = parse_cv("cv.txt")
    assert result.startswith("Error")
