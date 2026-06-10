"""
compiler_engine.pdf_extractor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Utilitário para extração do texto bruto de um PDF de histórico escolar
do SIGAA-UERN.

Dependência externa:
    pip install pdfplumber

``pdfplumber`` preserva melhor a ordem de leitura de tabelas em PDFs do
SIGAA do que PyMuPDF, por isso é a biblioteca escolhida.  A tolerância
de agrupamento (x_tolerance / y_tolerance) está ajustada para compensar
o espaçamento variável entre colunas.
"""

from __future__ import annotations

from pathlib import Path


def extract_text(pdf_path: str | Path) -> str:
    """
    Extrai e concatena o texto de todas as páginas de um PDF.

    Parameters
    ----------
    pdf_path:
        Caminho para o arquivo ``.pdf`` do histórico escolar.

    Returns
    -------
    str
        Texto bruto completo, com páginas separadas por ``\\n``.

    Raises
    ------
    ImportError
        Se ``pdfplumber`` não estiver instalado no ambiente.
    FileNotFoundError
        Se o arquivo não existir no caminho fornecido.
    """
    try:
        import pdfplumber  # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "pdfplumber não encontrado. Instale com:\n"
            "    pip install pdfplumber"
        ) from exc

    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    pages: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            # x_tolerance agrupa caracteres próximos na mesma "palavra";
            # y_tolerance define o espaçamento que separa linhas distintas.
            text: str | None = page.extract_text(x_tolerance=3, y_tolerance=3)
            if text:
                pages.append(text)

    # Salvar texto do pdf em um txt para analisar
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(pages))

    return "\n".join(pages)
