"""
compiler_engine.lexer
~~~~~~~~~~~~~~~~~~~~~~
Analisador Léxico (Scanner) baseado nos autômatos finitos definidos em
``automatos_finitos_lexico.html``.

Estratégia de implementação
----------------------------
Um único padrão-mestre é construído concatenando todas as expressões
regulares via alternação (|).  A engine do módulo ``re`` testa as
alternativas da ESQUERDA para a DIREITA e retorna o PRIMEIRO casamento,
por isso a ordem em ``_TOKEN_SPECS`` é crítica:

    padrões mais específicos (comprimento fixo / estrutura única)
        DEVEM preceder
    padrões mais gerais (comprimento variável / apenas dígitos/letras)

Rastreamento de posição
-----------------------
Espaços horizontais (SPACE, TAB, CR) são descartados silenciosamente.
Quebras de linha incrementam o contador de linha e resetam a coluna.
O consumo de espaços embutidos em T_CARGA_HORARIA (ex: "60 h") avança
a coluna corretamente, pois o lexema completo é medido depois do match.
"""

from __future__ import annotations

import re
from typing import List

from .exceptions import LexicalError
from .tokens import Token, TokenType

# ──────────────────────────────────────────────────────────────────────────────
# Especificação dos tokens  →  (tipo, regex_str)
#
# ORDEM IMPORTA: cada padrão é testado na sequência abaixo.  Padrões mais
# restritos aparecem ANTES dos mais genéricos para evitar casamentos parciais.
# ──────────────────────────────────────────────────────────────────────────────
_TOKEN_SPECS: list[tuple[TokenType, str]] = [
    # 1. CPF  →  NNN.NNN.NNN-NN
    #    Deve vir antes de T_NUMERO (ambos iniciam com dígitos).
    (
        TokenType.T_CPF,
        r"\b[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}\b",
    ),
    # 2. Data  →  DD/MM/AAAA
    #    Deve vir antes de T_NUMERO e de T_MARCADOR_LEGENDA ('/').
    (
        TokenType.T_DATA,
        r"\b[0-9]{2}/[0-9]{2}/[0-9]{4}\b",
    ),
    # 3. Período Letivo  →  AAAA.1 ou AAAA.2
    #    Deve vir antes de T_NUMERO (que também captura decimais com ponto).
    (
        TokenType.T_PERIODO_LETIVO,
        r"\b[0-9]{4}\.[12]\b",
    ),
    # 4. Matrícula  →  exatamente 11 dígitos (word-boundary nos dois lados)
    #    Deve vir antes de T_NUMERO para não ser particionada em pedaços.
    (
        TokenType.T_MATRICULA,
        r"\b[0-9]{11}\b",
    ),
    # 5. Carga Horária  →  dígitos + espaço(s) opcional(is) + 'h'
    #    [ \t]* em vez de \s* para não engolir quebras de linha.
    #    Deve vir antes de T_NUMERO.
    (
        TokenType.T_CARGA_HORARIA,
        r"\b[0-9]+[ \t]*h\b",
    ),
    # 6. Número genérico  →  inteiro ou decimal (separador: ponto OU vírgula)
    #    Ex: 7.8803 | 100,0 | 60 | 08052211
    (
        TokenType.T_NUMERO,
        r"\b[0-9]+(?:[.,][0-9]+)?\b",
    ),
    # 7. Sigla de situação acadêmica  →  Trie parcial das siglas exatas.
    #    Alternativas mais longas ANTES das mais curtas para evitar casamento
    #    parcial (ex: REPMF antes de REP).
    #    Deve vir antes de T_PALAVRA.
    (
        TokenType.T_SITUACAO_SIGLA,
        r"\b(?:REPNF|REPMF|REPF|REPN|REP|APRN|APR|CANC|DISP|MATR|REC|TRANC|TRANS|INCORP|CUMP)\b",
    ),
    # 8. Código de disciplina  →  3 letras MAIÚSCULAS + 4 dígitos
    #    Deve vir antes de T_PALAVRA (que também captura letras maiúsculas).
    (
        TokenType.T_COD_DISCIPLINA,
        r"\b[A-Z]{3}[0-9]{4}\b",
    ),
    # 9. Palavra  →  sequência de letras latinas (a-z, A-Z, À-ÿ)
    #    Suporte completo à acentuação do Português Brasileiro.
    (
        TokenType.T_PALAVRA,
        r"[A-Za-zÀ-ÿ]+",
    ),
    # 10. Marcadores e pontuação unitária
    #     Inclui os marcadores da legenda (@, &, #, §, %, *, º, °) e os
    #     separadores estruturais ( : / - ( ) , . ).
    (
        TokenType.T_MARCADOR_LEGENDA,
        r"[@&#§%*º°:/\-()\.,]",
    ),
]

