"""File helpers for uploads: content-type detection and SHA-256 fingerprints.

Used by Post.create() for REQ.4.2 and NFR-SEC-06.
"""
import codecs
import hashlib
import zipfile

# Approved types (FEAT-04): PDF, PNG, JPEG, DOCX, plain text.
ALLOWED_TYPES = {
    "pdf": "application/pdf",
    "png": "image/png",
    "jpg": "image/jpeg",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "txt": "text/plain",
}


def sha256_of(stream, chunk_size=64 * 1024) -> str:
    """Return the SHA-256 hex digest of a file-like object, then rewind it."""
    digest = hashlib.sha256()
    stream.seek(0)
    for chunk in iter(lambda: stream.read(chunk_size), b""):
        digest.update(chunk)
    stream.seek(0)
    return digest.hexdigest()


def detect_file_type(stream):
    """Identify the file by its CONTENT (magic bytes), not its extension.

    Returns a key of ALLOWED_TYPES (e.g. "pdf") or None if the type is not approved.
    """
    stream.seek(0)
    head = stream.read(8)
    stream.seek(0)

    if head.startswith(b"%PDF-"):
        return "pdf"
    if head.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if head.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if head.startswith(b"PK\x03\x04"):
        # .docx files are zip archives containing word/document.xml
        try:
            with zipfile.ZipFile(stream) as zf:
                is_docx = "word/document.xml" in zf.namelist()
        except zipfile.BadZipFile:
            is_docx = False
        stream.seek(0)
        return "docx" if is_docx else None
    if _looks_like_text(stream):
        return "txt"
    return None


def _looks_like_text(stream, sample_size=4096) -> bool:
    stream.seek(0)
    sample = stream.read(sample_size)
    stream.seek(0)
    if b"\x00" in sample:
        return False
    try:
        # final=False tolerates a multi-byte character cut off at the sample's end
        codecs.getincrementaldecoder("utf-8")().decode(sample, final=False)
        return True
    except UnicodeDecodeError:
        return False
