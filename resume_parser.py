"""
resume_parser.py - Handles resume file upload and text extraction.
Supports PDF files with fallback error handling.
"""

import re
import io
from typing import Optional


def extract_text_from_pdf(file) -> str:
    """
    Extract raw text from a PDF file object.
    Tries pdfplumber first (better layout handling), falls back to PyPDF2.

    Args:
        file: File-like object (from Streamlit uploader)

    Returns:
        Extracted text string
    """
    text = ""

    # Try pdfplumber first (handles complex layouts better)
    try:
        import pdfplumber
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception:
        pass

    # Fallback to PyPDF2
    try:
        import PyPDF2
        if hasattr(file, 'seek'):
            file.seek(0)
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception:
        pass

    # Last fallback: try pypdf
    try:
        from pypdf import PdfReader
        if hasattr(file, 'seek'):
            file.seek(0)
        reader = PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        raise ValueError(f"Could not extract text from PDF: {str(e)}")

    return text


def clean_resume_text(text: str) -> str:
    """
    Clean and normalize extracted resume text.

    Args:
        text: Raw extracted text

    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)

    # Remove non-printable characters
    text = re.sub(r'[^\x20-\x7E\n]', ' ', text)

    # Fix common PDF extraction artifacts
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # camelCase splits

    return text.strip()


def detect_sections(text: str) -> dict:
    """
    Detect key sections in a resume using regex pattern matching.

    Args:
        text: Cleaned resume text

    Returns:
        Dict of detected section names and their content
    """
    sections = {}

    # Common section headers (case-insensitive)
    section_patterns = {
        "contact": r"(contact|personal\s+info|contact\s+information)",
        "summary": r"(summary|objective|profile|about\s+me|professional\s+summary)",
        "experience": r"(experience|work\s+experience|employment|work\s+history|professional\s+experience)",
        "education": r"(education|academic|qualification|degrees?)",
        "skills": r"(skills|technical\s+skills|core\s+competencies|technologies|expertise)",
        "projects": r"(projects|personal\s+projects|key\s+projects|portfolio)",
        "certifications": r"(certifications?|certificates?|credentials|licenses?|achievements?)",
        "languages": r"(languages?)",
    }

    lines = text.split('\n')
    current_section = "header"
    sections[current_section] = []

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue

        # Check if line is a section header
        found_section = False
        for section_name, pattern in section_patterns.items():
            if re.match(r'^' + pattern + r'[\s:]*$', line_stripped, re.IGNORECASE):
                current_section = section_name
                sections[current_section] = []
                found_section = True
                break

        if not found_section:
            sections.setdefault(current_section, []).append(line_stripped)

    # Convert lists to strings
    return {k: '\n'.join(v) for k, v in sections.items()}

"""
