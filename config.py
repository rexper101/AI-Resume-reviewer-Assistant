"""
config.py - Centralized configuration for the AI Resume Screening system.
Contains constants, regex patterns, and color schemes used across modules.
"""

import re
from typing import Dict, List, Pattern

# ── Color Scheme ───────────────────────────────────────────────────────────────
COLORS: Dict[str, str] = {
    "primary": "#0D9488",
    "secondary": "#0891B2",
    "accent": "#0F766E",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#3B82F6",
    "bg_dark": "#0F172A",
    "card_bg": "#FFFFFF",
    "text": "#0F172A",
    "text_muted": "#64748B",
    "grid": "#E2E8F0",
}

CHART_COLORS: List[str] = [
    "#14B8A6", "#06B6D4", "#8B5CF6", "#10B981", "#F59E0B",
    "#3B82F6", "#5EEAD4", "#F97316", "#84CC16", "#A78BFA"
]

# ── Resume Parser Patterns (Raw strings for compilation) ──────────────────────
_SECTION_PATTERNS_RAW: Dict[str, str] = {
    "contact": r"(contact|personal\s+info|contact\s+information)",
    "summary": r"(summary|objective|profile|about\s+me|professional\s+summary)",
    "experience": r"(experience|work\s+experience|employment|work\s+history|professional\s+experience)",
    "education": r"(education|academic|qualification|degrees?)",
    "skills": r"(skills|technical\s+skills|core\s+competencies|technologies|expertise)",
    "projects": r"(projects|personal\s+projects|key\s+projects|portfolio)",
    "certifications": r"(certifications?|certificates?|credentials|licenses?|achievements?)",
    "languages": r"(languages?)",
}

# Precompile section patterns for efficiency
SECTION_PATTERNS: Dict[str, Pattern] = {
    key: re.compile(pattern, re.IGNORECASE) 
    for key, pattern in _SECTION_PATTERNS_RAW.items()
}

_CONTACT_PATTERNS_RAW: Dict[str, str] = {
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "phone": r'(\+?[\d\s\-\(\)]{10,15})',
    "linkedin": r'linkedin\.com/in/[\w\-]+',
    "github": r'github\.com/[\w\-]+',
    "location": r'\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*,\s*(?:[A-Z]{2}|[A-Z][a-z]+))\b',
}

# Precompile contact patterns for efficiency
CONTACT_PATTERNS: Dict[str, Pattern] = {
    key: re.compile(pattern) 
    for key, pattern in _CONTACT_PATTERNS_RAW.items()
}

# ── Text Cleaning Patterns (Precompiled) ───────────────────────────────────────
WHITESPACE_PATTERN: Pattern = re.compile(r'\n{3,}')
MULTI_SPACE_PATTERN: Pattern = re.compile(r' {2,}')
NON_PRINTABLE_PATTERN: Pattern = re.compile(r'[^\x20-\x7E\n]')
CAMELCASE_PATTERN: Pattern = re.compile(r'([a-z])([A-Z])')

# ── Text Normalization Patterns ─────────────────────────────────────────────────
ALIAS_REPLACE_PATTERN: Pattern = re.compile(r'[/\\|]')
BRACKET_PATTERN: Pattern = re.compile(r'[\(\)\[\]\{\}]')
WHITESPACE_NORM_PATTERN: Pattern = re.compile(r'\s+')

# ── ATS Scoring Weights ─────────────────────────────────────────────────────────
SCORING_WEIGHTS: Dict[str, int] = {
    "keyword_optimization": 25,
    "skills_relevance": 20,
    "structure_quality": 20,
    "experience_section": 15,
    "education_section": 10,
    "contact_completeness": 5,
    "additional_sections": 5,
}

# Validate scoring weights sum to 100
assert sum(SCORING_WEIGHTS.values()) == 100, "Scoring weights must sum to 100"

# ── ATS Keywords ────────────────────────────────────────────────────────────────
ATS_KEYWORDS: List[str] = [
    "experience", "skills", "education", "projects", "achievements",
    "responsibilities", "accomplished", "developed", "implemented",
    "managed", "led", "created", "designed", "optimized", "improved",
    "collaborated", "delivered", "built", "deployed"
]

ACTION_VERBS: List[str] = [
    "built", "developed", "designed", "implemented", "optimized",
    "improved", "increased", "reduced", "led", "managed", "created",
    "deployed", "architected", "delivered", "automated", "accelerated"
]

# ── Feature Extraction ──────────────────────────────────────────────────────────
QUANTIFIED_PATTERN: Pattern = re.compile(r'\d+[\%\+xX]|\d+\s*(million|billion|thousand|k\b)')
DATE_PATTERN: Pattern = re.compile(r'(20\d{2})\s*[-–]\s*(20\d{2}|present|current)', re.IGNORECASE)
COMPANY_PATTERN: Pattern = re.compile(
    r'[A-Z][a-z]+(?:\s[A-Z][a-z]+)*(?:\s(?:Inc|LLC|Ltd|Corp|Co|Technologies|Solutions|Group)\.?)?'
)

# ── Interview Generation ────────────────────────────────────────────────────────
EXPERIENCE_LEVELS: Dict[str, str] = {
    "Fresher/Student": "basic",
    "Entry Level": "basic",
    "Junior": "basic",
    "Mid-Level": "intermediate",
    "Senior": "advanced",
    "Lead/Principal": "advanced"
}

# ── PDF Processing ─────────────────────────────────────────────────────────────
PDF_LIBRARIES: List[str] = ["pdfplumber", "PyPDF2", "pypdf"]
WORDS_PER_PAGE: int = 400  # Estimated for resumes
MAX_PDF_PAGES: int = 20  # Maximum pages to parse
MAX_TEXT_LENGTH: int = 50000  # Maximum characters to process

# ── Logging Configuration ───────────────────────────────────────────────────────
LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL: str = "INFO"

# ── Model Configuration ─────────────────────────────────────────────────────────
TFIDF_CONFIG: Dict[str, object] = {
    "stop_words": "english",
    "ngram_range": (1, 2),
    "max_features": 5000,
    "min_df": 1
}

ROLE_PREDICTOR_CONFIG: Dict[str, object] = {
    "tfidf_ngram": (1, 2),
    "tfidf_max_features": 3000,
    "logistic_regression": {
        "max_iter": 1000,
        "C": 1.0,
        "solver": "lbfgs",
        "random_state": 42
    },
    "random_forest": {
        "n_estimators": 100,
        "max_depth": 10,
        "random_state": 42,
    },
    "naive_bayes": {
        "alpha": 0.1
    }
}
