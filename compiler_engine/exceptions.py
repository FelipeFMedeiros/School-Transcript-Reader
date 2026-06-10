"""
compiler_engine.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Hierarquia de erros customizados para as três fases do compilador.
Cada exceção carrega a posição exata (linha, coluna) do token ofensor
para facilitar o diagnóstico.
"""

from __future__ import annotations


class CompilerError(Exception):
    """Classe base para todos os erros do compilador."""

    def __init__(self, message: str, line: int, column: int) -> None:
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"[Linha {line}, Col {column}] {message}")

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"message={self.message!r}, "
            f"line={self.line}, "
            f"column={self.column})"
        )


class LexicalError(CompilerError):
    """
    Lançado pelo Scanner quando um caractere ou sequência de caracteres
    não pertence ao alfabeto formal definido para o histórico escolar.

    Exemplo:
        Caractere inválido: '¥' (U+00A5) na linha 3, coluna 17.
    """


class SyntacticError(CompilerError):
    """
    Lançado pelo Parser quando a sequência de tokens não obedece às
    regras de produção da Gramática Livre de Contexto (Descida Recursiva).

    Exemplo:
        Esperava T_COD_DISCIPLINA mas encontrou T_PALAVRA 'Campus'
        na linha 12, coluna 5.
    """


class SemanticError(CompilerError):
    """
    Lançado pelo SemanticAnalyser quando os dados extraídos são
    estruturalmente válidos mas semanticamente inconsistentes.

    Exemplos:
        - Situação APR com média < 5.0.
        - Carga horária igual a 0.
        - Frequência acima de 100 %.
    """
