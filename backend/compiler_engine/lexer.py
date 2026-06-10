from __future__ import annotations

import re

from compiler_engine.dto import Token, CompilerError, PHASE_LEXICAL
from compiler_engine.tokens import TokenType, TOKEN_SPECS, WHITESPACE


# Monta o regex 
_MASTER = re.compile(
    "|".join(
        [f"(?P<{ttype.name}>{pattern})" for ttype, pattern in TOKEN_SPECS]
        + [f"(?P<WS>{WHITESPACE})"]
    )
)

#
class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.tokens: list[Token] = []
        self.errors: list[CompilerError] = []

    def tokenize(self) -> tuple[list[Token], list[CompilerError]]:
        pos = 0
        line = 1
        line_start = 0  # linha atual contar colunas
        n = len(self.text)

        while pos < n:
            ch = self.text[pos]

            # quebra de linha
            if ch == "\n":
                line += 1
                pos += 1
                line_start = pos
                continue

            match = _MASTER.match(self.text, pos)
            if match is None:
                # caracteres não reconhecidos 
                column = pos - line_start + 1
                self.errors.append(
                    CompilerError(
                        phase=PHASE_LEXICAL,
                        message=f"Caractere inválido {ch!r} fora do alfabeto da linguagem.",
                        line=line,
                        column=column,
                    )
                )
                self.tokens.append(
                    Token(type=TokenType.T_ERRO.value, value=ch, line=line, column=column)
                )
                pos += 1
                continue

            kind = match.lastgroup
            value = match.group()
            column = match.start() - line_start + 1

            if kind != "WS":
                self.tokens.append(
                    Token(type=kind, value=value, line=line, column=column)
                )

            # demais tokens podem conter espaços internos (só n quebra de linha)
            pos = match.end()

        self.tokens.append(Token(type=TokenType.T_EOF.value, value="", line=line, column=1))
        return self.tokens, self.errors


def tokenize(text: str) -> tuple[list[Token], list[CompilerError]]:
    return Lexer(text).tokenize()
