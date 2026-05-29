from rest_framework import serializers
from documents.models import Document


class DocumentUploadSerializer(serializers.Serializer):
    """
    Validates the incoming file upload.
    Just the file field — everything else is handled by the upload service.
    """
    file = serializers.FileField(help_text="The file to upload (PDF, DOCX, XLSX, CSV, TXT, JSON, XML, HTML).")


class DocumentListSerializer(serializers.ModelSerializer):
    """
    For the history view — shows metadata but NOT the full parsed text.
    Keeps API responses light when listing many documents.
    """
    uploaded_by_name = serializers.CharField(source="uploaded_by.user_name", read_only=True)

    class Meta:
        model = Document
        fields = [
            "document_id",
            "original_name",
            "file_type",
            "file_size",
            "parse_status",
            "uploaded_by_name",
            "uploaded_at",
            "updated_at",
        ]
        read_only_fields = fields


class DocumentDetailSerializer(serializers.ModelSerializer):
    """
    For viewing a single document — includes the full parsed text.
    """
    uploaded_by_name = serializers.CharField(source="uploaded_by.user_name", read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            "document_id",
            "original_name",
            "file",
            "file_url",
            "file_type",
            "file_size",
            "parsed_text",
            "parse_status",
            "parse_error",
            "uploaded_by_name",
            "uploaded_at",
            "updated_at",
        ]
        read_only_fields = fields

    def get_file_url(self, obj):
        """Return the full URL to download the file."""
        request = self.context.get("request")
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
