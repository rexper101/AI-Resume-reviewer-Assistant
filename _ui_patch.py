from pathlib import Path

p = Path(__file__).parent / "app.py"
text = p.read_text(encoding="utf-8")
T = "MOTIONDIV"

def tag(s: str) -> str:
    return s.replace(T, "d" + "iv")

# --- page_home ---
s = text.index("def page_home():")
e = text.index("\n\n# ── Page: Upload & Analyze")
text = text[:s] + tag(r'''
def page_home():
    st.markdown("""
    <MOTIONDIV class='hero-section'>
        <MOTIONDIV class='hero-badge'>AI-powered career toolkit</MOTIONDIV>
        <MOTIONDIV class='hero-title'>Screen smarter.<br>Interview better.</MOTIONDIV>
        <MOTIONDIV class='hero-subtitle'>
            One upload unlocks ATS scoring, job matches, skill gaps, ML role predictions,
            and a personalized interview prep pack.
        </MOTIONDIV>
    </MOTIONDIV>
    """, unsafe_allow_html=True)

    features = [
        ("01", "\U0001f4c4", "Resume Parser", "Extract structure, sections, and contact info from PDF"),
        ("02", "\U0001f4ca", "ATS Score", "7 weighted dimensions with actionable feedback"),
        ("03", "\U0001f4bc", "Job Matching", "TF-IDF + cosine similarity across 8 roles"),
        ("04", "\U0001f9e0", "Skill Extraction", "50+ skills across six technical categories"),
        ("05", "\U0001f3af", "Skill Gap", "See what to learn for your target role"),
        ("06", "\U0001f916", "ML Prediction", "Logistic regression, random forest, naive Bayes"),
        ("07", "\U0001f3a4", "Interview Prep", "Technical, behavioral, and scenario questions"),
        ("08", "\U0001f4c8", "Analytics", "Interactive Plotly dashboards in one view"),
    ]

    cols = st.columns(4)
    for i, (num, emoji, title, desc) in enumerate(features):
        with cols[i % 4]:
            st.markdown(f"""
            <MOTIONDIV class='feature-card'>
                <MOTIONDIV class='feature-num'>{num}</MOTIONDIV>
                <MOTIONDIV style='font-size:1.25rem;margin-bottom:8px;'>{emoji}</MOTIONDIV>
                <MOTIONDIV class='feature-title'>{title}</MOTIONDIV>
                <MOTIONDIV class='feature-desc'>{desc}</MOTIONDIV>
            </MOTIONDIV>
            """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### Quick start")
        for i, step in enumerate([
            "Open **Upload & Analyze** in the sidebar",
            "Upload a PDF or load the sample resume",
            "Click **Run Full AI Analysis**",
            "Explore ATS, matches, skills, and interview prep",
        ], 1):
            st.markdown(
                f"<MOTIONDIV style='color:#94A3B8;padding:6px 0;'>"
                f"<span style='color:#14B8A6;font-weight:700;margin-right:8px;'>{i}</span>{step}</MOTIONDIV>",
                unsafe_allow_html=True,
            )
    with col2:
        st.markdown("### Built with")
        for item in ["Python 3.10+", "Streamlit", "scikit-learn", "Plotly", "PyPDF2"]:
            st.markdown(f"<span class='skill-tag'>{item}</span>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cta1, cta2, _ = st.columns([1, 1, 2])
    with cta1:
        if st.button("Upload resume", type="primary", use_container_width=True):
            st.session_state.current_page = "Upload & Analyze"
            st.rerun()
    with cta2:
        if st.session_state.analysis_done and st.button("View dashboard", use_container_width=True):
            st.session_state.current_page = "Analytics Dashboard"
            st.rerun()

''') + text[e:]

subs = [
    (
        "def page_upload():\n    st.markdown(\"<div class='section-header'>Resume Upload & Analysis</div>\", unsafe_allow_html=True)",
        'def page_upload():\n    render_page_header("Upload & Analyze")',
    ),
    (
        "def page_ats_score():\n    st.markdown(\"<div class='section-header'>ATS Score Analysis</div>\", unsafe_allow_html=True)\n\n    if not st.session_state.ats_result:\n        st.warning(\"Please upload and analyze a resume first.\")\n        return",
        'def page_ats_score():\n    render_page_header("ATS Score")\n    if not require_analysis("ATS Score"):\n        return',
    ),
    (
        "def page_job_matches():\n    st.markdown(\"<motion-div class='section-header'>Job Recommendations</motion-div>\", unsafe_allow_html=True)\n\n    if not st.session_state.recommendations:\n        st.warning(\"Please upload and analyze a resume first.\")\n        return",
        'def page_job_matches():\n    render_page_header("Job Matches")\n    if not require_analysis("Job Matches"):\n        return',
    ),
]

