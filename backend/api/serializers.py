from __future__ import annotations

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from api.models import CompilationResult, CompilerError, Document

_PHASE_PT = {"lexical": "Léxica", "syntactic": "Sintática", "semantic": "Semântica"}

class UploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        name = value.name.lower()
        if not (name.endswith(".pdf") or name.endswith(".txt")):
            raise serializers.ValidationError(
                "Envie um arquivo .pdf (ou .txt para testes)."
            )
        return value


class DocumentListSerializer(serializers.ModelSerializer):
    """GET /api/histories/ — visão resumida."""

    fileName = serializers.CharField(source="filename")
    date = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = Document
        fields = ["id", "fileName", "date", "status"]


class CompilerErrorSerializer(serializers.ModelSerializer):
    fase = serializers.SerializerMethodField()
    mensagem = serializers.CharField(source="message")
    linha = serializers.IntegerField(source="line")

    class Meta:
        model = CompilerError
        fields = ["fase", "mensagem", "linha", "column"]

    def get_fase(self, obj: CompilerError) -> str:
        return _PHASE_PT.get(obj.phase, obj.phase)


class DocumentDetailSerializer(serializers.ModelSerializer):
    """GET /api/histories/{id}/ — visão completa, alinhada ao frontend."""

    fileName = serializers.CharField(source="filename")
    date = serializers.DateTimeField(source="created_at", read_only=True)
    symbolTable = serializers.SerializerMethodField()
    errors = CompilerErrorSerializer(many=True, read_only=True)
    studentData = serializers.SerializerMethodField()
    syntaxTree = serializers.SerializerMethodField()
    semanticAnalysis = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            "id",
            "fileName",
            "date",
            "status",
            "processing_time_ms",
            "engine_version",
            "symbolTable",
            "errors",
            "studentData",
            "syntaxTree",
            "semanticAnalysis",
        ]

    def _result(self, obj: Document) -> CompilationResult | None:
        return getattr(obj, "result", None)

    def get_symbolTable(self, obj: Document) -> list[dict]:
        result = self._result(obj)
        if not result:
            return []
        # mapear tokens do motor para a "tabela de simbolos do frontend.
        return [
            {
                "id": str(i + 1),
                "token": tok.get("type", ""),
                "valor": tok.get("value", ""),
                "linha": tok.get("line", 0),
                "tipo": tok.get("type", ""),
            }
            for i, tok in enumerate(result.tokens)
        ]

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_studentData(self, obj: Document):
        result = self._result(obj)
        return result.student_data if result else None

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_syntaxTree(self, obj: Document):
        result = self._result(obj)
        return result.syntax_tree if result else None

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_semanticAnalysis(self, obj: Document):
        result = self._result(obj)
        return result.semantic_analysis if result else {}
