from __future__ import annotations
import os

from compiler_engine.exceptions import PdfExtractionError


def extract_text(path: str) -> str:
    if not os.path.exists(path):
        raise PdfExtractionError(f"Arquivo não encontrado: {path}")

    if path.lower().endswith(".txt"):
        try:
            with open(path, encoding="utf-8") as fh: 
                return fh.read()
        except OSError as exc:  
            raise PdfExtractionError(str(exc)) from exc

    return _extract_pdf(path)


def _extract_pdf(path: str) -> str:
    try:
        import pdfplumber
    except ImportError as exc:  
        raise PdfExtractionError("pdfplumber não está instalado. Adicione 'pdfplumber' ao requirements.") from exc
    try:
        parts: list[str] = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                parts.append(page.extract_text() or "")
        return "\n".join(parts)
    except Exception as exc: 
        raise PdfExtractionError(f"Falha ao extrair texto do PDF: {exc}") from exc