# fix job matches old string
subs[2] = (
    "def page_job_matches():\n    st.markdown(\"<div class='section-header'>Job Recommendations</div>\", unsafe_allow_html=True)\n\n    if not st.session_state.recommendations:\n        st.warning(\"Please upload and analyze a resume first.\")\n        return",
    'def page_job_matches():\n    render_page_header("Job Matches")\n    if not require_analysis("Job Matches"):\n        return',
)

subs += [
    (
        "def page_skill_analysis():\n    st.markdown(\"<div class='section-header'>Skill Analysis</motion-div>\", unsafe_allow_html=True)\n\n    if not st.session_state.skill_data:\n        st.warning(\"Please upload and analyze a resume first.\")\n        return",
        'def page_skill_analysis():\n    render_page_header("Skill Analysis")\n    if not require_analysis("Skill Analysis"):\n        return',
    ),
]

subs[-1] = (
    "def page_skill_analysis():\n    st.markdown(\"<div class='section-header'>Skill Analysis</div>\", unsafe_allow_html=True)\n\n    if not st.session_state.skill_data:\n        st.warning(\"Please upload and analyze a resume first.\")\n        return",
    'def page_skill_analysis():\n    render_page_header("Skill Analysis")\n    if not require_analysis("Skill Analysis"):\n        return',
)

more = [
    (
        "def page_skill_gap():\n    st.markdown(\"<div class='section-header'>Skill Gap Analysis</div>\", unsafe_allow_html=True)\n\n    if not st.session_state.recommendations:\n        st.warning(\"Please upload and analyze a resume first.\")\n        return",
        'def page_skill_gap():\n    render_page_header("Skill Gap")\n    if not require_analysis("Skill Gap"):\n        return',
    ),
    (
        "def page_role_predictor():\n    st.markdown(\"<div class='section-header'>ML Role Predictor</div>\", unsafe_allow_html=True)\n\n    if not st.session_state.prediction_result:\n        st.warning(\"Please upload and analyze a resume first.\")\n        return",
        'def page_role_predictor():\n    render_page_header("Role Predictor")\n    if not require_analysis("Role Predictor"):\n        return',
    ),
    (
        "def page_interview_prep():\n    st.markdown(\"<div class='section-header'>Interview Preparation</div>\", unsafe_allow_html=True)\n\n    if not st.session_state.interview_pack:\n        st.warning(\"Please upload and analyze a resume first.\")\n        return",
        'def page_interview_prep():\n    render_page_header("Interview Prep")\n    if not require_analysis("Interview Prep"):\n        return',
    ),
    (
        "def page_analytics_dashboard():\n    st.markdown(\"<div class='section-header'>Analytics Dashboard</div>\", unsafe_allow_html=True)\n\n    if not st.session_state.analysis_done:\n        st.warning(\"Please upload and analyze a resume first.\")\n        return",
        'def page_analytics_dashboard():\n    render_page_header("Analytics Dashboard")\n    if not require_analysis("the analytics dashboard"):\n        return',
    ),
]
subs.extend(more)

for old, new in subs:
    if old not in text:
        print("MISSING:", repr(old[:70]))
    else:
        text = text.replace(old, new, 1)

old_empty = '''        st.markdown("""
        <div style='text-align:center; padding:50px; color:#475569;'>
            <motion-div style='font-size:1.5rem; margin-bottom:16px; color:#475569;'>---</motion-div>
            <motion-div style='font-size:1.1rem;'>Upload a PDF resume or load the sample to begin</motion-div>
        </motion-div>
        """, unsafe_allow_html=True)'''
old_empty = old_empty.replace("motion-div", "motion-div")
old_empty = '''        st.markdown("""
        <div style='text-align:center; padding:50px; color:#475569;'>
            <div style='font-size:1.5rem; margin-bottom:16px; color:#475569;'>---</div>
            <div style='font-size:1.1rem;'>Upload a PDF resume or load the sample to begin</div>
        </div>
        """, unsafe_allow_html=True)'''
new_empty = '        render_empty_state("\\U0001f4c4", "No resume yet", "Upload a PDF or load the sample resume to get started.")'
if old_empty in text:
    text = text.replace(old_empty, new_empty, 1)
else:
    print("empty state block missing")

p.write_text(text, encoding="utf-8")
print("done")
