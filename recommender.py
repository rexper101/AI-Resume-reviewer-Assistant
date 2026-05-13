"""
recommender.py - Job recommendation engine using TF-IDF and Cosine Similarity.
Compares resume skills against job descriptions to find best role matches.
"""

import re
import numpy as np
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from datasets.job_descriptions import JOB_ROLES


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

    Returns:
        Tuple of (job_names, job_texts)
    """
    job_names = []
    job_texts = []

    for role_name, role_data in JOB_ROLES.items():
        job_names.append(role_name)
        # Combine description + required skills (repeated for weight)
        skill_text = ' '.join(role_data["required_skills"] * 3)
        desc_text = role_data["description"].lower()
        combined = f"{desc_text} {skill_text}"
        job_texts.append(combined)

    return job_names, job_texts


def compute_recommendations(resume_text: str, extracted_skills: List[str]) -> List[Dict]:
    """
    Compute job recommendations using TF-IDF cosine similarity.

    Args:
        resume_text: Full resume text
        extracted_skills: List of skills extracted from the resume

    Returns:
        List of job recommendations sorted by match score
    """
    # Prepare resume text (combine full text + repeated skills for emphasis)
    skill_emphasis = ' '.join(extracted_skills * 2)
    resume_query = f"{resume_text.lower()} {skill_emphasis}"

    # Build job corpus
    job_names, job_texts = build_job_corpus()

    # Fit TF-IDF vectorizer on job corpus + resume
    all_texts = job_texts + [resume_query]

    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),  # unigrams and bigrams
        max_features=5000,
        min_df=1
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(all_texts)
    except Exception as e:
        # Fallback to simpler vectorizer
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Resume is the last document
    job_vectors = tfidf_matrix[:-1]
    resume_vector = tfidf_matrix[-1]

    # Compute cosine similarity
    similarities = cosine_similarity(resume_vector, job_vectors)[0]

    # Build recommendations list
    recommendations = []
    for i, (job_name, score) in enumerate(zip(job_names, similarities)):
        role_data = JOB_ROLES[job_name]

        # Compute skill overlap
        resume_skills_lower = [s.lower() for s in extracted_skills]
        required_skills = role_data["required_skills"]
        matched_skills = [s for s in required_skills if s in resume_skills_lower]
        missing_skills = [s for s in required_skills if s not in resume_skills_lower]

        # Skill overlap ratio
        overlap_ratio = len(matched_skills) / len(required_skills) if required_skills else 0

        # Combined score: 60% TF-IDF similarity + 40% skill overlap
        combined_score = (0.6 * float(score)) + (0.4 * overlap_ratio)
        match_percentage = min(99, round(combined_score * 100))

        recommendations.append({
            "role": job_name,
            "match_percentage": match_percentage,
            "tfidf_score": round(float(score), 4),
            "skill_overlap_ratio": round(overlap_ratio, 4),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills[:8],  # top 8 missing
            "required_skills": required_skills,
            "nice_to_have": role_data.get("nice_to_have", []),
            "experience_years": role_data.get("experience_years", "N/A"),
            "salary_range": role_data.get("salary_range", "N/A"),
            "category": role_data.get("category", "General"),
        })

    # Sort by match percentage
    recommendations.sort(key=lambda x: x["match_percentage"], reverse=True)
    return recommendations


def get_top_recommendations(resume_text: str, extracted_skills: List[str], top_n: int = 5) -> List[Dict]:
    """
    Get top N job recommendations for a resume.

    Args:
        resume_text: Full resume text
        extracted_skills: Skills extracted from resume
        top_n: Number of top recommendations to return

    Returns:
        Top N recommendations
    """
    all_recs = compute_recommendations(resume_text, extracted_skills)
    return all_recs[:top_n]


def explain_recommendation(recommendation: Dict, extracted_skills: List[str]) -> str:
    """
    Generate a human-readable explanation for why a role was recommended.

    Args:
        recommendation: Single recommendation dict
        extracted_skills: All skills from resume

    Returns:
        Explanation string
    """
    role = recommendation["role"]
    match_pct = recommendation["match_percentage"]
    matched = recommendation["matched_skills"]
    missing = recommendation["missing_skills"]

    explanation = f"**Why {role}?**\n\n"
    explanation += f"Your resume matches **{match_pct}%** of the requirements for this role.\n\n"

    if matched:
        top_matched = matched[:5]
        explanation += f"✅ **Key skills you have:** {', '.join(top_matched)}\n\n"

    if missing:
        top_missing = missing[:3]
        explanation += f"📚 **Skills to develop:** {', '.join(top_missing)}\n\n"

    if match_pct >= 80:
        explanation += "🌟 **Excellent match!** You're strongly qualified for this role."
    elif match_pct >= 60:
        explanation += "👍 **Good match.** With a few more skills, you'd be a strong candidate."
    elif match_pct >= 40:
        explanation += "📈 **Fair match.** Focus on the missing skills to improve your candidacy."
    else:
        explanation += "🎯 **Aspirational match.** This role requires significant additional skills."

    return explanation


def compute_skill_gap(extracted_skills: List[str], target_role: str) -> Dict:
    """
    Compute detailed skill gap analysis for a specific target role.

    Args:
        extracted_skills: Skills from resume
        target_role: Target job role name

    Returns:
        Detailed skill gap analysis
    """
    if target_role not in JOB_ROLES:
        return {"error": f"Role '{target_role}' not found"}

    role_data = JOB_ROLES[target_role]
    resume_skills_lower = [s.lower() for s in extracted_skills]

    required = role_data["required_skills"]
    nice_to_have = role_data.get("nice_to_have", [])

    matched_required = [s for s in required if s in resume_skills_lower]
    missing_required = [s for s in required if s not in resume_skills_lower]
    matched_optional = [s for s in nice_to_have if s in resume_skills_lower]
    missing_optional = [s for s in nice_to_have if s not in resume_skills_lower]

    completion_score = len(matched_required) / len(required) * 100 if required else 0

    from datasets.job_descriptions import CERTIFICATIONS
    certs = CERTIFICATIONS.get(target_role, [])

    return {
        "target_role": target_role,
        "required_skills": required,
        "matched_required": matched_required,
        "missing_required": missing_required,
        "nice_to_have": nice_to_have,
        "matched_optional": matched_optional,
        "missing_optional": missing_optional,
        "completion_score": round(completion_score, 1),
        "recommended_certifications": certs,
        "experience_required": role_data.get("experience_years", "N/A"),
        "salary_range": role_data.get("salary_range", "N/A"),
    }
