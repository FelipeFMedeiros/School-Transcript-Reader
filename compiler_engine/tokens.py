"""
compiler_engine.tokens
~~~~~~~~~~~~~~~~~~~~~~~
Definição do tipo de token (TokenType) e da estrutura imutável Token.

Os tipos são derivados diretamente dos autômatos finitos especificados
em ``automatos_finitos_lexico.html``.  A ordem dos membros do Enum não
tem relevância; a precedência de matching é controlada pelo Lexer.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    # ── Identificadores estruturados ──────────────────────────────────────────
    #
    # A prioridade de reconhecimento (do mais ao menos específico) é:
    #   T_CPF > T_DATA > T_PERIODO_LETIVO > T_MATRICULA > T_CARGA_HORARIA
    #   > T_NUMERO > T_SITUACAO_SIGLA > T_COD_DISCIPLINA > T_PALAVRA
    #   > T_MARCADOR_LEGENDA
    #
    # Essa ordem está implementada no Lexer, não aqui.

    # Autômato: \b[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}\b
    # Ex: 166.760.077-03
    T_CPF = auto()

    # Autômato: \b[0-9]{2}/[0-9]{2}/[0-9]{4}\b
    # Ex: 19/01/2005
    T_DATA = auto()

    # Autômato: \b[0-9]{4}\.[12]\b
    # Ex: 2023.1 | 2024.2
    T_PERIODO_LETIVO = auto()

    # Autômato: \b[0-9]{11}\b  (exatamente 11 dígitos consecutivos)
    # Ex: 20230029704
    T_MATRICULA = auto()

    # Autômato: \b[0-9]+[ \t]*h\b
    # Ex: 60h | 90 h
    T_CARGA_HORARIA = auto()

    # Autômato: \b[0-9]+(?:[.,][0-9]+)?\b
    # Ex: 7.8803 | 100,0 | 60 | 08052211
    T_NUMERO = auto()

    # Trie parcial — siglas exatas da tabela de situação acadêmica.
    # Ex: APR | APRN | REP | REPMF | REPF | REPN | REPNF |
    #     CANC | DISP | MATR | REC | TRANC | TRANS | INCORP | CUMP
    T_SITUACAO_SIGLA = auto()

    # Autômato: \b[A-Z]{3}[0-9]{4}\b
    # Ex: NCC0214 | CAN0077
    T_COD_DISCIPLINA = auto()

    # Autômato: [A-Za-zÀ-ÿ]+  (suporte completo ao PT-BR acentuado)
    # Ex: COMPUTAÇÃO | MEDEIROS | Matriculado
    T_PALAVRA = auto()

    # Pontuação e marcadores unitários do layout do histórico.
    # Ex: @ & # § % * : / - ( ) , .
    T_MARCADOR_LEGENDA = auto()

    # ── Controle ──────────────────────────────────────────────────────────────
    T_EOF = auto()


@dataclass(frozen=True)
class Token:
    """
    Unidade léxica produzida pelo Scanner.

    Attributes
    ----------
    tipo:
        Classificação semântica do lexema (membro de :class:`TokenType`).
    lexema:
        O texto exato capturado da entrada.
    linha:
        Número da linha na fonte (1-indexado).
    coluna:
        Número da coluna de início do lexema (1-indexado).
    """

    tipo: TokenType
    lexema: str
    linha: int
    coluna: int

    def __repr__(self) -> str:
        return (
            f"Token({self.tipo.name}, {self.lexema!r}, "
            f"L{self.linha}:C{self.coluna})"
        )

    def is_eof(self) -> bool:
        """Retorna True se este token encerra o fluxo de entrada."""
        return self.tipo is TokenType.T_EOF
