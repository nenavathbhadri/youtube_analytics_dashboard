"""
Shared UI Theme for YouTube Analytics Dashboard
Supports dark/light mode toggle via session state.
"""
import streamlit as st

DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
    color: #E8E8F0;
}
[data-testid="stHeader"] {
    background: rgba(15, 15, 26, 0.8);
    backdrop-filter: blur(20px);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12122a 0%, #0d0d1f 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
h1, h2, h3 { color: #E8E8F0 !important; font-family: 'Inter', sans-serif !important; }
p, label { font-family: 'Inter', sans-serif !important; }

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 18px 22px;
    transition: all 0.3s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(108,99,255,0.15);
}
[data-testid="stMetric"] label { color: #9CA3AF !important; font-size: 0.85rem !important; text-transform: uppercase; letter-spacing: 0.04em; }
[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #E8E8F0 !important; font-weight: 700 !important; }

.stButton > button {
    background: linear-gradient(135deg, #6C63FF, #00D9FF) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    font-weight: 600 !important; transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(108,99,255,0.3) !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; filter: brightness(1.1) !important; }

.stDownloadButton > button {
    background: rgba(0,200,83,0.12) !important; color: #00C853 !important;
    border: 1px solid rgba(0,200,83,0.3) !important; border-radius: 10px !important;
}

.stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.04); border-radius: 12px; padding: 4px; border: 1px solid rgba(255,255,255,0.08); }
.stTabs [data-baseweb="tab"] { color: #9CA3AF !important; border-radius: 8px; transition: all 0.3s ease; }
.stTabs [aria-selected="true"] { background: rgba(108,99,255,0.18) !important; color: #00D9FF !important; }

.stTextInput > div > div > input { background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 10px !important; color: #E8E8F0 !important; }
.stTextInput > div > div > input:focus { border-color: #6C63FF !important; box-shadow: 0 0 0 3px rgba(108,99,255,0.3) !important; }

[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; border: 1px solid rgba(255,255,255,0.08); }
hr { border-color: rgba(255,255,255,0.08) !important; }

.theme-toggle-btn { cursor: pointer; font-size: 1.4rem; padding: 6px 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.06); transition: all 0.3s ease; }
.theme-toggle-btn:hover { background: rgba(255,255,255,0.12); transform: scale(1.1); }
</style>
"""

LIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #f8f9fc 0%, #eef1f8 100%);
    color: #1a1a2e;
}
[data-testid="stHeader"] {
    background: rgba(248, 249, 252, 0.9);
    backdrop-filter: blur(20px);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f3f4f8 100%);
    border-right: 1px solid #e2e5ed;
}
h1, h2, h3 { color: #1a1a2e !important; font-family: 'Inter', sans-serif !important; }
p, label { font-family: 'Inter', sans-serif !important; }

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e2e5ed;
    border-radius: 14px;
    padding: 18px 22px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    transition: all 0.3s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(37,99,235,0.12);
}
[data-testid="stMetric"] label { color: #6b7280 !important; font-size: 0.85rem !important; text-transform: uppercase; letter-spacing: 0.04em; }
[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #1a1a2e !important; font-weight: 700 !important; }

.stButton > button {
    background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    font-weight: 600 !important; transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(37,99,235,0.25) !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; filter: brightness(1.1) !important; }

.stDownloadButton > button {
    background: rgba(0,200,83,0.08) !important; color: #059669 !important;
    border: 1px solid rgba(5,150,105,0.3) !important; border-radius: 10px !important;
}

.stTabs [data-baseweb="tab-list"] { background: white; border-radius: 12px; padding: 4px; border: 1px solid #e2e5ed; }
.stTabs [data-baseweb="tab"] { color: #6b7280 !important; border-radius: 8px; transition: all 0.3s ease; }
.stTabs [aria-selected="true"] { background: rgba(37,99,235,0.1) !important; color: #2563eb !important; }

.stTextInput > div > div > input { background: white !important; border: 1px solid #e2e5ed !important; border-radius: 10px !important; color: #1a1a2e !important; }
.stTextInput > div > div > input:focus { border-color: #2563eb !important; box-shadow: 0 0 0 3px rgba(37,99,235,0.15) !important; }

[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; border: 1px solid #e2e5ed; }
hr { border-color: #e2e5ed !important; }

.theme-toggle-btn { cursor: pointer; font-size: 1.4rem; padding: 6px 12px; border-radius: 10px; border: 1px solid #e2e5ed; background: white; transition: all 0.3s ease; }
.theme-toggle-btn:hover { background: #f3f4f6; transform: scale(1.1); }
</style>
"""

PLOTLY_DARK_TEMPLATE = "plotly_dark"
PLOTLY_LIGHT_TEMPLATE = "simple_white"


def get_plotly_template():
    """Return the appropriate Plotly template based on current theme."""
    if st.session_state.get("theme", "light") == "dark":
        return PLOTLY_DARK_TEMPLATE
    return PLOTLY_LIGHT_TEMPLATE


def inject_theme():
    """Inject theme CSS and render the toggle button at top-right."""
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

    # Theme toggle in top-right using columns
    _, toggle_col = st.columns([9, 1])
    with toggle_col:
        icon = "🌙" if st.session_state.theme == "light" else "☀️"
        if st.button(icon, key="theme_toggle", help="Toggle Dark/Light Mode"):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.rerun()

    # Inject the right CSS
    if st.session_state.theme == "dark":
        st.markdown(DARK_CSS, unsafe_allow_html=True)
    else:
        st.markdown(LIGHT_CSS, unsafe_allow_html=True)
