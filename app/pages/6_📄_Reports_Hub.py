import os, sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "app"))

import streamlit as st
import json

from reports.export_utils import export_csv, export_excel
from reports.pdf_report import generate_pdf_report
from reports.report_builder import build_custom_report
from reports.template_manager import save_template, load_templates
from ui_theme import inject_theme

st.set_page_config(page_title="Reports Hub — TubeMetrics", layout="wide", page_icon="📄")
inject_theme()

# ======================================================
# HEADER
# ======================================================
st.title("📄 Reports Hub")
st.markdown('<p class="page-subtitle">Export data, generate custom reports, and manage report templates</p>', unsafe_allow_html=True)

# ---------------- CHECK DATA ----------------
if "analysis_done" not in st.session_state or not st.session_state.analysis_done:
    st.warning("⚠ Please analyze a channel first from the Home page")
    st.stop()

channel_df = st.session_state.channel_df
video_df = st.session_state.video_df
results = st.session_state.results

# ---------------- EXPORT ----------------
st.markdown("""
<div class="section-header">
<div class="icon">⬇</div>
<h3>Export Data</h3>
</div>
""", unsafe_allow_html=True)

csv_data = export_csv(video_df)
excel_data = export_excel(video_df)

metrics = {
    "Subscribers": channel_df["subscriber_count"][0],
    "Videos": len(video_df),
    "Views": channel_df["total_views"][0]
}

pdf_file = generate_pdf_report(
    channel_df["channel_name"][0],
    metrics,
    []
)

col1, col2, col3 = st.columns(3)

with col1:
    st.download_button("📥 CSV", csv_data, "data.csv")

with col2:
    st.download_button("📥 Excel", excel_data, "data.xlsx")

with col3:
    st.download_button("📥 PDF", pdf_file, "report.pdf")

st.divider()

# ---------------- CUSTOM REPORT ----------------
st.markdown("""
<div class="section-header">
<div class="icon">🧩</div>
<h3>Custom Report Builder</h3>
</div>
""", unsafe_allow_html=True)

options = st.multiselect(
    "Select sections to include",
    ["Subscribers","Top Videos","Trends"]
)

if st.button("🔨 Generate Report"):

    report_data = build_custom_report(options, channel_df, video_df)

    pdf = generate_pdf_report(
        channel_df["channel_name"][0],
        report_data,
        []
    )

    st.download_button("📥 Download Custom Report", pdf, "custom.pdf")

st.divider()

# ---------------- TEMPLATE ----------------
st.markdown("""
<div class="section-header">
<div class="icon">💾</div>
<h3>Report Templates</h3>
</div>
""", unsafe_allow_html=True)

name = st.text_input("Template Name", placeholder="e.g. Monthly Summary")

if st.button("💾 Save Template"):
    save_template(name, options)
    st.success("✅ Template saved successfully!")

templates = load_templates()

if templates:
    names = [t[1] for t in templates]
    selected = st.selectbox("Load Template", names)

    if st.button("▶ Apply Template"):
        for t in templates:
            if t[1] == selected:
                options = json.loads(t[2])
                st.success("✅ Template applied!")

st.divider()

# ---------------- HELP ----------------
st.markdown("""
<div class="section-header">
<div class="icon">❓</div>
<h3>Help & Documentation</h3>
</div>
""", unsafe_allow_html=True)

with st.expander("📐 Key Metrics Explained"):
    st.markdown("""
    | Metric | Formula | What It Means |
    |--------|---------|---------------|
    | **Engagement Rate** | (Likes + Comments) / Views × 100 | How actively viewers interact with content |
    | **Sub/View Ratio** | Subscribers / Total Views | Measures how efficiently views convert to subscribers |
    | **Avg Views** | Total Views / Total Videos | Average performance per video |
    | **Avg Duration** | Sum of durations / Total Videos | Typical video length on the channel |
    """)

with st.expander("📖 How to Use — Step by Step"):
    st.markdown("""
    1. **Go to the Home page** and enter a valid YouTube Channel ID (starts with `UC`)
    2. **Click "Analyze Channel"** — the system fetches channel & video data via the YouTube API
    3. **Explore the tabs** on the Home page for a quick overview of subscribers, videos, and trends
    4. **Visit other pages** from the sidebar:
       - 📊 **Channel Insights** — Detailed KPIs and channel comparison
       - 📈 **Performance Charts** — Views over time, top videos, upload distribution
       - 🔬 **Deep Analytics** — Heatmaps, funnels, histograms, and metric selectors
       - ⚔ **Channel Comparison** — Compare up to 3 channels side by side
       - 🔍 **Video Explorer** — Search and filter videos with advanced options
    5. **Come to Reports Hub** to export your data as CSV, Excel, or PDF
    """)

with st.expander("📁 Export Formats"):
    st.markdown("""
    | Format | Best For |
    |--------|----------|
    | **CSV** | Importing into spreadsheets, data analysis tools, or databases |
    | **Excel** | Sharing formatted reports with teams, presentations |
    | **PDF** | Printable summaries, client-ready reports |
    """)

with st.expander("💾 Using Templates"):
    st.markdown("""
    **Save a Template:**
    1. Select the report sections you want (Subscribers, Top Videos, Trends)
    2. Enter a template name (e.g., "Weekly Review")
    3. Click **Save Template**

    **Load a Template:**
    1. Select a saved template from the dropdown
    2. Click **Apply Template** — sections will be pre-selected
    3. Click **Generate Report** to create the PDF
    """)

with st.expander("🔑 Where to Find a Channel ID"):
    st.markdown("""
    1. Go to the YouTube channel page
    2. Look at the URL — format: `youtube.com/channel/UCxxxxxxxxxxxxxxxxxxxxxxxx`
    3. Copy the part starting with `UC` (24 characters total)

    **Example:** `UCq-Fj5jknLsUf-MWSy4_brA`
    """)

# ======================================================
# FOOTER
# ======================================================
st.markdown('<div class="footer-text">© 2026 TubeMetrics — YouTube Analytics Platform</div>', unsafe_allow_html=True)
