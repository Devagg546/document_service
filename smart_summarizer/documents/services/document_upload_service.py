""" Upload Service """

import os
from django.conf import settings
from documents.models import Document
from documents.constants import PENDING, SUCCESS, FAILED
from documents.services.document_parser_service import detect_file_type, parse_document


def get_max_upload_size():
    """ get max upload size from settings (default 25 MB)."""
    return getattr(settings, "MAX_UPLOAD_SIZE", 25 * 1024 * 1024)


def validate_file(uploaded_file):
    """
    Basic checks before we accept the file.
    Returns (is_valid, error_message).
    """
    if not uploaded_file:
        return False, "No file was provided."

    if uploaded_file.size == 0:
        return False, "The uploaded file is empty."

    max_size = get_max_upload_size()
    if uploaded_file.size > max_size:
        max_mb = max_size / (1024 * 1024)
        return False, f"File is too large. Maximum allowed size is {max_mb:.0f} MB."

    # Check if we can parse this type
    file_type = detect_file_type(uploaded_file.name)
    if not file_type:
        return False, (
            f"Unsupported file format: '{uploaded_file.name}'. "
            "Supported formats: PDF, DOCX, XLSX, CSV, TXT, JSON, XML, HTML."
        )

    return True, None


def handle_upload(user, uploaded_file):
    """
    saves it, parses it, and returns the Document object.

    Raises:
        ValueError: If the file fails validation.
    """
    # 1. Validate
    is_valid, error_message = validate_file(uploaded_file)
    if not is_valid:
        raise ValueError(error_message)

    #2. Detect file type
    file_type = detect_file_type(uploaded_file.name)

    # 3: Create the document record (status starts as "pending")
    document = Document(
        uploaded_by=user,
        original_name=uploaded_file.name,
        file=uploaded_file,
        file_type=file_type,
        file_size=uploaded_file.size,
        parse_status=PENDING,
    )
    document.save()

    # 4 - Parse the file
    run_parser(document)

    return document


def handle_bulk_upload(user, files):
    """
    Process multiple files in one request.
    Returns a list of per-file result dicts:
        {"filename": str, "success": bool, "error": str|None, "document": Document|None}
    """
    results = []
    for uploaded_file in files:
        try:
            document = handle_upload(user, uploaded_file)
            results.append({
                "filename": uploaded_file.name,
                "success": True,
                "error": None,
                "document": document,
            })
        except (ValueError, Exception) as e:
            results.append({
                "filename": uploaded_file.name,
                "success": False,
                "error": str(e),
                "document": None,
            })
    return results


def run_parser(document):
    """
    Run  parser on document.
    Updates parse_status and parsed_text in place.
    This is separated so we can re-run it ("reparse" endpoint).
    """
    try:
        file_path = document.file.path
        parsed_text, _ = parse_document(file_path, file_type=document.file_type)

        # Success — store the text
        document.parsed_text = parsed_text
        document.parse_status = SUCCESS
        document.parse_error = ""
        document.save(update_fields=["parsed_text", "parse_status", "parse_error", "updated_at"])

    except Exception as e:
        # Failed — store the error
        document.parse_status = FAILED
        document.parse_error = str(e)
        document.save(update_fields=["parse_status", "parse_error", "updated_at"])
