from pathlib import Path

D = "d" + "iv"
T = "MOTIONDIV"

def h(s):
    return s.replace(T, D)

p = Path(__file__).parent / "app.py"
t = p.read_text(encoding="utf-8")

old_brand = h("""            <MOTIONDIV style='font-family: Outfit, sans-serif; font-size: 1.35rem;
                        font-weight: 700; color: #F1F5F9;'>ResumeAI</MOTIONDIV>
            <MOTIONDIV style='color: #64748B; font-size: 0.7rem; letter-spacing: 0.14em;
                        text-transform: uppercase; margin-top: 4px;'>Career Intelligence</MOTIONDIV>""")

new_brand = h("""            <MOTIONDIV class='sidebar-title'>ResumeAI</MOTIONDIV>
            <MOTIONDIV class='sidebar-tagline'>Career Intelligence</MOTIONDIV>""")

if old_brand in t:
    t = t.replace(old_brand, new_brand, 1)
    print("brand ok")
else:
    print("brand miss", old_brand[:50])

old_nav = h("""                    st.markdown(
                        f"<MOTIONDIV style='padding:8px 12px;margin:2px 0;border-radius:10px;"
                        f"background:rgba(20,184,166,0.14);border:1px solid rgba(20,184,166,0.35);"
                        f"color:#5EEAD4;font-size:0.88rem;font-weight:600;'>{label}</MOTIONDIV>",
                        unsafe_allow_html=True,
                    )""")

new_nav = h("""                    st.markdown(
                        f"<MOTIONDIV class='nav-active'>{label}</MOTIONDIV>",
                        unsafe_allow_html=True,
                    )""")

if old_nav in t:
    t = t.replace(old_nav, new_nav, 1)

old_stat = h("""            <MOTIONDIV class='glass-card' style='padding:14px;'>
                <MOTIONDIV style='color:#6EE7B7;font-size:0.72rem;font-weight:700;
                            letter-spacing:0.08em;text-transform:uppercase;'>Analysis ready</MOTIONDIV>
                <MOTIONDIV style='margin-top:10px;display:flex;gap:6px;flex-wrap:wrap;'>
                    <span style='background:rgba(20,184,166,0.12);color:#5EEAD4;padding:4px 10px;
                                 border-radius:8px;font-size:0.75rem;'>{skills_count} skills</span>
                    <span style='background:rgba(20,184,166,0.12);color:#5EEAD4;padding:4px 10px;
                                 border-radius:8px;font-size:0.75rem;'>ATS {ats_score}</span>
                    <span style='background:rgba(20,184,166,0.12);color:#5EEAD4;padding:4px 10px;
                                 border-radius:8px;font-size:0.75rem;'>{top_match}% match</span>
                </MOTIONDIV>
            </MOTIONDIV>""")

new_stat = h("""            <MOTIONDIV class='glass-card' style='padding:14px;'>
                <MOTIONDIV class='status-ready'>Analysis ready</MOTIONDIV>
                <MOTIONDIV style='margin-top:10px;display:flex;gap:6px;flex-wrap:wrap;'>
                    <span class='stat-pill'>{skills_count} skills</span>
                    <span class='stat-pill'>ATS {ats_score}</span>
                    <span class='stat-pill'>{top_match}% match</span>
                </MOTIONDIV>
            </MOTIONDIV>""")

if old_stat in t:
    t = t.replace(old_stat, new_stat, 1)

subs = [
    ("color: #F1F5F9", "color: var(--text)"),
    ("color:#5EEAD4", "color:var(--accent-text)"),
    ("color:#6EE7B7", "color:#047857"),
    ("color: #6EE7B7", "color: #047857"),
    ("color: #5EEAD4", "color: var(--accent-text)"),
    ("color: #CBD5E1", "color: var(--text-muted)"),
    ("color: #E2E8F0", "color: var(--text)"),
    ("color: #94A3B8", "color: var(--text-muted)"),
    ("color:#94A3B8", "color:var(--text-muted)"),
    ("background: rgba(30,41,59,0.5)", "background: var(--bg-muted)"),
    ("background: rgba(30,41,59,0.6)", "background: #FFFFFF"),
    ("background: rgba(0,0,0,0.2)", "background: var(--bg-muted)"),
    ("border: 1px solid rgba(99,102,241,0.2)", "border: 1px solid #E2E8F0"),
    ("border: 1px solid rgba(99,102,241,0.15)", "border: 1px solid #E2E8F0"),
    ("border: 1px solid rgba(99,102,241,0.25)", "border: 1px solid #E2E8F0"),
    ("border: 1px solid rgba(99,102,241,0.35)", "border: 1px solid #99F6E4"),
    (
        "background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.08))",
        "background: linear-gradient(135deg, #F0FDFA, #ECFEFF)",
    ),
    (
        "background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(139,92,246,0.1));\n"
        "                border: 1px solid #99F6E4",
        "background: linear-gradient(135deg, #F0FDFA, #ECFEFF);\n"
        "                border: 1px solid #99F6E4",
    ),
    ("color: #6366F1", "color: var(--accent)"),
    ("#8B5CF6", "var(--accent)"),
    ("#A78BFA", "#5EEAD4"),
]

for a, b in subs:
    t = t.replace(a, b)

t = t.replace(
    h('f"<MOTIONDIV style=\'color:#94A3B8;padding:6px 0;\'>"'),
    h('f"<MOTIONDIV class=\'feature-row\'>"'),
)

p.write_text(t, encoding="utf-8")
print("done")
