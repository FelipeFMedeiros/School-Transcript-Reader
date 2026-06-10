from __future__ import annotations

from typing import Any, Optional

from compiler_engine.dto import ParseNode, CompilerError, Token, PHASE_SEMANTIC
from compiler_engine.tokens import TokenType, SITUACAO_SIGLAS


class SemanticAnalyzer:
    def __init__(self, tree: ParseNode) -> None:
        self.tree = tree
        self.errors: list[CompilerError] = []

    def analyze(self) -> tuple[dict[str, Any], Optional[dict[str, Any]], list[CompilerError]]:
        student = self._extract_student_data()
        self._validate(student)
        analysis = {
            "total_disciplinas": len(student["disciplinas"]),
            "aprovadas": sum(
                1 for d in student["disciplinas"] if d["situacao"].upper().startswith("APR")
            ),
            "checagens_realizadas": [
                "matricula_8_a_11_digitos",
                "ira_intervalo_0_10",
                "carga_horaria_positiva",
                "situacao_valida",
            ],
        }
        return analysis, student, self.errors

    # extração da árvore sintática
    def _extract_student_data(self) -> dict[str, Any]:
        nome = self._first_sequencia_palavras(self._find("DadosPessoais"))
        matricula = self._matricula_value(self._find("Matricula"))
        curso = self._first_sequencia_palavras(self._find("DadosVinculo"))
        ira = self._first_token_value(self._find("IndicesAcademicos"), TokenType.T_NUMERO)

        disciplinas = [self._extract_disciplina(d) for d in self._find_all("Disciplina")]

        return {
            "nome": nome or "",
            "matricula": matricula or "",
            "curso": curso or "",
            "ira": self._to_float(ira),
            "disciplinas": disciplinas,
        }

    def _extract_disciplina(self, node: ParseNode) -> dict[str, Any]:
        codigo = self._first_token_value(node, TokenType.T_COD_DISCIPLINA) or ""
        nome = self._first_sequencia_palavras(node) or ""
        situacao = self._first_token_value(node, TokenType.T_SITUACAO_SIGLA) or ""
        return {
            "codigo": codigo,
            "nome": nome,
            "ch": self._carga_horaria(node),
            "situacao": situacao,
        }

    def _carga_horaria(self, node: ParseNode) -> Optional[int]:
        ch_raw = self._first_token_value(node, TokenType.T_CARGA_HORARIA)
        if ch_raw:
            return self._carga_to_int(ch_raw)
        campos = next(self._iter(node, "CamposNumericos"), None)
        if campos is None:
            return None
        numeros = [
            c.token.value
            for c in campos.children
            if c.token is not None and c.token.type == TokenType.T_NUMERO.value
        ]
        if not numeros:
            return None
        return self._carga_to_int(numeros[1] if len(numeros) > 1 else numeros[0])

    # 
    def _validate(self, student: dict[str, Any]) -> None:
        matricula = student["matricula"]
        # matriculas tanto 8 e 11 digitos
        if matricula and (not matricula.isdigit() or not (8 <= len(matricula) <= 11)):
            self._err(f"Matrícula inválida: '{matricula}' (esperados 8 a 11 dígitos).")

        ira = student["ira"]
        if ira is not None and not (0.0 <= ira <= 10.0):
            self._err(f"IRA fora do intervalo esperado [0, 10]: {ira}.")

        known = set(SITUACAO_SIGLAS)
        for d in student["disciplinas"]:
            if d["ch"] is not None and d["ch"] <= 0:
                self._err(f"Carga horária inválida na disciplina {d['codigo']}: {d['ch']}.")
            if d["situacao"] and d["situacao"] not in known:
                self._err(
                    f"Situação desconhecida '{d['situacao']}' na disciplina {d['codigo']}."
                )

    def _err(self, message: str) -> None:
        self.errors.append(CompilerError(phase=PHASE_SEMANTIC, message=message))

    # utilitários (acessar a arvore sintática)
    def _find(self, symbol: str) -> Optional[ParseNode]:
        return next(self._iter(self.tree, symbol), None)

    def _find_all(self, symbol: str) -> list[ParseNode]:
        return list(self._iter(self.tree, symbol))

    def _iter(self, node: Optional[ParseNode], symbol: str):
        if node is None:
            return
        if node.symbol == symbol:
            yield node
        for child in node.children:
            yield from self._iter(child, symbol)

    def _matricula_value(self, node: Optional[ParseNode]) -> Optional[str]:
        if node is None:
            return None
        for tok in self._tokens(node):
            if tok.type in (TokenType.T_MATRICULA.value, TokenType.T_NUMERO.value):
                return tok.value
        return None

    def _first_token_value(self, node: Optional[ParseNode], ttype: TokenType) -> Optional[str]:
        if node is None:
            return None
        for tok in self._tokens(node):
            if tok.type == ttype.value:
                return tok.value
        return None

    def _first_sequencia_palavras(self, node: Optional[ParseNode]) -> Optional[str]:
        if node is None:
            return None
        seq = next(self._iter(node, "SequenciaPalavras"), None)
        if seq is None:
            return None
        words = [c.token.value for c in seq.children if c.token is not None]
        return " ".join(words) if words else None

    def _tokens(self, node: ParseNode):
        if node.token is not None:
            yield node.token
        for child in node.children:
            yield from self._tokens(child)

    @staticmethod
    def _to_float(raw: Optional[str]) -> Optional[float]:
        if not raw:
            return None
        try:
            return float(raw.replace(",", "."))
        except ValueError:
            return None

    @staticmethod
    def _carga_to_int(raw: str) -> Optional[int]:
        digits = "".join(c for c in raw if c.isdigit())
        return int(digits) if digits else None


def analyze(tree: ParseNode) -> tuple[dict[str, Any], Optional[dict[str, Any]], list[CompilerError]]:
    return SemanticAnalyzer(tree).analyze()
