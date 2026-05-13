"""
interview_generator.py - AI-powered interview question generator.
Generates personalized interview questions based on extracted skills.
Uses local question database + optional Gemini/OpenAI API integration.
"""

import random
from typing import List, Dict, Optional

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from datasets.interview_questions import INTERVIEW_QUESTIONS, BEHAVIORAL_QUESTIONS


def get_questions_for_skill(skill: str, level: str = "mixed", count: int = 3) -> List[str]:
    """
    Get interview questions for a specific skill.

    Args:
        skill: Skill name (e.g., "python", "machine learning")
        level: "basic", "intermediate", "advanced", or "mixed"
        count: Number of questions to return

    Returns:
        List of interview questions
    """
    skill_lower = skill.lower()

    # Find matching skill in question database
    matched_key = None
    for key in INTERVIEW_QUESTIONS.keys():
        if key in skill_lower or skill_lower in key:
            matched_key = key
            break

    if not matched_key:
        return []

    skill_questions = INTERVIEW_QUESTIONS[matched_key]

    if level == "mixed":
        # Take from all available levels
        all_questions = []
        for level_key, questions in skill_questions.items():
            all_questions.extend(questions)
        return random.sample(all_questions, min(count, len(all_questions)))

    elif level in skill_questions:
        questions = skill_questions[level]
        return random.sample(questions, min(count, len(questions)))

    else:
        # Default to basic
        questions = skill_questions.get("basic", [])
        return random.sample(questions, min(count, len(questions)))


def generate_interview_pack(
    extracted_skills: List[str],
    experience_level: str = "Junior",
    target_role: Optional[str] = None,
    questions_per_skill: int = 3
) -> Dict:
    """
    Generate a complete interview question pack based on resume.

    Args:
        extracted_skills: Skills from resume
        experience_level: "Fresher", "Junior", "Mid-Level", "Senior"
        target_role: Optional target job role
        questions_per_skill: Questions per skill category

    Returns:
        Dict containing organized interview questions
    """
    # Determine question difficulty based on experience
    level_map = {
        "Fresher/Student": "basic",
        "Entry Level": "basic",
        "Junior": "basic",
        "Mid-Level": "intermediate",
        "Senior": "advanced",
        "Lead/Principal": "advanced"
    }
    question_level = level_map.get(experience_level, "basic")

    # Priority skills to generate questions for
    # Match against our question database
    available_skills = list(INTERVIEW_QUESTIONS.keys())
    priority_skills = []

    for skill in extracted_skills:
        skill_lower = skill.lower()
        for available in available_skills:
            if available in skill_lower or skill_lower in available:
                if available not in priority_skills:
                    priority_skills.append(available)

    # Limit to top 6 skills for manageable interview pack
    priority_skills = priority_skills[:6]

    # Generate technical questions
    technical_questions = {}
    for skill in priority_skills:
        questions = get_questions_for_skill(skill, question_level, questions_per_skill)
        if questions:
            technical_questions[skill.title()] = questions

    # Add behavioral questions
    behavioral_sample = random.sample(BEHAVIORAL_QUESTIONS, min(5, len(BEHAVIORAL_QUESTIONS)))

    # Add role-specific questions if target role is specified
    role_specific_questions = get_role_specific_questions(target_role) if target_role else []

    # Generate problem-solving scenarios
    scenario_questions = generate_scenario_questions(extracted_skills, target_role)

    return {
        "technical_questions": technical_questions,
        "behavioral_questions": behavioral_sample,
        "role_specific_questions": role_specific_questions,
        "scenario_questions": scenario_questions,
        "total_questions": (
            sum(len(q) for q in technical_questions.values()) +
            len(behavioral_sample) +
            len(role_specific_questions) +
            len(scenario_questions)
        ),
        "experience_level": experience_level,
        "question_level": question_level,
        "skills_covered": list(technical_questions.keys())
    }


def get_role_specific_questions(role: str) -> List[str]:
    """
    Get role-specific interview questions.

    Args:
        role: Job role name

    Returns:
        List of role-specific questions
    """
    role_questions = {
        "Data Scientist": [
            "Walk me through your approach to a data science problem from scratch.",
            "How do you decide which ML algorithm to use for a given problem?",
            "Describe how you would handle a severely imbalanced dataset.",
            "How do you explain a complex model's predictions to business stakeholders?",
            "What's the most challenging ML project you've worked on? What made it hard?",
        ],
        "Data Analyst": [
            "How do you approach data cleaning and validation?",
            "Walk me through how you'd build a dashboard for business stakeholders.",
            "How do you handle conflicting data from different sources?",
            "What metrics would you track for an e-commerce business?",
            "Describe a time when your data analysis changed a business decision.",
        ],
        "ML Engineer": [
            "How do you monitor a deployed ML model in production?",
            "What is your approach to model versioning and experiment tracking?",
            "How do you handle model degradation over time?",
            "Describe your CI/CD pipeline for ML models.",
            "How would you serve a model that needs to handle 10,000 requests/second?",
        ],
        "Python Developer": [
            "How do you structure a large Python application for maintainability?",
            "Walk me through how you'd design a REST API with FastAPI or Django.",
            "How do you approach testing in Python? What's your testing strategy?",
            "How do you handle database migrations in a production environment?",
            "What's your approach to async programming in Python?",
        ],
        "AI Engineer": [
            "How would you design a RAG (Retrieval-Augmented Generation) system?",
            "What are the key considerations when fine-tuning a large language model?",
            "How do you evaluate and mitigate hallucinations in LLM applications?",
            "Walk me through how you'd build a production-ready chatbot.",
            "How do you handle context length limitations in LLM applications?",
        ],
        "Backend Developer": [
            "How do you design a scalable microservices architecture?",
            "How do you approach database optimization for high-traffic applications?",
            "Explain how you'd implement authentication and authorization in an API.",
            "How do you handle race conditions and concurrent requests?",
            "What's your approach to API versioning?",
        ],
    }

    return role_questions.get(role, [
        f"Why do you want to work as a {role}?",
        f"What relevant experience do you have for the {role} position?",
        f"What are your career goals as a {role}?",
    ])


