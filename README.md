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
}