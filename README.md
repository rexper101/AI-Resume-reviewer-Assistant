# 🧠 AI Resume Screening & Interview Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.20+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**An end-to-end AI-powered platform for intelligent resume analysis, ATS scoring,
job recommendation, skill gap identification, and personalized interview preparation.**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Future Scope](#-future-scope)

</div>

---

## 📸 Screenshots

> _Screenshots placeholder — run the application and capture your results_

| Dashboard | ATS Score | Job Matches |
|-----------|-----------|-------------|
| ![Dashboard](assets/dashboard.png) | ![ATS](assets/ats_score.png) | ![Jobs](assets/job_matches.png) |

| Skill Analysis | Skill Gap | Interview Prep |
|----------------|-----------|----------------|
| ![Skills](assets/skills.png) | ![Gap](assets/skill_gap.png) | ![Interview](assets/interview.png) |

---

## 🎯 Project Overview

The **AI Resume Screening & Interview Assistant** is a comprehensive Data Science internship portfolio project that demonstrates the integration of:

- **Natural Language Processing** for skill extraction and resume parsing
- **Machine Learning** for role classification and job recommendation
- **TF-IDF + Cosine Similarity** for intelligent job matching
- **Interactive Data Visualization** with Plotly dashboards
- **Production-grade Python architecture** with modular design

This project simulates a real-world HR-tech tool used by companies like LinkedIn, Naukri, and Indeed for automated candidate screening.

---

## ✨ Features

### 📤 Resume Parser
- Upload PDF resumes with drag-and-drop interface
- Extract structured text using PyPDF2 / pdfplumber
- Detect resume sections (Summary, Experience, Education, Skills, Projects)
- Extract contact info (email, phone, LinkedIn, GitHub)
- Calculate resume statistics (word count, page estimate)

### 📊 ATS Score Calculator
- 7-dimension scoring across 100 points:
  - Keyword Optimization (25%)
  - Skills Relevance (20%)
  - Resume Structure (20%)
  - Experience Quality (15%)
  - Education Section (10%)
  - Contact Completeness (5%)
  - Additional Sections (5%)
- Radar chart visualization of component scores
- Actionable feedback for each dimension

### 💼 Job Recommendation Engine
- **TF-IDF vectorization** of resume and job descriptions
- **Cosine similarity** for semantic matching
- Combined scoring: 60% TF-IDF similarity + 40% skill overlap
- 8 job roles with salary ranges and experience requirements
- Explainable recommendations with matched/missing skills

### 🔍 NLP Skill Extraction
- 50+ technical skills detection across 6 categories
- Multi-word phrase matching (e.g., "machine learning", "deep learning")
- Skill alias resolution (e.g., "sklearn" → "scikit-learn")
- Skill frequency analysis and visualization
- Priority-weighted extraction by resume section

### 🎯 Skill Gap Analysis
- Compare resume against any target role
- Visual breakdown of matched vs. missing skills
- Personalized certification recommendations
- Learning roadmap suggestions

### 🤖 ML Role Predictor
- **Logistic Regression** (default) with multinomial classification
- **Random Forest** for ensemble prediction
- **Naive Bayes** for probabilistic classification
- Explainable AI: feature importance visualization
- Synthetic training data with augmentation (~200+ samples)
- Probability distribution across all roles

### 🎤 Interview Question Generator
- 300+ curated questions across 10+ technologies
- Difficulty levels: Basic, Intermediate, Advanced
- Role-specific behavioral and scenario questions
- Downloadable interview prep guide (Markdown)
- Optional Gemini/OpenAI API integration

### 📈 Analytics Dashboard
- 8 interactive Plotly charts
- Skill frequency bar charts
- Category distribution donut chart
- ATS radar visualization
- Role prediction probability bars
- Skill gap stacked bar chart

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit 1.32+ |
| **Backend** | Python 3.10+ |
| **Machine Learning** | scikit-learn (TF-IDF, Logistic Regression, Random Forest, Naive Bayes) |
| **NLP** | Regex, keyword matching, NLP preprocessing |
| **PDF Parsing** | PyPDF2, pdfplumber, pypdf |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly, Matplotlib |
| **Caching** | Streamlit `@st.cache_resource` |
| **Optional AI** | Google Gemini API, OpenAI API |

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/ai-resume-screener.git
cd ai-resume-screener

# 2. Create virtual environment (recommended)
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

### Optional: Install NLP Enhancement
```bash
pip install spacy
python -m spacy download en_core_web_sm
```

### Optional: Configure AI API (for dynamic question generation)
```bash
pip install google-generativeai
# Set your API key in the app settings
```

---

## 📖 Usage

### Quick Start

1. **Launch the app** with `streamlit run app.py`
2. **Navigate** using the sidebar menu
3. **Upload** your PDF resume on the "Upload & Analyze" page
4. Click **"Run Full AI Analysis"** to process
5. **Explore** results across all dashboard sections

### Demo Mode
Can't find a PDF? Use the built-in **Sample Resume** button to load a pre-built data scientist resume and see all features in action.

### Downloading Results
- Interview questions are downloadable as a **Markdown file**
- Charts can be exported using Plotly's built-in toolbar

---

## 🏗️ Architecture

```
ai-resume-screener/
│
├── app.py                    # Main Streamlit application & routing
│
├── resume_parser.py          # PDF text extraction & section detection
├── skill_extractor.py        # NLP keyword-based skill extraction
├── recommender.py            # TF-IDF job recommendation engine
├── ats_calculator.py         # ATS score computation (7 dimensions)
├── interview_generator.py    # Interview question generation
├── role_predictor.py         # ML classification model
├── dashboard.py              # Plotly chart factories
│
├── datasets/
│   ├── job_descriptions.py   # Job roles, skills taxonomy, certifications
│   └── interview_questions.py # 300+ interview questions database
│
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

### Data Flow

```
PDF Upload
    │
    ▼
resume_parser.py ──► Clean Text + Sections + Contact Info
    │
    ▼
skill_extractor.py ──► Skills List + Categories + Frequency
    │
    ├──► ats_calculator.py ──► ATS Score (0-100) + Feedback
    │
    ├──► recommender.py ──► Job Matches + Skill Gaps
    │         └──► TF-IDF Vectorizer + Cosine Similarity
    │
    ├──► role_predictor.py ──► ML Role Classification + Probabilities
    │         └──► Logistic Regression / Random Forest / Naive Bayes
    │
    └──► interview_generator.py ──► Personalized Question Pack
```

### ML Pipeline

```python
# TF-IDF + Cosine Similarity (Recommendation)
Resume Text → TfidfVectorizer → cosine_similarity(resume, job_descriptions)

# Classification (Role Prediction)
Skills Text → TfidfVectorizer → LogisticRegression.fit(training_data)
                              → predict_proba(resume_vector)
```

---

## 🔬 ML Models Explained

### 1. TF-IDF Recommendation Engine
- **TF-IDF** (Term Frequency-Inverse Document Frequency) converts text to numerical vectors
- **Cosine similarity** measures the angle between vectors (1 = identical, 0 = completely different)
- Combined score: `0.6 × TF-IDF_similarity + 0.4 × skill_overlap_ratio`

### 2. Role Classification Models

| Model | Pros | Cons |
|-------|------|------|
| Logistic Regression | Fast, interpretable, good for sparse text | Linear decision boundary |
| Random Forest | Robust, handles non-linearity | Slower, less interpretable |
| Naive Bayes | Very fast, good for text | Independence assumption |

### 3. Explainable AI
- Feature importance from Logistic Regression coefficients
- Highlights which skills/keywords drove the prediction
- Confidence scores for all predicted roles

---

## 💡 Interview Explanation Points

### For Your Interview, Explain:

**"What ML algorithm did you use and why?"**
> "I chose TF-IDF + Cosine Similarity for job recommendations because resumes and job descriptions are sparse text documents. TF-IDF emphasizes important keywords while downweighting common words. For role classification, I used Logistic Regression with multinomial classification — it's interpretable, works well with TF-IDF features, and provides probability outputs for all classes."

**"How does the ATS score work?"**
> "The ATS score is a weighted composite of 7 dimensions — keyword density, skills count, resume structure, experience quality, education completeness, contact information, and additional sections. Each dimension is scored 0-100 then weighted by importance. This mimics how real ATS systems like Greenhouse and Lever parse resumes."

**"How did you handle NLP without a large model?"**
> "I used regex-based keyword extraction with a curated 50+ skill taxonomy. Skills are matched using whole-word boundary patterns to avoid false positives. Multi-word phrases like 'machine learning' are matched first. Aliases like 'sklearn' → 'scikit-learn' are normalized. This is fast, explainable, and works without GPU requirements."

---

## 🔮 Future Scope

| Enhancement | Description |
|------------|-------------|
| **LLM Integration** | Use GPT-4/Gemini for contextual resume summarization |
| **Semantic Search** | Replace keyword matching with sentence-transformers embeddings |
| **Multi-resume** | Batch process and compare multiple resumes |
| **Job Board API** | Real-time job listings from LinkedIn/Indeed API |
| **Resume Builder** | AI-powered resume improvement suggestions |
| **Interview Simulator** | Voice-based mock interview with AI feedback |
| **Company Match** | Match candidates to company culture profiles |
| **ATS Bypass Tips** | Role-specific ATS optimization recommendations |
| **Multi-language** | Support resumes in Spanish, French, German |
| **Bias Detection** | Flag potentially biased language in resumes |

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io) — for the amazing web framework
- [scikit-learn](https://scikit-learn.org) — for ML algorithms
- [Plotly](https://plotly.com) — for interactive visualizations
- [PyPDF2](https://pypdf2.readthedocs.io) — for PDF parsing

---

<div align="center">
Built with ❤️ as a Data Science internship portfolio project<br>
<a href="https://github.com/yourusername">GitHub</a> • <a href="https://linkedin.com/in/yourprofile">LinkedIn</a>
</div>
