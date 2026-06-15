import uuid

from django.db import models
from django.utils.timezone import now
from user.models import User
from documents.constants import PENDING, SUCCESS, FAILED, STATUS_CHOICES


def user_document_path(instance, filename):
    """
    Files go to: media/documents/<user_id>/<filename>
    Each user gets their own folder so files don't collide.
    """
    return f"documents/{instance.uploaded_by.user_id}/{filename}"


class Document(models.Model):
    """
    Tracks every file a user uploads.
    After upload, the parser extracts raw text into `parsed_text`.
    """

    # WHO uploaded it
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    # WHAT was uploaded
    document_id = models.BigAutoField(primary_key=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    original_name = models.CharField(max_length=255, help_text="Original filename the user uploaded.")
    file = models.FileField(upload_to=user_document_path)
    file_type = models.CharField(max_length=20, blank=True, help_text="Detected type: pdf, docx, csv, etc.")
    file_size = models.PositiveIntegerField(default=0, help_text="File size in bytes.")

    # PARSED OUTPUT
    parsed_text = models.TextField(blank=True, default="", help_text="Raw text extracted by the parser.")
    parse_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    parse_error = models.TextField(blank=True, default="", help_text="Error message if parsing failed.")

    # TIMESTAMPS
    uploaded_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "documents"
        ordering = ["uploaded_at"]

    def __str__(self):
        return f"{self.original_name} ({self.file_type}) — {self.parse_status}"
