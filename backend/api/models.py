from __future__ import annotations

import uuid
from django.db import models


class ProcessingStatus(models.TextChoices):
    PENDING = "pending", "Pendente"
    PROCESSING = "processing", "Processando"
    SUCCESS = "success", "Sucesso"
    ERROR = "error", "Erro"


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to="transcripts/")
    filename = models.CharField(max_length=255)
    content_hash = models.CharField(max_length=64, blank=True, db_index=True)
    status = models.CharField(
        max_length=20,
        choices=ProcessingStatus.choices,
        default=ProcessingStatus.PENDING,
    )
    raw_text = models.TextField(blank=True)
    engine_version = models.CharField(max_length=20, blank=True)
    processing_time_ms = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["-created_at"])]

    def __str__(self) -> str:
        return f"{self.filename} ({self.status})"


class CompilationResult(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name="result")
    success = models.BooleanField(default=False)
    tokens = models.JSONField(default=list)
    syntax_tree = models.JSONField(null=True, blank=True)
    semantic_analysis = models.JSONField(default=dict)
    student_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Resultado de {self.document_id} (success={self.success})"


class ErrorPhase(models.TextChoices):
    LEXICAL = "lexical", "Léxica"
    SYNTACTIC = "syntactic", "Sintática"
    SEMANTIC = "semantic", "Semântica"


class CompilerError(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="errors")
    phase = models.CharField(max_length=20, choices=ErrorPhase.choices)
    message = models.TextField()
    line = models.PositiveIntegerField(default=0)
    column = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["phase", "line"]

    def __str__(self) -> str:
        return f"[{self.phase}] L{self.line}: {self.message[:50]}"
