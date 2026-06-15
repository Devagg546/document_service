from django.urls import path
from documents.views import (
    DocumentDeleteView,
    DocumentDetailView,
    DocumentListView,
    DocumentReparseView,
    DocumentUploadView,
)

urlpatterns = [
    # Upload file(s)
    path("documents/upload/", DocumentUploadView.as_view(), name="document-upload"),

    # List my documents (history)
    path("documents/", DocumentListView.as_view(), name="document-list"),

    # View a single document
    path("documents/<int:document_id>/", DocumentDetailView.as_view(), name="document-detail"),

    # Delete a document
    path("documents/<int:document_id>/delete/", DocumentDeleteView.as_view(), name="document-delete"),

    # Re-parse a document
    path("documents/<int:document_id>/reparse/", DocumentReparseView.as_view(), name="document-reparse"),
]
