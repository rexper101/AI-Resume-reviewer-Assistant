from pathlib import Path

p = Path(__file__).parent / "app.py"
text = p.read_text(encoding="utf-8")
start = text.index("def render_sidebar():")
end = text.index("\n\n# ── Helper: Run Analysis")

TAG = "div"
o, c = f"<{TAG}", f"</{TAG}>"

new_sidebar = f'''def render_sidebar():
    with st.sidebar:
        st.markdown("""
        {o} style='text-align:center; padding: 8px 0 16px;'>
            {o} class='brand-logo'>&#128203;{c}
            {o} style='font-family: Outfit, sans-serif; font-size: 1.35rem;
                        font-weight: 700; color: #F1F5F9;'>ResumeAI{c}
            {o} style='color: #64748B; font-size: 0.7rem; letter-spacing: 0.14em;
                        text-transform: uppercase; margin-top: 4px;'>Career Intelligence{c}
        {c}
        """, unsafe_allow_html=True)

        current = st.session_state.get("current_page", "Home")
        for group_name, pages in NAV_GROUPS:
            st.markdown(f"{o} class='nav-group-label'>{{group_name}}{c}", unsafe_allow_html=True)
            for page in pages:
                icon = NAV_ICONS.get(page, "\\u2022")
                label = f"{{icon}}  {{page}}"
                if current == page:
                    st.markdown(
                        f"{o} style='padding:8px 12px;margin:2px 0;border-radius:10px;"
                        f"background:rgba(20,184,166,0.14);border:1px solid rgba(20,184,166,0.35);"
                        f"color:#5EEAD4;font-size:0.88rem;font-weight:600;'>{{label}}{c}",
                        unsafe_allow_html=True,
                    )
                elif st.button(label, key=f"nav_{{page}}", use_container_width=True):
                    st.session_state.current_page = page
                    st.rerun()

        st.markdown("<hr style='border-color:rgba(20,184,166,0.12);margin:16px 0;'>", unsafe_allow_html=True)

        if st.session_state.analysis_done:
            skills_count = len(st.session_state.extracted_skills or [])
            ats_score = st.session_state.ats_result["total_score"] if st.session_state.ats_result else 0
            top_match = st.session_state.recommendations[0]["match_percentage"] if st.session_state.recommendations else 0
            st.markdown(f"""
            {o} class='glass-card' style='padding:14px;'>
                {o} style='color:#6EE7B7;font-size:0.72rem;font-weight:700;
                            letter-spacing:0.08em;text-transform:uppercase;'>Analysis ready{c}
                {o} style='margin-top:10px;display:flex;gap:6px;flex-wrap:wrap;'>
                    <span style='background:rgba(20,184,166,0.12);color:#5EEAD4;padding:4px 10px;
                                 border-radius:8px;font-size:0.75rem;'>{{skills_count}} skills</span>
                    <span style='background:rgba(20,184,166,0.12);color:#5EEAD4;padding:4px 10px;
                                 border-radius:8px;font-size:0.75rem;'>ATS {{ats_score}}</span>
                    <span style='background:rgba(20,184,166,0.12);color:#5EEAD4;padding:4px 10px;
                                 border-radius:8px;font-size:0.75rem;'>{{top_match}}% match</span>
                {c}
            {c}
            """, unsafe_allow_html=True)
            if st.button("Start over", use_container_width=True):
                for key in ("resume_text", "parsed_resume", "extracted_skills", "skill_data",
                            "recommendations", "ats_result", "prediction_result",
                            "interview_pack", "skill_gap"):
                    st.session_state[key] = None
                st.session_state.analysis_done = False
                st.session_state.current_page = "Upload & Analyze"
                st.rerun()
        else:
            st.markdown("""
            {o} class='glass-card' style='padding:14px;color:#94A3B8;font-size:0.82rem;line-height:1.5;'>
                Upload a resume to unlock ATS scoring, job matches, and interview prep.
            {c}
            """, unsafe_allow_html=True)

        st.markdown("""
        {o} style='margin-top:24px;text-align:center;color:#475569;font-size:0.7rem;line-height:1.6;'>
            Python &middot; Streamlit &middot; scikit-learn<br>v1.0
        {c}
        """, unsafe_allow_html=True)

'''

p.write_text(text[:start] + new_sidebar + text[end:], encoding="utf-8")
print("done")