# ──────────────────────────────────────────────────────────────────────────────
# Padrão-mestre compilado com grupos nomeados.
# O prefixo "_" nos nomes de grupo evita colisões com identificadores Python.
# ──────────────────────────────────────────────────────────────────────────────
_MASTER_RE: re.Pattern[str] = re.compile(
    "|".join(
        f"(?P<_{ttype.name}>{pattern})" for ttype, pattern in _TOKEN_SPECS
    ),
    re.UNICODE,
)

# Padrões auxiliares para controle de posição (não geram tokens)
_HORIZONTAL_WS_RE: re.Pattern[str] = re.compile(r"[ \t\r]+")
_NEWLINE_RE: re.Pattern[str] = re.compile(r"\n")


# ──────────────────────────────────────────────────────────────────────────────
# Função auxiliar (module-level para evitar overhead de atributo em loop)
# ──────────────────────────────────────────────────────────────────────────────
def _resolve_type(match: re.Match) -> TokenType:  # type: ignore[type-arg]
    """
    Retorna o TokenType correspondente ao primeiro grupo nomeado que disparou.

    Raises
    ------
    RuntimeError
        Estado impossível — indica dessincronização entre _TOKEN_SPECS e
        _MASTER_RE.
    """
    for ttype, _ in _TOKEN_SPECS:
        if match.group(f"_{ttype.name}") is not None:
            return ttype
    raise RuntimeError(
        "Nenhum grupo do padrão-mestre casou — _TOKEN_SPECS e _MASTER_RE "
        "estão fora de sincronia."
    )


# ──────────────────────────────────────────────────────────────────────────────
# Scanner
# ──────────────────────────────────────────────────────────────────────────────
class Scanner:
    """
    Analisador Léxico para históricos escolares do SIGAA-UERN.

    Recebe o texto bruto extraído do PDF, descarta espaços em branco
    horizontais e produz uma lista plana de :class:`~tokens.Token`.
    Cada token carrega tipo, lexema, linha e coluna de origem.

    O token sentinela ``T_EOF`` é sempre o último elemento da lista.

    Parameters
    ----------
    source:
        Texto bruto do histórico escolar (unicode, qualquer quebra de linha).

    Raises
    ------
    LexicalError
        Quando um caractere não pertence ao alfabeto formal.

    Example
    -------
    >>> scanner = Scanner("NCC0214 APR 8.5")
    >>> tokens = scanner.tokenize()
    >>> tokens[0]
    Token(T_COD_DISCIPLINA, 'NCC0214', L1:C1)
    >>> tokens[1]
    Token(T_SITUACAO_SIGLA, 'APR', L1:C9)
    >>> tokens[2]
    Token(T_NUMERO, '8.5', L1:C13)
    """

    def __init__(self, source: str) -> None:
        self._source = source

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def tokenize(self) -> List[Token]:
        """
        Varre toda a entrada e retorna a lista de tokens (incluindo EOF).

        Returns
        -------
        List[Token]
            Tokens em ordem de aparição.  O último elemento é sempre
            ``Token(T_EOF, '', linha_final, coluna_final)``.
        """
        tokens: list[Token] = []
        src = self._source
        src_len = len(src)

        pos: int = 0
        line: int = 1
        col: int = 1

        while pos < src_len:
            # ── 1. Descartar espaços horizontais (space, tab, CR) ──────────
            m = _HORIZONTAL_WS_RE.match(src, pos)
            if m:
                col += m.end() - m.start()
                pos = m.end()
                continue

            # ── 2. Rastrear quebras de linha ───────────────────────────────
            m = _NEWLINE_RE.match(src, pos)
            if m:
                line += 1
                col = 1
                pos = m.end()
                continue

            # ── 3. Tentar casar um token conhecido ─────────────────────────
            m = _MASTER_RE.match(src, pos)
            if m:
                ttype = _resolve_type(m)
                lexema = m.group()
                tokens.append(Token(ttype, lexema, line, col))
                # Avança coluna pelo comprimento do lexema (inclui espaços
                # internos em T_CARGA_HORARIA, e.g. "60 h" → +4).
                col += len(lexema)
                pos = m.end()
                continue

            # ── 4. Caractere fora do alfabeto → erro léxico ────────────────
            bad_char = src[pos]
            raise LexicalError(
                f"Caractere inválido: {bad_char!r} (U+{ord(bad_char):04X})\n"
                f"Texto completo: {src[pos:pos+50]!r}",
                line,
                col,
            )

        tokens.append(Token(TokenType.T_EOF, "", line, col))
        return tokens
