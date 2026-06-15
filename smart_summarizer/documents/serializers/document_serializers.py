from rest_framework import serializers
from documents.models import Document


class DocumentUploadSerializer(serializers.Serializer):
    """
    Validates multi-file upload.
    Accepts one or more files under the 'files' key.
    """
    files = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=False,
        help_text="One or more files to upload (PDF, DOCX, XLSX, CSV, TXT, JSON, XML, HTML).",
    )


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
            "id",
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
            "id",
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


class BulkUploadResultSerializer(serializers.Serializer):
    """
    Per-file result in a bulk upload response.
    On success: document data is populated, error is null.
    On failure: document is null, error has the message.
    """
    filename = serializers.CharField()
    success = serializers.BooleanField()
    error = serializers.CharField(allow_null=True)
    document = DocumentDetailSerializer(allow_null=True)
