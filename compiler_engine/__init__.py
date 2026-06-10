"""
compiler_engine
~~~~~~~~~~~~~~~
Motor do compilador para leitura e validação de históricos escolares
do SIGAA-UERN em formato PDF.

Pipeline:
    pdf_extractor  →  lexer (Scanner)  →  parser (Parser)  →  semantic (SemanticAnalyser)

Uso rápido:
    python -m compiler_engine.main <caminho.pdf>
    python -m compiler_engine.main --text "<texto bruto>"
"""

from .exceptions import LexicalError, SemanticError, SyntacticError
from .lexer import Scanner
from .tokens import Token, TokenType

__all__ = [
    "LexicalError",
    "SyntacticError",
    "SemanticError",
    "Token",
    "TokenType",
    "Scanner",
]
