"""
compiler_engine.main
~~~~~~~~~~~~~~~~~~~~~
Ponto de entrada para testes manuais do pipeline do compilador via CLI.

Uso
---
    # Passar texto bruto diretamente (útil para testes rápidos do Lexer):
    python -m compiler_engine.main --text "2023.1 NCC0214 APR 8.5 60h"

    # Passar um PDF real:
    python -m compiler_engine.main historico.pdf

    # Suprimir a listagem individual de tokens:
    python -m compiler_engine.main --text "NCC0214 APR" --no-verbose
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List

from .exceptions import LexicalError, SemanticError, SyntacticError
from .lexer import Scanner
from .tokens import Token


# ──────────────────────────────────────────────────────────────────────────────
# Helpers de formatação
# ──────────────────────────────────────────────────────────────────────────────

def _print_header(title: str) -> None:
    bar = "─" * 60
    print(f"\n{bar}")
    print(f"  {title}")
    print(bar)


def _tokens_to_serializable(tokens: List[Token]) -> list[dict]:
    return [
        {
            "tipo": tok.tipo.name,
            "lexema": tok.lexema,
            "linha": tok.linha,
            "coluna": tok.coluna,
        }
        for tok in tokens
    ]


# ──────────────────────────────────────────────────────────────────────────────
# Pipeline
# ──────────────────────────────────────────────────────────────────────────────

def run_pipeline(source_text: str, *, verbose: bool = True) -> None:
    """Executa as fases do compilador sobre ``source_text``."""
    _print_header("COMPILER ENGINE — HISTÓRICO ESCOLAR SIGAA-UERN")

    # ── Fase 1: Análise Léxica ─────────────────────────────────────────────
    print("\n[1/3] Análise Léxica...")
    try:
        tokens = Scanner(source_text).tokenize()
    except LexicalError as exc:
        print(f"  ERRO LÉXICO  →  {exc}")
        sys.exit(1)

    token_count = len(tokens) - 1  # exclui EOF
    print(f"  OK  {token_count} token(s) gerado(s).")

    if verbose:
        print()
        for tok in tokens:
            print(f"    {tok}")

    # ── Fase 2: Análise Sintática (pendente) ───────────────────────────────
    print("\n[2/3] Análise Sintática... (não implementada — aguardando revisão do Lexer)")

    # ── Fase 3: Análise Semântica (pendente) ───────────────────────────────
    print("\n[3/3] Análise Semântica... (não implementada)")

    # ── Saída provisória: tokens como JSON ────────────────────────────────
    print("\n── Tokens (JSON) " + "─" * 43)
    print(json.dumps(_tokens_to_serializable(tokens), ensure_ascii=False, indent=2))


# ──────────────────────────────────────────────────────────────────────────────
# Entrypoint
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    args = sys.argv[1:]

    if not args:
        print(
            "Uso:\n"
            "  python -m compiler_engine.main <caminho.pdf>\n"
            "  python -m compiler_engine.main --text <texto_raw> [--no-verbose]"
        )
        sys.exit(1)

    verbose = "--no-verbose" not in args
    args = [a for a in args if a != "--no-verbose"]

    if args[0] == "--text":
        source = " ".join(args[1:])
        if not source.strip():
            print("Erro: forneça o texto após --text.")
            sys.exit(1)
        run_pipeline(source, verbose=verbose)

    else:
        pdf_path = Path(args[0])
        try:
            from .pdf_extractor import extract_text
            source = extract_text(pdf_path)
        except (ImportError, FileNotFoundError) as exc:
            print(f"Erro ao extrair PDF: {exc}")
            sys.exit(1)
        run_pipeline(source, verbose=verbose)


if __name__ == "__main__":
    main()
