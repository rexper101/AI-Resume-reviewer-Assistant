from pathlib import Path

p = Path(__file__).parent / "dashboard.py"
t = p.read_text(encoding="utf-8")

t = t.replace(
    '''COLORS = {
    "primary": "#14B8A6",      # Teal
    "secondary": "#06B6D4",    # Cyan
    "accent": "#8B5CF6",       # Violet accent
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#3B82F6",
    "bg_dark": "#0B0F1A",
    "card_bg": "#131B2E",
    "text": "#F1F5F9",
}''',
    '''COLORS = {
    "primary": "#0D9488",
    "secondary": "#0891B2",
    "accent": "#0F766E",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#3B82F6",
    "bg_dark": "#F8FAFC",
    "card_bg": "#FFFFFF",
    "text": "#0F172A",
    "text_muted": "#64748B",
    "grid": "#E2E8F0",
}''',
)

t = t.replace("apply_dark_theme", "apply_chart_theme")
t = t.replace(
    '''def apply_chart_theme(fig: go.Figure) -> go.Figure:
    """Apply consistent dark theme to a Plotly figure."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC", family="Inter, sans-serif", size=12),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.08)", linecolor="rgba(255,255,255,0.15)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)", linecolor="rgba(255,255,255,0.15)")
    return fig''',
    '''def apply_chart_theme(fig: go.Figure) -> go.Figure:
    """Apply consistent light theme to a Plotly figure."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0F172A", family="DM Sans, sans-serif", size=12),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    fig.update_xaxes(gridcolor="#E2E8F0", linecolor="#CBD5E1", tickfont=dict(color="#64748B"))
    fig.update_yaxes(gridcolor="#E2E8F0", linecolor="#CBD5E1", tickfont=dict(color="#64748B"))
    return fig''',
)

t = t.replace('font=dict(color="#F8FAFC', 'font=dict(color="#0F172A')
t = t.replace('textfont=dict(color="#F8FAFC', 'textfont=dict(color="#0F172A')
t = t.replace('title=dict(text="Skill Frequency Analysis", font=dict(size=16, color="#0F172A', 'title=dict(text="Skill Frequency Analysis", font=dict(size=16, color="#0F172A')
t = t.replace('legend=dict(font=dict(color="#94A3B8"))', 'legend=dict(font=dict(color="#64748B"))')
t = t.replace('line=dict(color="#09090B", width=2)', 'line=dict(color="#FFFFFF", width=2)')
t = t.replace('line=dict(color="rgba(255,255,255,0.1)", width=1)', 'line=dict(color="#E2E8F0", width=1)')
t = t.replace('line_color="rgba(255,255,255,0.3)"', 'line_color="#CBD5E1"')
t = t.replace('annotation_font_color="#94A3B8"', 'annotation_font_color="#64748B"')
t = t.replace('tickfont=dict(color="#94A3B8")', 'tickfont=dict(color="#64748B")')
t = t.replace('tickfont=dict(color="#A1A1AA", size=10)', 'tickfont=dict(color="#64748B", size=10)')
t = t.replace('gridcolor="rgba(255,255,255,0.1)"', 'gridcolor="#E2E8F0"')
t = t.replace('linecolor="rgba(255,255,255,0.15)"', 'linecolor="#CBD5E1"')
t = t.replace('tickcolor="rgba(255,255,255,0.3)"', 'tickcolor="#94A3B8"')
t = t.replace('line={"color": "#FFFFFF", "width": 2}', 'line={"color": "#0F172A", "width": 2}')
t = t.replace(
    '"font": {"color": "#F8FAFC", "family": "Inter, sans-serif"}',
    '"font": {"color": "#0F172A", "family": "DM Sans, sans-serif"}',
)


p.write_text(t, encoding="utf-8")
print("dashboard done")
