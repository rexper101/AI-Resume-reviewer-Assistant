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

