from __future__ import annotations

import unicodedata

from compiler_engine.dto import Token, CompilerError, ParseNode, PHASE_SYNTACTIC
from compiler_engine.tokens import TokenType


def _norm(text: str) -> str:
    #nomalizar o texto
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


_DISC_MARKERS = ("@", "&", "#", "§", "%", "*")
_SECTION_STOPS = ("Componentes", "Legenda")


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        # ignora tokens de erro léxico para o fluxo sintático.
        self.tokens = [t for t in tokens if t.type != TokenType.T_ERRO.value]
        self.pos = 0
        self.errors: list[CompilerError] = []

    @property
    def current(self) -> Token:
        return self.tokens[self.pos]

    def at_end(self) -> bool:
        return self.current.type == TokenType.T_EOF.value

    def advance(self) -> Token:
        tok = self.tokens[self.pos]
        if not self.at_end():
            self.pos += 1
        return tok

    def check_type(self, ttype: TokenType) -> bool:
        return self.current.type == ttype.value

    def check_keyword(self, *words: str) -> bool:
        return (
            self.current.type == TokenType.T_PALAVRA.value
            and _norm(self.current.value) in {_norm(w) for w in words}
        )

    def check_marker(self, *symbols: str) -> bool:
        return (
            self.current.type == TokenType.T_MARCADOR_LEGENDA.value
            and self.current.value in set(symbols)
        )

    def error(self, message: str) -> None:
        tok = self.current
        self.errors.append(
            CompilerError(
                phase=PHASE_SYNTACTIC,
                message=message,
                line=tok.line,
                column=tok.column,
            )
        )

    # ancora
    def skip_until_type(self, ttype: TokenType) -> bool:
        while not self.at_end():
            if self.check_type(ttype):
                return True
            self.advance()
        return False

    def skip_until_keyword(self, *words: str) -> bool:
        targets = {_norm(w) for w in words}
        while not self.at_end():
            if self.current.type == TokenType.T_PALAVRA.value and _norm(self.current.value) in targets:
                return True
            self.advance()
        return False

    def skip_until_type_bounded(self, ttype: TokenType, stops: tuple[str, ...] = _SECTION_STOPS) -> bool:
        start = self.pos
        stopset = {_norm(s) for s in stops}
        while not self.at_end():
            if self.check_type(ttype):
                return True
            if self.current.type == TokenType.T_PALAVRA.value and _norm(self.current.value) in stopset:
                break
            self.advance()
        self.pos = start
        return False

    def skip_until_keyword_bounded(self, *words: str, stops: tuple[str, ...] = _SECTION_STOPS) -> bool:
        start = self.pos
        targets = {_norm(w) for w in words}
        stopset = {_norm(s) for s in stops} - targets
        while not self.at_end():
            if self.current.type == TokenType.T_PALAVRA.value:
                n = _norm(self.current.value)
                if n in targets:
                    return True
                if n in stopset:
                    break
            self.advance()
        self.pos = start
        return False

    # consumo terminais
    def expect_type(self, ttype: TokenType, parent: ParseNode) -> bool:
        if self.check_type(ttype):
            parent.add(ParseNode.leaf(self.advance()))
            return True
        self.error(f"Esperado {ttype.value}, encontrado '{self.current.value}'.")
        return False

    def expect_keyword(self, word: str, parent: ParseNode) -> bool:
        if self.check_keyword(word):
            parent.add(ParseNode.leaf(self.advance()))
            return True
        self.error(f"Esperada a palavra '{word}', encontrado '{self.current.value}'.")
        return False

    def expect_marker(self, symbol: str, parent: ParseNode) -> bool:
        if self.check_marker(symbol):
            parent.add(ParseNode.leaf(self.advance()))
            return True
        self.error(f"Esperado '{symbol}', encontrado '{self.current.value}'.")
        return False

    def opt_marker(self, symbol: str, parent: ParseNode) -> None:
        if self.check_marker(symbol):
            parent.add(ParseNode.leaf(self.advance()))

    # regras
    def parse(self) -> tuple[ParseNode, list[CompilerError]]:
        root = ParseNode("Historico")
        self._dados_pessoais(root)
        self._dados_vinculo(root)
        self._indices_academicos(root)
        self._corpo_documento(root)
        return root, self.errors

    def _sequencia_palavras(self, parent: ParseNode, stop: set[str] | None = None) -> ParseNode:
        node = parent.add(ParseNode("SequenciaPalavras"))
        stop_norm = {_norm(s) for s in (stop or set())}
        consumed = False
        while self.check_type(TokenType.T_PALAVRA) and _norm(self.current.value) not in stop_norm:
            node.add(ParseNode.leaf(self.advance()))
            consumed = True
        if not consumed:
            self.error(f"Esperada ao menos uma palavra, encontrado '{self.current.value}'.")
        return node

    def _capturar_matricula(self, parent: ParseNode) -> None:
        if not self.skip_until_keyword_bounded("Matrícula"):
            return
        mat = parent.add(ParseNode("Matricula"))
        self.expect_keyword("Matrícula", mat)
        self.opt_marker(":", mat)
        if self.check_type(TokenType.T_MATRICULA) or self.check_type(TokenType.T_NUMERO):
            mat.add(ParseNode.leaf(self.advance()))

    def _dados_pessoais(self, root: ParseNode) -> None:
        node = root.add(ParseNode("DadosPessoais"))

        if self.skip_until_keyword("Nome"):
            self.expect_keyword("Nome", node)
            self.opt_marker(":", node)
            self._sequencia_palavras(node, stop={"Data", "Matrícula"})

        self._capturar_matricula(node)

        if self.skip_until_type_bounded(TokenType.T_DATA):
            self.expect_type(TokenType.T_DATA, node)

        if self.skip_until_type_bounded(TokenType.T_CPF):
            self.expect_type(TokenType.T_CPF, node)

    def _dados_vinculo(self, root: ParseNode) -> None:
        node = root.add(ParseNode("DadosVinculo"))

        if self.skip_until_keyword_bounded("Curso"):
            self.expect_keyword("Curso", node)
            self.opt_marker(":", node)
            self._sequencia_palavras(node, stop={"Status", "Ênfase", "Índices", "Componentes"})

        if self.check_keyword("Status"):
            self.expect_keyword("Status", node)
            self.opt_marker(":", node)
            if self.check_type(TokenType.T_PALAVRA):
                node.add(ParseNode.leaf(self.advance()))

    def _indices_academicos(self, root: ParseNode) -> None:
        node = root.add(ParseNode("IndicesAcademicos"))
        if self.skip_until_keyword_bounded("IRA"):
            self.expect_keyword("IRA", node)
            self.opt_marker(":", node)
            self.expect_type(TokenType.T_NUMERO, node)

    def _corpo_documento(self, root: ParseNode) -> None:
        node = root.add(ParseNode("CorpoDocumento"))
        if not self.skip_until_keyword("Componentes"):
            return
        self.expect_keyword("Componentes", node)
        if self.check_keyword("Curriculares"):
            self.advance()
        self._lista_disciplinas(node)

    def _lista_disciplinas(self, parent: ParseNode) -> None:
        node = parent.add(ParseNode("ListaDisciplinas"))
        current_period: Token | None = None
        pending_name: ParseNode | None = None

        while not self.at_end() and not self.check_keyword("Legenda"):
            if self.check_type(TokenType.T_PERIODO_LETIVO):
                current_period = self.advance()
                self._skip_leading_disc_marker()
                continue

            if self.check_type(TokenType.T_COD_DISCIPLINA):
                self._disciplina(node, current_period, pending_name)
                pending_name = None
                continue

            if self.check_type(TokenType.T_PALAVRA):
                seq, is_name = self._linha_texto()
                if is_name:
                    pending_name = seq
                continue

            self.advance()

    def _skip_leading_disc_marker(self) -> None:
        if self.check_marker(*_DISC_MARKERS):
            self.advance()
        elif self.check_type(TokenType.T_PALAVRA) and len(self.current.value) == 1:
            self.advance()

    def _linha_texto(self) -> tuple[ParseNode, bool]:
        line_no = self.current.line
        seq = ParseNode("SequenciaPalavras")
        has_carga = False
        while not self.at_end() and self.current.line == line_no:
            tok = self.advance()
            if tok.type == TokenType.T_PALAVRA.value:
                seq.add(ParseNode.leaf(tok))
            elif tok.type == TokenType.T_CARGA_HORARIA.value:
                has_carga = True
        is_name = bool(seq.children) and not has_carga
        return seq, is_name

    def _disciplina(
        self,
        parent: ParseNode,
        period_tok: Token | None,
        pending_name: ParseNode | None,
    ) -> None:
        node = parent.add(ParseNode("Disciplina"))
        if period_tok is not None:
            node.add(ParseNode.leaf(period_tok))

        self.expect_type(TokenType.T_COD_DISCIPLINA, node)

        inline = ParseNode("SequenciaPalavras")
        while self.check_type(TokenType.T_PALAVRA):
            inline.add(ParseNode.leaf(self.advance()))
        has_inline = bool(inline.children)

        if self.check_marker("("):
            self.advance()
            if self.check_type(TokenType.T_NUMERO):
                self.advance()
            if self.check_marker(")"):
                self.advance()

        campos = node.add(ParseNode("CamposNumericos"))
        while (
            self.check_type(TokenType.T_NUMERO)
            or self.check_type(TokenType.T_CARGA_HORARIA)
            or self.check_marker("-", ",", ".")
        ):
            campos.add(ParseNode.leaf(self.advance()))

        if self.check_type(TokenType.T_SITUACAO_SIGLA):
            node.add(ParseNode.leaf(self.advance()))
        elif self.check_keyword("Matriculado"):
            node.add(ParseNode.leaf(self.advance()))

        node.add(inline if has_inline or pending_name is None else pending_name)


def parse(tokens: list[Token]) -> tuple[ParseNode, list[CompilerError]]:
    return Parser(tokens).parse()
