
class CompilerEngineError(Exception):
    """Erro base do motor."""


class PdfExtractionError(CompilerEngineError):
    """Falha ao abrir/ler o PDF ou extrair texto."""
