"""
recommender.py - Job recommendation engine using TF-IDF and Cosine Similarity.
Compares resume skills against job descriptions to find best role matches.
"""

import logging
from typing import List, Dict, Tuple, Optional

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from datasets.job_descriptions import JOB_ROLES
import config

logger = logging.getLogger(__name__)

# Recommendation score weights and constants
TFIDF_WEIGHT = 0.6
SKILL_OVERLAP_WEIGHT = 0.4
MAX_MATCH_PERCENTAGE = 99
TOP_MISSING_SKILLS_DISPLAY = 8
TOP_MATCHED_SKILLS_DISPLAY = 5
TOP_MISSING_SKILLS_EXPLANATION = 3
MATCH_SCORE_EXCELLENT = 80
MATCH_SCORE_GOOD = 60
MATCH_SCORE_FAIR = 40

# Cache for job corpus to avoid rebuilding on every recommendation
_JOB_CORPUS_CACHE: Optional[Tuple[List[str], List[str]]] = None


def normalize_skills(skills: List[str]) -> List[str]:
    """
    Normalize skill list to lowercase for consistent comparison.

    Args:
        skills: List of skill strings

    Returns:
        Lowercase normalized skills
    """
    return [s.lower() for s in skills]


def build_skill_text(skills: List[str]) -> str:
    """
    Convert skill list to a single text string for TF-IDF processing.
    Repeats high-frequency skills for better weighting.

    Args:
        skills: List of skill strings

    Returns:
        Space-joined skill string
    """
    return ' '.join(skills).lower()


def build_job_corpus() -> Tuple[List[str], List[str]]:
    """
    Build a text corpus from job descriptions for TF-IDF vectorization.
    Results are cached to avoid rebuilding on every call.

    Returns:
        Tuple of (job_names, job_texts)
    """
    global _JOB_CORPUS_CACHE
    
    # Return cached corpus if available
    if _JOB_CORPUS_CACHE is not None:
        logger.debug("Using cached job corpus")
        return _JOB_CORPUS_CACHE
    
    job_names = []
    job_texts = []

    try:
        for role_name, role_data in JOB_ROLES.items():
            job_names.append(role_name)
            # Combine description + required skills (repeated for weight)
            skill_text = ' '.join(role_data["required_skills"] * 3)
            desc_text = role_data["description"].lower()
            combined = f"{desc_text} {skill_text}"
            job_texts.append(combined)

        _JOB_CORPUS_CACHE = (job_names, job_texts)
        logger.debug(f"Built and cached job corpus with {len(job_names)} roles")
    except KeyError as e:
        logger.error(f"Missing required field in JOB_ROLES: {e}")
        raise ValueError(f"Invalid job role data structure: {e}")

    return job_names, job_texts


def match_skills(required_skills: List[str], resume_skills_normalized: List[str]) -> Tuple[List[str], List[str]]:
    """
    Match required skills against normalized resume skills.

    Args:
        required_skills: List of required skills
        resume_skills_normalized: Already normalized (lowercase) resume skills

    Returns:
        Tuple of (matched_skills, missing_skills)
    """
    matched = [s for s in required_skills if s in resume_skills_normalized]
    missing = [s for s in required_skills if s not in resume_skills_normalized]
    return matched, missing


