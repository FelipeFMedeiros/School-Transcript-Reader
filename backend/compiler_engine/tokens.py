from __future__ import annotations

from enum import Enum


class TokenType(str, Enum):
    T_CPF = "T_CPF"
    T_DATA = "T_DATA"
    T_PERIODO_LETIVO = "T_PERIODO_LETIVO"
    T_MATRICULA = "T_MATRICULA"
    T_COD_DISCIPLINA = "T_COD_DISCIPLINA"
    T_CARGA_HORARIA = "T_CARGA_HORARIA"

    T_NUMERO = "T_NUMERO"
    T_SITUACAO_SIGLA = "T_SITUACAO_SIGLA"
    T_PALAVRA = "T_PALAVRA"
    T_MARCADOR_LEGENDA = "T_MARCADOR_LEGENDA"
    T_EOF = "T_EOF"
    T_ERRO = "T_ERRO"


# Siglas de situação reconhecidas. Ordenadas por comprimento decrescente para
# que a alternância de regex case o prefixo mais longo (REPMF antes de REP),
SITUACAO_SIGLAS = [
    "REPMF",
    "REPF",
    "TRANC",
    "MATR",
    "CUMP",
    "DISP",
    "APRN",
    "APR",
    "REP",
]

_SIGLAS_ALT = "|".join(SITUACAO_SIGLAS)

# letras com acentuação pt-br
_LETRA = r"A-Za-zÀ-ÿ"

# token final 
TOKEN_SPECS: list[tuple[TokenType, str]] = [
    (TokenType.T_CPF, r"\d{3}\.\d{3}\.\d{3}-\d{2}(?!\d)"),
    (TokenType.T_DATA, r"\d{2}/\d{2}/\d{4}(?!\d)"),
    (TokenType.T_PERIODO_LETIVO, r"\d{4}\.[1-2](?!\d)"),
    (TokenType.T_MATRICULA, r"\d{11}(?!\d)"),
    (TokenType.T_COD_DISCIPLINA, rf"[A-Z]{{3}}\d{{4}}(?![{_LETRA}\d])"),
    (TokenType.T_CARGA_HORARIA, r"\d+\s*h(?![A-Za-z])"),
    (TokenType.T_SITUACAO_SIGLA, rf"(?:{_SIGLAS_ALT})(?![{_LETRA}])"),
    (TokenType.T_NUMERO, r"\d+(?:[.,]\d+)?"),
    (TokenType.T_PALAVRA, rf"[{_LETRA}]+"),
    (TokenType.T_MARCADOR_LEGENDA, r"[@&#§%*:/()\-.,°º]"),
]

# ignora espaços em branco e tbb
WHITESPACE = r"[ \t\r\f\v]+"
