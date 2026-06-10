"""
compiler_engine.parser
~~~~~~~~~~~~~~~~~~~~~~~
Analisador Sintático — Descida Recursiva (Recursive Descent Parser).

Baseado nas regras BNF definidas em ``analise_sintatica_gramatica.html``.
Todas as regras foram modeladas com recursão à DIREITA para compatibilidade
com o método de descida recursiva (sem recursão à esquerda).

TODO: Implementar na próxima iteração após revisão do Lexer.
"""

from __future__ import annotations

from typing import Any, List

from .exceptions import SyntacticError
from .tokens import Token, TokenType


class Parser:
    """
    Parser de descida recursiva para históricos escolares do SIGAA-UERN.

    Cada regra não-terminal da gramática corresponde a um método
    ``parse_<NomeRegra>()``.  O método ``match()`` consome o token atual
    se o tipo coincidir, ou lança :class:`SyntacticError` caso contrário.

    Parameters
    ----------
    tokens:
        Lista de tokens produzida pelo :class:`~lexer.Scanner`.
        Deve terminar com um token ``T_EOF``.

    Raises
    ------
    SyntacticError
        Quando a sequência de tokens viola as regras gramaticais.

    .. note::
        Ainda não implementado.  Lança ``NotImplementedError`` ao chamar
        :meth:`parse`.
    """

    def __init__(self, tokens: List[Token]) -> None:
        self._tokens = tokens
        self._pos: int = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def parse(self) -> dict[str, Any]:
        """
        Executa o parsing completo e retorna a AST simplificada
        como dicionário Python.

        Returns
        -------
        dict
            Estrutura aninhada com todos os dados extraídos do histórico.

        Raises
        ------
        NotImplementedError
            Enquanto o parser ainda não foi implementado.
        """
        raise NotImplementedError(
            "Parser ainda não implementado. "
            "Implemente os métodos parse_<Regra>() baseados nas BNFs de "
            "analise_sintatica_gramatica.html."
        )

    # ------------------------------------------------------------------
    # Helpers (serão usados pelos métodos parse_*())
    # ------------------------------------------------------------------

    @property
    def _current(self) -> Token:
        """Token sob o cursor sem consumi-lo."""
        return self._tokens[self._pos]

    def _match(self, expected: TokenType) -> Token:
        """
        Consome e retorna o token atual se o tipo coincidir com ``expected``.

        Raises
        ------
        SyntacticError
            Se o tipo do token atual for diferente de ``expected``.
        """
        tok = self._current
        if tok.tipo is not expected:
            raise SyntacticError(
                f"Esperava {expected.name} mas encontrou "
                f"{tok.tipo.name} {tok.lexema!r}",
                tok.linha,
                tok.coluna,
            )
        self._pos += 1
        return tok

    def _match_palavra(self, lexema: str) -> Token:
        """
        Consome o token atual se for T_PALAVRA com o lexema exato fornecido
        (case-insensitive).

        Raises
        ------
        SyntacticError
            Se o token atual não for a palavra esperada.
        """
        tok = self._current
        if tok.tipo is not TokenType.T_PALAVRA or tok.lexema.upper() != lexema.upper():
            raise SyntacticError(
                f"Esperava palavra {lexema!r} mas encontrou "
                f"{tok.tipo.name} {tok.lexema!r}",
                tok.linha,
                tok.coluna,
            )
        self._pos += 1
        return tok
