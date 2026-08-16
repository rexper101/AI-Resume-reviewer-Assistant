"""
resume_parser.py - Handles resume file upload and text extraction.
Supports PDF files with fallback error handling.
"""

import re
import io
import logging
from typing import Optional, Dict, BinaryIO

# Import config
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import config

logger = logging.getLogger(__name__)

# Maximum text length to prevent memory issues
MAX_TEXT_LENGTH = config.MAX_TEXT_LENGTH


def extract_text_from_pdf(file: BinaryIO) -> str:
    """
    Extract raw text from a PDF file object.
    Tries multiple PDF libraries in order for robustness.

    Args:
        file: File-like object (from Streamlit uploader)

    Returns:
        Extracted text string
        
    Raises:
        ValueError: If no text could be extracted from any library
        IOError: If file reading fails
    """
    if not file:
        raise ValueError("File object cannot be None")
    
    text = ""
    
    # Try pdfplumber first (better layout handling)
    try:
        import pdfplumber
        with pdfplumber.open(file) as pdf:
            # Safety check: don't process too many pages
            max_pages = min(len(pdf.pages), config.MAX_PDF_PAGES)
            for i, page in enumerate(pdf.pages[:max_pages]):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                        if len(text) > MAX_TEXT_LENGTH:
                            logger.warning(f"PDF text exceeds maximum length at page {i+1}")
                            break
                except Exception as page_err:
                    logger.debug(f"Failed to extract page {i+1} with pdfplumber: {page_err}")
                    continue
        
        if text.strip():
            logger.info("Successfully extracted text using pdfplumber")
            return text[:MAX_TEXT_LENGTH]
    except ImportError:
        logger.debug("pdfplumber not installed, trying next library")
    except Exception as e:
        logger.warning(f"pdfplumber extraction failed: {e}")
    
    # Fallback to PyPDF2
    try:
        import PyPDF2
        if hasattr(file, 'seek'):
            file.seek(0)
        reader = PyPDF2.PdfReader(file)
        max_pages = min(len(reader.pages), config.MAX_PDF_PAGES)
        
        for i, page in enumerate(reader.pages[:max_pages]):
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                    if len(text) > MAX_TEXT_LENGTH:
                        logger.warning(f"PDF text exceeds maximum length at page {i+1}")
                        break
            except Exception as page_err:
                logger.debug(f"Failed to extract page {i+1} with PyPDF2: {page_err}")
                continue
        
        if text.strip():
            logger.info("Successfully extracted text using PyPDF2")
            return text[:MAX_TEXT_LENGTH]
    except ImportError:
        logger.debug("PyPDF2 not installed, trying next library")
    except Exception as e:
        logger.warning(f"PyPDF2 extraction failed: {e}")
    
    # Final fallback: try pypdf
    try:
        from pypdf import PdfReader
        if hasattr(file, 'seek'):
            file.seek(0)
        reader = PdfReader(file)
        max_pages = min(len(reader.pages), config.MAX_PDF_PAGES)
        
        for i, page in enumerate(reader.pages[:max_pages]):
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                    if len(text) > MAX_TEXT_LENGTH:
                        logger.warning(f"PDF text exceeds maximum length at page {i+1}")
                        break
            except Exception as page_err:
                logger.debug(f"Failed to extract page {i+1} with pypdf: {page_err}")
                continue
        
        if text.strip():
            logger.info("Successfully extracted text using pypdf")
            return text[:MAX_TEXT_LENGTH]
    except ImportError:
        logger.debug("pypdf not installed")
    except Exception as e:
        logger.warning(f"pypdf extraction failed: {e}")
    
    # All methods failed
    error_msg = "Could not extract text from PDF using any available library"
    logger.error(error_msg)
    raise ValueError(error_msg)


def clean_resume_text(text: str) -> str:
    """
    Clean and normalize extracted resume text using precompiled patterns.

    Args:
        text: Raw extracted text

    Returns:
        Cleaned text
        
    Raises:
        ValueError: If input text is None or empty
    """
    if not text:
        raise ValueError("Input text cannot be None or empty")
    
    # Remove excessive whitespace
    text = config.WHITESPACE_PATTERN.sub('\n\n', text)
    text = config.MULTI_SPACE_PATTERN.sub(' ', text)

    # Remove non-printable characters
    text = config.NON_PRINTABLE_PATTERN.sub(' ', text)

    # Fix common PDF extraction artifacts
    text = config.CAMELCASE_PATTERN.sub(r'\1 \2', text)

    cleaned = text.strip()
    
    if not cleaned:
        logger.warning("Text cleaning resulted in empty string")
    
    return cleaned


