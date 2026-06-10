from __future__ import annotations

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from api.models import Document, ProcessingStatus
from api.serializers import (
    DocumentDetailSerializer,
    DocumentListSerializer,
    UploadSerializer,
)
from api.services import compute_hash, process_document


class HistoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Document.objects.all().select_related("result").prefetch_related("errors")
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action == "list":
            return DocumentListSerializer
        if self.action == "create":
            return UploadSerializer
        return DocumentDetailSerializer

    @extend_schema(
        request=UploadSerializer,
        responses={201: DocumentDetailSerializer},
        summary="Envia um histórico (PDF) e executa o pipeline do compilador",
    )
    def create(self, request, *args, **kwargs):
        upload = UploadSerializer(data=request.data)
        upload.is_valid(raise_exception=True)
        file = upload.validated_data["file"]

        document = Document.objects.create(
            file=file,
            filename=file.name,
            content_hash=compute_hash(file),
            status=ProcessingStatus.PENDING,
        )

        process_document(document)
        document.refresh_from_db()

        output = DocumentDetailSerializer(document, context={"request": request})
        return Response(output.data, status=status.HTTP_201_CREATED)
