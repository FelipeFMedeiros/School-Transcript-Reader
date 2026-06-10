from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

# fases do compilador
PHASE_LEXICAL = "lexical"
PHASE_SYNTACTIC = "syntactic"
PHASE_SEMANTIC = "semantic"


@dataclass(frozen=True)
class Token:

    type: str       
    value: str         
    line: int          
    column: int        

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "value": self.value,
            "line": self.line,
            "column": self.column,
        }


@dataclass
class CompilerError:

    phase: str                      
    message: str
    line: int = 0
    column: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "phase": self.phase,
            "message": self.message,
            "line": self.line,
            "column": self.column,
        }


@dataclass
class ParseNode:
    """
    no da arvore de derivação
    """

    symbol: str
    children: list["ParseNode"] = field(default_factory=list)
    token: Optional[Token] = None

    def add(self, node: "ParseNode") -> "ParseNode":
        self.children.append(node)
        return node

    @classmethod
    def leaf(cls, token: Token) -> "ParseNode":
        return cls(symbol=token.type, token=token)

    def to_dict(self) -> dict[str, Any]:
        node: dict[str, Any] = {"symbol": self.symbol}
        if self.token is not None:
            node["value"] = self.token.value
            node["line"] = self.token.line
        if self.children:
            node["children"] = [c.to_dict() for c in self.children]
        return node


@dataclass
class PipelineResult:

    success: bool
    raw_text: str = ""
    tokens: list[Token] = field(default_factory=list)
    syntax_tree: Optional[ParseNode] = None
    semantic_analysis: dict[str, Any] = field(default_factory=dict)
    student_data: Optional[dict[str, Any]] = None
    errors: list[CompilerError] = field(default_factory=list)

    def errors_by_phase(self, phase: str) -> list[CompilerError]:
        return [e for e in self.errors if e.phase == phase]

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "tokens": [t.to_dict() for t in self.tokens],
            "syntax_tree": self.syntax_tree.to_dict() if self.syntax_tree else None,
            "semantic_analysis": self.semantic_analysis,
            "student_data": self.student_data,
            "errors": [e.to_dict() for e in self.errors],
        }