def detect_sections(text: str) -> Dict[str, str]:
    """
    Detect key sections in a resume using precompiled regex patterns.

    Args:
        text: Cleaned resume text

    Returns:
        Dict of detected section names and their content
        
    Raises:
        ValueError: If input text is empty
    """
    if not text or not text.strip():
        raise ValueError("Cannot detect sections from empty text")
    
    sections: Dict[str, list] = {}

    lines = text.split('\n')
    current_section = "header"
    sections[current_section] = []

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue

        # Check if line is a section header using precompiled patterns
        found_section = False
        for section_name, pattern in config.SECTION_PATTERNS.items():
            if pattern.match(line_stripped.rstrip(':').rstrip()):
                current_section = section_name
                sections[current_section] = []
                found_section = True
                logger.debug(f"Detected section: {section_name}")
                break

        if not found_section:
            sections.setdefault(current_section, []).append(line_stripped)

    # Convert lists to strings
    return {k: '\n'.join(v) for k, v in sections.items()}


def extract_contact_info(text: str) -> Dict[str, Optional[str]]:
    """
    Extract contact information from resume text using precompiled patterns.

    Args:
        text: Resume text

    Returns:
        Dict with email, phone, linkedin, github, location
    """
    if not text:
        logger.warning("Cannot extract contact info from empty text")
        return {
            "email": None,
            "phone": None,
            "linkedin": None,
            "github": None,
            "location": None,
        }
    
    contact: Dict[str, Optional[str]] = {
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
        "location": None,
    }

    try:
        # Email
        email_match = config.CONTACT_PATTERNS["email"].search(text)
        if email_match:
            contact["email"] = email_match.group()

        # Phone
        phone_match = config.CONTACT_PATTERNS["phone"].search(text)
        if phone_match:
            contact["phone"] = phone_match.group().strip()

        # LinkedIn
        linkedin_match = config.CONTACT_PATTERNS["linkedin"].search(text.lower())
        if linkedin_match:
            contact["linkedin"] = linkedin_match.group()

        # GitHub
        github_match = config.CONTACT_PATTERNS["github"].search(text.lower())
        if github_match:
            contact["github"] = github_match.group()

        # Location
        location_match = config.CONTACT_PATTERNS["location"].search(text)
        if location_match:
            contact["location"] = location_match.group()
    except Exception as e:
        logger.error(f"Error extracting contact info: {e}")

    return contact


def calculate_resume_stats(text: str) -> dict:
    """
    Calculate basic statistics about the resume.

    Args:
        text: Resume text

    Returns:
        Dict with word count, page estimate, sections found
    """
    words = text.split()
    sections = detect_sections(text)

    # Estimate pages (average words per page from config)
    estimated_pages = max(1, round(len(words) / config.WORDS_PER_PAGE, 1))

    # Count years of experience from text
    year_matches = re.findall(r'\b(19|20)(\d{2})\b', text)
    unique_years = sorted(set([int(a + b) for a, b in year_matches]))

    has_sections = {
        "has_summary": "summary" in sections and len(sections.get("summary", "")) > 20,
        "has_experience": "experience" in sections and len(sections.get("experience", "")) > 20,
        "has_education": "education" in sections and len(sections.get("education", "")) > 20,
        "has_skills": "skills" in sections and len(sections.get("skills", "")) > 10,
        "has_projects": "projects" in sections and len(sections.get("projects", "")) > 20,
        "has_certifications": "certifications" in sections and len(sections.get("certifications", "")) > 10,
    }

    return {
        "word_count": len(words),
        "char_count": len(text),
        "estimated_pages": estimated_pages,
        "sections_detected": [k for k, v in has_sections.items() if v],
        **has_sections
    }


def parse_resume(file) -> dict:
    """
    Main function to parse a resume file and return structured data.

    Args:
        file: Uploaded file object from Streamlit

    Returns:
        Dict containing all parsed resume data
    """
    # Extract raw text
    raw_text = extract_text_from_pdf(file)

    if not raw_text.strip():
        raise ValueError("No text could be extracted from the PDF. The file may be scanned or image-based.")

    # Clean the text
    cleaned_text = clean_resume_text(raw_text)

    # Extract structured data
    sections = detect_sections(cleaned_text)
    contact_info = extract_contact_info(cleaned_text)
    stats = calculate_resume_stats(cleaned_text)

    return {
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "sections": sections,
        "contact_info": contact_info,
        "stats": stats
    }


def get_sample_resume_text() -> str:
    """
    Returns a sample resume text for demo purposes when no file is uploaded.
    """
    return """
John Smith
john.smith@email.com | +1-555-0123 | linkedin.com/in/johnsmith | github.com/johnsmith
San Francisco, CA

PROFESSIONAL SUMMARY
Passionate Data Scientist with 3+ years of experience building machine learning models and
data pipelines. Expertise in Python, SQL, and cloud technologies. Proven track record of
delivering end-to-end ML solutions from data collection to production deployment.

WORK EXPERIENCE

Senior Data Scientist | TechCorp Inc. | 2022 - Present
- Built and deployed machine learning models for customer churn prediction (92% accuracy)
- Developed NLP pipeline for sentiment analysis using BERT and TensorFlow
- Reduced data processing time by 60% using Apache Spark and AWS EMR
- Mentored junior data scientists and conducted code reviews

