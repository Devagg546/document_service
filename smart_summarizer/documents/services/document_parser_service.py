"""
Parser Service
"""

import json
import os
import fitz  # PyMuPDF
import pandas as pd
import chardet
from lxml import etree
from lxml import html
from docx import Document as DocxDocument



# 1. Figure out what type of file this is

# Map file extensions
EXTENSION_MAP = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".doc": "doc",
    ".xlsx": "xlsx",
    ".xls": "xls",
    ".csv": "csv",
    ".txt": "txt",
    ".log": "txt",
    ".md": "txt",
    ".json": "json",
    ".xml": "xml",
    ".html": "html",
    ".htm": "html",
}

SUPPORTED_TYPES = set(EXTENSION_MAP.values())


def detect_file_type(filename):
    """
    Look file extension and return a type string.
    Returns None if the extension is not recognized.
    """
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    return EXTENSION_MAP.get(ext)


# 2: One parser function per format

def parse_pdf(file_path):
    """Extract text from a PDF using PyMuPDF (fitz)."""

    text_parts = []
    with fitz.open(file_path) as doc:
        for page_number, page in enumerate(doc, start=1):
            page_text = page.get_text()
            if page_text.strip():
                text_parts.append(f"--- Page {page_number} ---\n{page_text}")

    return "\n\n".join(text_parts) if text_parts else "(No readable text found in PDF)"


def parse_docx(file_path):
    """Extract text from a DOCX file using python-docx."""

    doc = DocxDocument(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs) if paragraphs else "(No readable text found in DOCX)"


def parse_xlsx(file_path):
    """Extract text from an Excel file using pandas."""

    text_parts = []
    # Read all sheets
    sheets = pd.read_excel(file_path, sheet_name=None, dtype=str)
    for sheet_name, df in sheets.items():
        df = df.fillna("")
        sheet_text = f"--- Sheet: {sheet_name} ---\n"
        sheet_text += df.to_string(index=False)
        text_parts.append(sheet_text)

    return "\n\n".join(text_parts) if text_parts else "(No readable data found in Excel file)"


def parse_csv(file_path):
    """Extract text from a CSV file using pandas."""

    df = pd.read_csv(file_path, dtype=str)
    df = df.fillna("")
    text = df.to_string(index=False)
    return text if text.strip() else "(No readable data found in CSV)"


def parse_txt(file_path):
    """Read a plain text file. Handles encoding detection."""

    # First, detect the encoding
    with open(file_path, "rb") as f:
        raw_bytes = f.read()

    detected = chardet.detect(raw_bytes)
    encoding = detected.get("encoding", "utf-8") or "utf-8"

    text = raw_bytes.decode(encoding, errors="replace")
    return text if text.strip() else "(Empty text file)"


def parse_json(file_path):
    """Read a JSON file and return it as formatted text."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return json.dumps(data, indent=2, ensure_ascii=False)


def parse_xml(file_path):
    """Extract all text content from an XML file using lxml."""

    tree = etree.parse(file_path)
    # Get all text nodes, join them
    text_parts = []
    for element in tree.iter():
        if element.text and element.text.strip():
            text_parts.append(element.text.strip())
        if element.tail and element.tail.strip():
            text_parts.append(element.tail.strip())

    return "\n".join(text_parts) if text_parts else "(No readable text found in XML)"


def parse_html(file_path):
    """Extract visible text from an HTML file using lxml."""

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    tree = html.fromstring(content)
    # text_content() pulls all visible text
    text = tree.text_content()
    # Clean up excessive whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines) if lines else "(No readable text found in HTML)"


# 3 Main dispatcher — call the right parser

# Map type names to their parser functions
PARSERS = {
    "pdf": parse_pdf,
    "docx": parse_docx,
    "doc": parse_docx,       
    "xlsx": parse_xlsx,
    "xls": parse_xlsx,
    "csv": parse_csv,
    "txt": parse_txt,
    "json": parse_json,
    "xml": parse_xml,
    "html": parse_html,
}


def parse_document(file_path, file_type=None):
    """
    Give it a file path, it figures out the format and extracts text.

    Raises:
        ValueError: If the file type is not supported.
        FileNotFoundError: If the file doesn't exist.
    """
    # Make sure the file actually exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Figure out the type if not provided
    if not file_type:
        file_type = detect_file_type(file_path)

    if not file_type or file_type not in PARSERS:
        supported = ", ".join(sorted(SUPPORTED_TYPES))
        raise ValueError(
            f"Unsupported file type: '{file_type or 'unknown'}'. "
            f"Supported types: {supported}"
        )

    # Call the right parser
    parser_fn = PARSERS[file_type]
    parsed_text = parser_fn(file_path)

    return parsed_text, file_type
