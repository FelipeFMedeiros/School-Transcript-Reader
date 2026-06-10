from __future__ import annotations

import hashlib
import time

from django.db import transaction

from compiler_engine import CompilerPipeline
from compiler_engine import __version__ as ENGINE_VERSION
from compiler_engine.exceptions import PdfExtractionError

from api.models import (
    CompilationResult,
    CompilerError,
    Document,
    ProcessingStatus,
)


def compute_hash(file_obj) -> str:
    """calcula o SHA-256 do arquivo """
    hasher = hashlib.sha256()
    for chunk in file_obj.chunks():
        hasher.update(chunk)
    file_obj.seek(0)
    return hasher.hexdigest()


@transaction.atomic
def process_document(document: Document) -> Document:
    """procesa documento"""
    document.status = ProcessingStatus.PROCESSING
    document.engine_version = ENGINE_VERSION
    document.save(update_fields=["status", "engine_version", "updated_at"])

    started = time.perf_counter()
    try:
        result = CompilerPipeline().run_result(document.file.path)
    except PdfExtractionError as exc:
        document.status = ProcessingStatus.ERROR
        document.processing_time_ms = int((time.perf_counter() - started) * 1000)
        document.save(update_fields=["status", "processing_time_ms", "updated_at"])
        CompilerError.objects.create(
            document=document,
            phase="lexical",
            message=f"Falha na extração do PDF: {exc}",
            line=0,
        )
        return document

    elapsed_ms = int((time.perf_counter() - started) * 1000)

    # persiste o resultado
    CompilationResult.objects.update_or_create(
        document=document,
        defaults={
            "success": result.success,
            "tokens": [t.to_dict() for t in result.tokens],
            "syntax_tree": result.syntax_tree.to_dict() if result.syntax_tree else None,
            "semantic_analysis": result.semantic_analysis,
            "student_data": result.student_data,
        },
    )

    # persiste os erros 
    document.errors.all().delete()
    CompilerError.objects.bulk_create(
        [
            CompilerError(
                document=document,
                phase=err.phase,
                message=err.message,
                line=err.line,
                column=err.column,
            )
            for err in result.errors
        ]
    )

    document.raw_text = result.raw_text
    document.processing_time_ms = elapsed_ms
    document.status = (
        ProcessingStatus.SUCCESS if result.success else ProcessingStatus.ERROR
    )
    document.save(
        update_fields=["raw_text", "processing_time_ms", "status", "updated_at"]
    )
    return document
