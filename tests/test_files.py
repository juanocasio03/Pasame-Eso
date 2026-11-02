"""Tests for upload helpers (REQ.4.2, NFR-SEC-06)."""
import io
import zipfile

from app.utils.files import detect_file_type, sha256_of


def test_same_content_same_hash():
    a = io.BytesIO(b"same notes")
    b = io.BytesIO(b"same notes")
    assert sha256_of(a) == sha256_of(b)


def test_different_content_different_hash():
    assert sha256_of(io.BytesIO(b"notes v1")) != sha256_of(io.BytesIO(b"notes v2"))


def test_detects_pdf_by_content():
    assert detect_file_type(io.BytesIO(b"%PDF-1.7 rest of file")) == "pdf"


def test_detects_png():
    assert detect_file_type(io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"\x00" * 20)) == "png"


def test_detects_docx():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("word/document.xml", "<doc/>")
    assert detect_file_type(buf) == "docx"


def test_plain_text_allowed():
    assert detect_file_type(io.BytesIO("Notas de cálculo".encode("utf-8"))) == "txt"


def test_executable_renamed_to_pdf_is_rejected():
    # An .exe starts with "MZ"; renaming it to notes.pdf must not fool the check.
    assert detect_file_type(io.BytesIO(b"MZ\x90\x00\x03\x00\x00\x00")) is None
