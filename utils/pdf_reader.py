"""
utils/pdf_reader.py
Extracts plain text from a PDF file using PyMuPDF.
"""

import os


def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        import fitz
    except ImportError:
        raise ImportError("Install PyMuPDF: pip install pymupdf")

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    pages = [page.get_text() for page in doc]
    doc.close()

    text = "\n".join(pages).strip()
    if not text:
        raise ValueError("No extractable text found in PDF (may be a scanned image).")
    return text
