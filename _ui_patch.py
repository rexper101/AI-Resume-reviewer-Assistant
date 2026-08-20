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

    