def generate_scenario_questions(skills: List[str], role: Optional[str] = None) -> List[str]:
    """
    Generate practical scenario-based questions.

    Args:
        skills: Extracted skills
        role: Target role

    Returns:
        List of scenario questions
    """
    scenarios = []
    skills_lower = [s.lower() for s in skills]

    # Data/ML scenarios
    if any(s in skills_lower for s in ["machine learning", "python", "tensorflow"]):
        scenarios.append(
            "Scenario: A client's ML model works well in dev but fails in production. "
            "Performance degrades after 2 weeks. How would you diagnose and fix this?"
        )

    if "sql" in skills_lower or "postgresql" in skills_lower:
        scenarios.append(
            "Scenario: A query that used to run in 2 seconds now takes 5 minutes. "
            "Walk me through your debugging process and optimization strategy."
        )

    if any(s in skills_lower for s in ["aws", "docker", "kubernetes"]):
        scenarios.append(
            "Scenario: Your application is experiencing intermittent downtime during peak hours. "
            "How would you diagnose the issue and design a solution?"
        )

    if "python" in skills_lower or "django" in skills_lower:
        scenarios.append(
            "Scenario: You need to design a REST API that will handle 1 million requests per day. "
            "Walk me through your architecture decisions."
        )

    if any(s in skills_lower for s in ["nlp", "natural language processing", "llm"]):
        scenarios.append(
            "Scenario: A customer wants a chatbot that answers questions from their 500-page product manual. "
            "How would you build this system?"
        )

    # Generic scenarios
    scenarios.append(
        "Scenario: You discover a critical bug in production 30 minutes before a major product demo. "
        "What do you do?"
    )

    scenarios.append(
        "Scenario: You're given 3 months to improve a product metric by 20%. "
        "How do you approach this problem?"
    )

    return scenarios[:4]  # Return max 4 scenarios


def format_interview_pack_markdown(interview_pack: Dict) -> str:
    """
    Format the interview pack as a markdown document.

    Args:
        interview_pack: Interview pack dict

    Returns:
        Formatted markdown string
    """
    md = []
    md.append(f"# 🎯 Interview Preparation Guide")
    md.append(f"\n**Experience Level:** {interview_pack['experience_level']}")
    md.append(f"**Question Level:** {interview_pack['question_level'].title()}")
    md.append(f"**Total Questions:** {interview_pack['total_questions']}")
    md.append(f"**Skills Covered:** {', '.join(interview_pack['skills_covered'])}\n")

    # Technical Questions
    if interview_pack["technical_questions"]:
        md.append("---\n## 💻 Technical Questions\n")
        for skill, questions in interview_pack["technical_questions"].items():
            md.append(f"### {skill}")
            for i, q in enumerate(questions, 1):
                md.append(f"{i}. {q}")
            md.append("")

    # Role-specific
    if interview_pack["role_specific_questions"]:
        md.append("---\n## 🎯 Role-Specific Questions\n")
        for i, q in enumerate(interview_pack["role_specific_questions"], 1):
            md.append(f"{i}. {q}")
        md.append("")

    # Scenarios
    if interview_pack["scenario_questions"]:
        md.append("---\n## 🧩 Scenario-Based Questions\n")
        for i, q in enumerate(interview_pack["scenario_questions"], 1):
            md.append(f"{i}. {q}")
        md.append("")

    # Behavioral
    if interview_pack["behavioral_questions"]:
        md.append("---\n## 🌟 Behavioral Questions\n")
        for i, q in enumerate(interview_pack["behavioral_questions"], 1):
            md.append(f"{i}. {q}")
        md.append("")

    md.append("---\n*Generated by AI Resume Screening & Interview Assistant*")

    return '\n'.join(md)


def generate_with_gemini_api(skills: List[str], role: str, api_key: str) -> List[str]:
    """
    Generate interview questions using Google Gemini API.
    Optional enhancement when API key is available.

    Args:
        skills: List of skills
        role: Target role
        api_key: Gemini API key

    Returns:
        List of AI-generated questions
    """
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        skills_str = ', '.join(skills[:10])
        prompt = f"""Generate 5 specific, technical interview questions for a {role} candidate 
        who has expertise in: {skills_str}.
        
        Format: Return only the questions, numbered 1-5, no preamble.
        Make them challenging but fair for an interview setting."""

        response = model.generate_content(prompt)
        text = response.text

        # Parse questions from response
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        questions = []
        for line in lines:
            # Remove numbering
            clean = re.sub(r'^\d+[\.\)]\s*', '', line)
            if len(clean) > 20 and '?' in clean:
                questions.append(clean)

        return questions[:5]

    except Exception as e:
        return [f"API generation failed: {str(e)}. Using local question bank instead."]