def compute_recommendations(resume_text: str, extracted_skills: List[str]) -> List[Dict]:
    """
    Compute job recommendations using TF-IDF cosine similarity.

    Args:
        resume_text: Full resume text
        extracted_skills: List of skills extracted from the resume

    Returns:
        List of job recommendations sorted by match score
    """
    if not resume_text or not extracted_skills:
        logger.warning("Empty resume_text or extracted_skills provided")
        return []

    # Prepare resume text (combine full text + repeated skills for emphasis)
    skill_emphasis = ' '.join(extracted_skills * 2)
    resume_query = f"{resume_text.lower()} {skill_emphasis}"

    # Build job corpus
    try:
        job_names, job_texts = build_job_corpus()
    except ValueError as e:
        logger.error(f"Failed to build job corpus: {e}")
        return []

    # Fit TF-IDF vectorizer on job corpus + resume
    all_texts = job_texts + [resume_query]

    try:
        vectorizer = TfidfVectorizer(**config.TFIDF_CONFIG)
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        logger.debug("TfidfVectorizer with full config succeeded")
    except Exception as e:
        logger.warning(f"Full TfidfVectorizer config failed ({e}), using simpler config")
        try:
            # Fallback to simpler vectorizer
            vectorizer = TfidfVectorizer(stop_words='english', max_features=2000)
            tfidf_matrix = vectorizer.fit_transform(all_texts)
            logger.info("Using simplified TfidfVectorizer")
        except Exception as e2:
            logger.error(f"Both vectorizers failed: {e2}")
            return []

    # Resume is the last document
    job_vectors = tfidf_matrix[:-1]
    resume_vector = tfidf_matrix[-1]

    # Compute cosine similarity
    similarities = cosine_similarity(resume_vector, job_vectors)[0]

    # Build recommendations list
    recommendations = []
    resume_skills_lower = normalize_skills(extracted_skills)

    for i, (job_name, score) in enumerate(zip(job_names, similarities)):
        try:
            role_data = JOB_ROLES[job_name]
            required_skills = role_data.get("required_skills", [])

            # Compute skill overlap
            matched_skills, missing_skills = match_skills(required_skills, resume_skills_lower)

            # Skill overlap ratio
            overlap_ratio = len(matched_skills) / len(required_skills) if required_skills else 0

            # Combined score: TFIDF_WEIGHT% TF-IDF similarity + SKILL_OVERLAP_WEIGHT% skill overlap
            combined_score = (TFIDF_WEIGHT * float(score)) + (SKILL_OVERLAP_WEIGHT * overlap_ratio)
            match_percentage = min(MAX_MATCH_PERCENTAGE, round(combined_score * 100))

            recommendations.append({
                "role": job_name,
                "match_percentage": match_percentage,
                "tfidf_score": round(float(score), 4),
                "skill_overlap_ratio": round(overlap_ratio, 4),
                "matched_skills": matched_skills,
                "missing_skills": missing_skills[:TOP_MISSING_SKILLS_DISPLAY],
                "required_skills": required_skills,
                "nice_to_have": role_data.get("nice_to_have", []),
                "experience_years": role_data.get("experience_years", "N/A"),
                "salary_range": role_data.get("salary_range", "N/A"),
                "category": role_data.get("category", "General"),
            })
        except KeyError as e:
            logger.error(f"Missing field for role {job_name}: {e}")
            continue

    # Sort by match percentage
    recommendations.sort(key=lambda x: x["match_percentage"], reverse=True)
    logger.info(f"Generated {len(recommendations)} recommendations")
    return recommendations


def get_top_recommendations(resume_text: str, extracted_skills: List[str], top_n: int = 5) -> List[Dict]:
    """
    Get top N job recommendations for a resume.

    Args:
        resume_text: Full resume text
        extracted_skills: Skills extracted from resume
        top_n: Number of top recommendations to return (default: 5)

    Returns:
        Top N recommendations ordered by match percentage
        
    Raises:
        ValueError: If top_n is not a positive integer
    """
    if not isinstance(top_n, int) or top_n < 1:
        logger.error(f"Invalid top_n value: {top_n}")
        raise ValueError("top_n must be a positive integer")
    
    all_recs = compute_recommendations(resume_text, extracted_skills)
    result = all_recs[:top_n]
    logger.debug(f"Returning top {len(result)} of {len(all_recs)} recommendations")
    return result


def explain_recommendation(recommendation: Dict, extracted_skills: List[str]) -> str:
    """
    Generate a human-readable explanation for why a role was recommended.

    Args:
        recommendation: Single recommendation dict with match details
        extracted_skills: All skills from resume (unused, kept for API compatibility)

    Returns:
        Markdown-formatted explanation string
    """
    role = recommendation.get("role", "Unknown Role")
    match_pct = recommendation.get("match_percentage", 0)
    matched = recommendation.get("matched_skills", [])
    missing = recommendation.get("missing_skills", [])

    explanation = f"**Why {role}?**\n\n"
    explanation += f"Your resume matches **{match_pct}%** of the requirements for this role.\n\n"

    if matched:
        top_matched = matched[:TOP_MATCHED_SKILLS_EXPLANATION]
        explanation += f"✅ **Key skills you have:** {', '.join(top_matched)}\n\n"

    if missing:
        top_missing = missing[:TOP_MISSING_SKILLS_EXPLANATION]
        explanation += f"📚 **Skills to develop:** {', '.join(top_missing)}\n\n"

    # Match quality assessment
    if match_pct >= MATCH_SCORE_EXCELLENT:
        explanation += "🌟 **Excellent match!** You're strongly qualified for this role."
    elif match_pct >= MATCH_SCORE_GOOD:
        explanation += "👍 **Good match.** With a few more skills, you'd be a strong candidate."
    elif match_pct >= MATCH_SCORE_FAIR:
        explanation += "📈 **Fair match.** Focus on the missing skills to improve your candidacy."
    else:
        explanation += "🎯 **Aspirational match.** This role requires significant additional skills."

    return explanation

