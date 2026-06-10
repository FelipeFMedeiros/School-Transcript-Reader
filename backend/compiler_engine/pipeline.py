from __future__ import annotations

from typing import Any

from compiler_engine.dto import PipelineResult
from compiler_engine.pdf_extractor import extract_text
from compiler_engine.lexer import tokenize
from compiler_engine.parser import parse
from compiler_engine.semantic import analyze


class CompilerPipeline:
    def run(self, source_path: str) -> dict[str, Any]:
        return self.run_result(source_path).to_dict()

    def run_result(self, source_path: str) -> PipelineResult:
        result = PipelineResult(success=False)

        # extração
        text = extract_text(source_path)
        result.raw_text = text

        # análise léxica
        tokens, lex_errors = tokenize(text)
        result.tokens = tokens
        result.errors.extend(lex_errors)

        # análise sintática
        tree, syn_errors = parse(tokens)
        result.syntax_tree = tree
        result.errors.extend(syn_errors)

        # análise semântica
        if not syn_errors:
            analysis, student, sem_errors = analyze(tree)
            result.semantic_analysis = analysis
            result.student_data = student
            result.errors.extend(sem_errors)

        result.success = len(result.errors) == 0
        return result

    def run_text(self, text: str) -> PipelineResult:
        result = PipelineResult(success=False, raw_text=text)
        tokens, lex_errors = tokenize(text)
        result.tokens = tokens
        result.errors.extend(lex_errors)
        tree, syn_errors = parse(tokens)
        result.syntax_tree = tree
        result.errors.extend(syn_errors)
        if not syn_errors:
            analysis, student, sem_errors = analyze(tree)
            result.semantic_analysis = analysis
            result.student_data = student
            result.errors.extend(sem_errors)
        result.success = len(result.errors) == 0
        return result
