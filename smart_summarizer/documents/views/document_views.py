""" Document Views """

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from documents.models import Document
from documents.constants import PENDING
from documents.serializers import (
    BulkUploadResultSerializer,
    DocumentDetailSerializer,
    DocumentListSerializer,
    DocumentUploadSerializer,
)
from documents.services.document_upload_service import handle_bulk_upload, run_parser


# Upload file(s)

@extend_schema(
    request={'multipart/form-data': DocumentUploadSerializer},
    responses={201: BulkUploadResultSerializer(many=True)},
)
class DocumentUploadView(APIView):
    """
    Upload one or more files in any supported format.
    Each file is saved, parsed, and the per-file results are returned.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = DocumentUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        files = serializer.validated_data["files"]
        results = handle_bulk_upload(user=request.user, files=files)

        response_serializer = BulkUploadResultSerializer(
            results, many=True, context={"request": request}
        )
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


# List my documents (history)

class DocumentListView(ListAPIView):
    """
    List all documents uploaded by the logged-in user.
    Supports search via ?search= on original_name and file_type.
    """
    serializer_class = DocumentListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only return documents belonging to the current user."""
        queryset = Document.objects.filter(uploaded_by=self.request.user)

        # Optional filters via query params
        file_type = self.request.query_params.get("file_type")
        parse_status = self.request.query_params.get("status")
        search = self.request.query_params.get("search")

        if file_type:
            queryset = queryset.filter(file_type=file_type)
        if parse_status:
            queryset = queryset.filter(parse_status=parse_status)
        if search:
            queryset = queryset.filter(original_name__icontains=search)

        return queryset


# View a single document (with parsed text)

class DocumentDetailView(RetrieveAPIView):
    """
    View full details of a single document, including the parsed text.
    """
    serializer_class = DocumentDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "document_id"

    def get_queryset(self):
        """Only return documents belonging to the current user."""
        return Document.objects.filter(uploaded_by=self.request.user)


# Delete a document

class DocumentDeleteView(DestroyAPIView):
    """
    Delete a document. Only the owner can delete it.
    """
    permission_classes = [IsAuthenticated]
    lookup_field = "document_id"

    def get_queryset(self):
        """Only return documents belonging to the current user."""
        return Document.objects.filter(uploaded_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        doc_name = instance.original_name

        # Delete the actual file from disk
        if instance.file:
            try:
                instance.file.delete(save=False)
            except Exception:
                pass

        # Delete the database record
        instance.delete()

        return Response(
            {"detail": f"Document '{doc_name}' deleted successfully."},
            status=status.HTTP_200_OK,
        )


# Re-parse an existing document

class DocumentReparseView(APIView):
    """
    Re-run the parser on an existing document.
    Useful if parsing failed and you want to retry
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, document_id):
        try:
            document = Document.objects.get(
                document_id=document_id,
                uploaded_by=request.user,
            )
        except Document.DoesNotExist:
            return Response(
                {"detail": "Document not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Reset status and re-run
        document.parse_status = PENDING
        document.parsed_text = ""
        document.parse_error = ""
        document.save(update_fields=["parse_status", "parsed_text", "parse_error"])

        run_parser(document)

        serializer = DocumentDetailSerializer(document, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)
