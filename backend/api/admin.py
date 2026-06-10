from django.contrib import admin

from api.models import CompilationResult, CompilerError, Document


class CompilerErrorInline(admin.TabularInline):
    model = CompilerError
    extra = 0
    readonly_fields = ("phase", "message", "line", "column")


class CompilationResultInline(admin.StackedInline):
    model = CompilationResult
    extra = 0
    readonly_fields = ("success", "semantic_analysis", "student_data")


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("filename", "status", "processing_time_ms", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("filename", "content_hash")
    readonly_fields = ("id", "content_hash", "raw_text", "engine_version", "created_at", "updated_at")
    inlines = [CompilationResultInline, CompilerErrorInline]


@admin.register(CompilerError)
class CompilerErrorAdmin(admin.ModelAdmin):
    list_display = ("document", "phase", "line", "message")
    list_filter = ("phase",)
