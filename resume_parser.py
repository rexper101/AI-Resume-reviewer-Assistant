"""
resume_parser.py - Handles resume file upload and text extraction.
Supports PDF files with fallback error handling.
"""

import re
import io
import logging
from typing import Optional

# Import config
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import config

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file) -> str:
    """
    Extract raw text from a PDF file object.
    Tries multiple PDF libraries in order for robustness.

    Args:
        file: File-like object (from Streamlit uploader)

    Returns:
        Extracted text string
        
    Raises:
        ValueError: If no text could be extracted from any library
    """
    text = ""
    
    # Try pdfplumber first (better layout handling)
    try:
        import pdfplumber
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            logger.info("Successfully extracted text using pdfplumber")
            return text
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
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if text.strip():
            logger.info("Successfully extracted text using PyPDF2")
            return text
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
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if text.strip():
            logger.info("Successfully extracted text using pypdf")
            return text
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
    """
    # Remove excessive whitespace
    text = config.WHITESPACE_PATTERN.sub('\n\n', text)
    text = config.MULTI_SPACE_PATTERN.sub(' ', text)

    # Remove non-printable characters
    text = config.NON_PRINTABLE_PATTERN.sub(' ', text)

    # Fix common PDF extraction artifacts
    text = config.CAMELCASE_PATTERN.sub(r'\1 \2', text)

    return text.strip()


def detect_sections(text: str) -> dict:
    """
    Detect key sections in a resume using precompiled regex patterns.

    Args:
        text: Cleaned resume text

    Returns:
        Dict of detected section names and their content
    """
    sections = {}

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
            if re.match(r'^' + pattern + r'[\s:]*$', line_stripped, re.IGNORECASE):
                current_section = section_name
                sections[current_section] = []
                found_section = True
                logger.debug(f"Detected section: {section_name}")
                break

        if not found_section:
            sections.setdefault(current_section, []).append(line_stripped)

    # Convert lists to strings
    return {k: '\n'.join(v) for k, v in sections.items()}


def extract_contact_info(text: str) -> dict:
    """
    Extract contact information from resume text using precompiled patterns.

    Args:
        text: Resume text

    Returns:
        Dict with email, phone, linkedin, github, location
    """
    contact = {
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
        "location": None,
    }

    # Email
    email_match = re.search(config.CONTACT_PATTERNS["email"], text)
    if email_match:
        contact["email"] = email_match.group()

    # Phone
    phone_match = re.search(config.CONTACT_PATTERNS["phone"], text)
    if phone_match:
        contact["phone"] = phone_match.group().strip()

    # LinkedIn
    linkedin_match = re.search(config.CONTACT_PATTERNS["linkedin"], text, re.IGNORECASE)
    if linkedin_match:
        contact["linkedin"] = linkedin_match.group()

    # GitHub
    github_match = re.search(config.CONTACT_PATTERNS["github"], text, re.IGNORECASE)
    if github_match:
        contact["github"] = github_match.group()

    # Location
    location_match = re.search(config.CONTACT_PATTERNS["location"], text)
    if location_match:
        contact["location"] = location_match.group()

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

Data Scientist | DataStartup | 2021 - 2022
- Created recommendation system using collaborative filtering and matrix factorization
- Built automated ETL pipelines using Apache Airflow and Python
- Performed A/B testing and statistical analysis for product experiments
- Developed dashboards using Tableau and Power BI for business stakeholders

Data Analyst Intern | Analytics Co. | 2020 - 2021
- Analyzed large datasets using SQL and Python (Pandas, NumPy)
- Created data visualizations using Matplotlib, Seaborn, and Plotly
- Built automated reporting pipelines using Python scripts

EDUCATION
Bachelor of Science in Computer Science | Stanford University | 2020
- GPA: 3.8/4.0
- Relevant Coursework: Machine Learning, Statistics, Algorithms, Database Systems

TECHNICAL SKILLS
Programming: Python, SQL, R, Scala, Bash
ML/AI: Machine Learning, Deep Learning, NLP, Computer Vision, TensorFlow, PyTorch, Scikit-learn
Data: Pandas, NumPy, Spark, Hadoop, Kafka, ETL
Visualization: Matplotlib, Seaborn, Plotly, Tableau, Power BI
Cloud/DevOps: AWS (EC2, S3, SageMaker, Lambda), Docker, Kubernetes, CI/CD, Git
Databases: PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch

PROJECTS

Real-time Fraud Detection System
- Built ML pipeline detecting fraudulent transactions in real-time using Random Forest and XGBoost
- Achieved 99.2% precision and deployed on AWS using Docker and FastAPI
- Technologies: Python, Scikit-learn, AWS, Docker, Redis

Customer Segmentation Engine
- Developed K-Means and DBSCAN clustering models for customer behavior analysis
- Built interactive Streamlit dashboard for business stakeholders
- Technologies: Python, Pandas, Plotly, Streamlit, PostgreSQL

CERTIFICATIONS
- AWS Certified Machine Learning Specialty (2023)
- Google Professional Data Engineer (2022)
- TensorFlow Developer Certificate (2021)
"""
