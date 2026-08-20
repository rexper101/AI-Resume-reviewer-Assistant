"""
skill_extractor.py - NLP-based skill extraction from resume text.
Uses keyword matching, NLP preprocessing, and pattern recognition.
Implements caching for improved performance.
"""

import re
import logging
from typing import List, Dict, Tuple, Optional, Set
from collections import Counter
from functools import lru_cache

# Import dataset
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from datasets.job_descriptions import SKILLS_TAXONOMY

logger = logging.getLogger(__name__)

# ── Master skills list (flattened from taxonomy) ──────────────────────────────
ALL_SKILLS: List[str] = []
for category, skills in SKILLS_TAXONOMY.items():
    ALL_SKILLS.extend(skills)
ALL_SKILLS = list(set(ALL_SKILLS))

# Skills that need exact phrase matching (multi-word)
MULTI_WORD_SKILLS: List[str] = [s for s in ALL_SKILLS if ' ' in s]
SINGLE_WORD_SKILLS: List[str] = [s for s in ALL_SKILLS if ' ' not in s]

# Precompile skill patterns for efficiency
MULTI_WORD_PATTERNS: List[re.Pattern] = [re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE) 
                                         for skill in MULTI_WORD_SKILLS]
SINGLE_WORD_PATTERNS: List[re.Pattern] = [re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE) 
                                          for skill in SINGLE_WORD_SKILLS]

# Additional skill aliases / synonyms
SKILL_ALIASES: Dict[str, str] = {
    "ml": "machine learning",
    "dl": "deep learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "tf": "tensorflow",
    "sk-learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "gcp": "google cloud",
    "k8s": "kubernetes",
    "pg": "postgresql",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "hf": "hugging face",
    "lc": "langchain",
    "llms": "llm",
    "bert": "transformers",
    "gpt": "llm",
    "openai": "openai",
    "aws sagemaker": "aws",
    "amazon web services": "aws",
    "microsoft azure": "azure",
    "google cloud platform": "google cloud",
    "node": "node.js",
    "nodejs": "node.js",
    "vue": "vue.js",
    "next": "next.js",
    "angular js": "angular",
    "spring": "spring boot",
    "power bi": "power bi",
    "powerbi": "power bi",
    "tableau desktop": "tableau",
    "ms excel": "excel",
    "github actions": "ci/cd",
    "gitlab ci": "ci/cd",
    "jenkins": "ci/cd",
}

# Precompile alias patterns
_ALIAS_PATTERNS: Dict[str, re.Pattern] = {
    alias: re.compile(r'\b' + re.escape(alias) + r'\b', re.IGNORECASE) 
    for alias in SKILL_ALIASES.keys()
}


@lru_cache(maxsize=128)
def preprocess_text(text: str) -> str:
    """
    Lowercase and normalize text for skill matching.
    Uses LRU cache for repeated inputs.
    
    Args:
        text: Input text to preprocess
    
    Returns:
        Normalized text
    """
    if not text:
        return ""
    
    text = text.lower().strip()
    # Normalize punctuation
    text = re.sub(r'[/\\|]', ' ', text)
    text = re.sub(r'[\(\)\[\]\{\}]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


@lru_cache(maxsize=128)
def apply_aliases(text: str) -> str:
    """
    Replace skill aliases with canonical names using precompiled patterns.
    Uses LRU cache for repeated inputs.
    
    Args:
        text: Input text with potential aliases
    
    Returns:
        Text with aliases replaced
    """
    if not text:
        return ""
    
    result = text
    for alias, pattern in _ALIAS_PATTERNS.items():
        canonical = SKILL_ALIASES[alias]
        result = pattern.sub(canonical, result)
    return result


def extract_skills_by_keyword(text: str) -> List[str]:
    """
    Extract skills using keyword matching against the skills taxonomy.
    Uses precompiled regex patterns for efficiency.

    Args:
        text: Resume text

    Returns:
        List of detected skill names (sorted)
        
    Raises:
        ValueError: If text is None or empty
    """
    if not text:
        logger.warning("Cannot extract skills from empty text")
        return []
    
    try:
        processed = preprocess_text(text)
        processed = apply_aliases(processed)

        found_skills: Set[str] = set()

        # Match multi-word skills first (higher priority)
        for skill, pattern in zip(MULTI_WORD_SKILLS, MULTI_WORD_PATTERNS):
            if pattern.search(processed):
                found_skills.add(skill)

        # Match single-word skills
        for skill, pattern in zip(SINGLE_WORD_SKILLS, SINGLE_WORD_PATTERNS):
            if pattern.search(processed):
                found_skills.add(skill)

        result = sorted(list(found_skills))
        logger.debug(f"Extracted {len(result)} unique skills from text")
        return result
    except Exception as e:
        logger.error(f"Error extracting skills: {e}")
        return []


def extract_skills_by_section(sections: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Extract skills from specific resume sections with weighted importance.

    Args:
        sections: Dict of resume sections from resume_parser

    Returns:
        Dict mapping section → skills found
    """
    