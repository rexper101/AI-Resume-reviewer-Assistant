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

    