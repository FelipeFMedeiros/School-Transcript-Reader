"""
compiler_engine.semantic
~~~~~~~~~~~~~~~~~~~~~~~~~
Analisador Semântico para históricos escolares do SIGAA-UERN.

Recebe a estrutura extraída pelo Parser e valida a coerência dos dados.

Regras semânticas previstas (a implementar):
    - Situação APR/APRN exige média >= 5.0.
    - Situação REP/REPMF exige média < 6.0.
    - Frequência deve estar no intervalo [0, 100].
    - Carga horária deve ser > 0.
    - T_PERIODO_LETIVO deve ser >= ano de ingresso do aluno.
    - Equivalências devem referenciar códigos existentes na tabela.

TODO: Implementar após revisão do Parser.
"""

from __future__ import annotations

from typing import Any

from .exceptions import SemanticError


class SemanticAnalyser:
    """
    Valida a coerência semântica da AST produzida pelo Parser.

    Parameters
    ----------
    ast:
        Dicionário retornado por :meth:`~parser.Parser.parse`.

    Raises
    ------
    SemanticError
        Quando os dados são estruturalmente válidos mas semanticamente
        inconsistentes.

    .. note::
        Ainda não implementado.  Lança ``NotImplementedError`` ao chamar
        :meth:`analyse`.
    """

    # Limites semânticos formais conforme a legenda do histórico
    _NOTA_APROVACAO_MEDIA: float = 7.0
    _NOTA_APROVACAO_MINIMA: float = 6.0
    _NOTA_MINIMA_VALIDA: float = 0.0
    _NOTA_MAXIMA_VALIDA: float = 10.0
    _FREQ_MINIMA_VALIDA: float = 0.0
    _FREQ_MAXIMA_VALIDA: float = 100.0

    def __init__(self, ast: dict[str, Any]) -> None:
        self._ast = ast

    def analyse(self) -> dict[str, Any]:
        """
        Executa todas as validações semânticas e retorna a AST anotada.

        Returns
        -------
        dict
            A mesma AST de entrada, possivelmente enriquecida com
            metadados de validação.

        Raises
        ------
        NotImplementedError
            Enquanto o analisador semântico ainda não foi implementado.
        """
        raise NotImplementedError(
            "Analisador Semântico ainda não implementado. "
            "Implemente os métodos _validate_*() com as regras de "
            "coerência do histórico escolar."
        )
