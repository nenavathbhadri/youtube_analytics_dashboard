import os, sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "app"))

import streamlit as st
import pandas as pd
import plotly.express as px

from database.dashboard_queries import get_all_channels
from database.comparison_queries import (
    get_channel_comparison,
    get_views_trend,
    benchmark_engagement,
    leaderboard
)
from ui_theme import inject_theme, PLOTLY_DARK_TEMPLATE

st.set_page_config(page_title="Channel Comparison — TubeMetrics", layout="wide", page_icon="⚔")
inject_theme()

# Chart color palette
COLORS = ["#6C63FF", "#00D9FF", "#FF6B6B", "#00C853", "#FF8E53", "#A78BFA"]

def style_chart(fig):
    """Apply consistent dark styling to a plotly figure."""
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E8E8F0"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        legend=dict(font=dict(color="#9CA3AF"))
    )
    return fig

# ======================================================
# HEADER
# ======================================================
st.title("⚔ Channel Comparison")
st.markdown('<p class="page-subtitle">Compare channels head-to-head with KPIs, trends, and leaderboards</p>', unsafe_allow_html=True)

# ------------------------------------------------
# Channel Selection
# ------------------------------------------------
channels_df = get_all_channels()

channel_map = {
    row["channel_name"]: row["channel_id"]
    for _, row in channels_df.iterrows()
}

selected_channels = st.multiselect(
    "Select Channels to Compare (max 3)",
    list(channel_map.keys()),
    max_selections=3
)

if not selected_channels:
    st.info("Select channels to start comparison.")
    st.stop()

channel_ids = [channel_map[ch] for ch in selected_channels]

# ------------------------------------------------
# KPI Comparison Table
# ------------------------------------------------
st.markdown("""
<div class="section-header">
<div class="icon">📊</div>
<h3>Channel KPI Comparison</h3>
</div>
""", unsafe_allow_html=True)

comparison_df = get_channel_comparison(channel_ids)

st.dataframe(comparison_df, use_container_width=True)

# ------------------------------------------------
# Trend Comparison Chart
# ------------------------------------------------
st.markdown("""
<div class="section-header">
<div class="icon">📈</div>
<h3>Views Trend Comparison</h3>
</div>
""", unsafe_allow_html=True)

trend_df = get_views_trend(channel_ids)

if not trend_df.empty:

    fig = px.line(
        trend_df,
        x="date",
        y="views",
        color="channel_id",
        markers=True,
        template=PLOTLY_DARK_TEMPLATE,
        color_discrete_sequence=COLORS
    )

    st.plotly_chart(style_chart(fig), use_container_width=True)

# ------------------------------------------------
# Benchmark Analysis
# ------------------------------------------------
st.markdown("""
<div class="section-header">
<div class="icon">🏆</div>
<h3>Benchmark Engagement</h3>
</div>
""", unsafe_allow_html=True)

benchmark_df = benchmark_engagement()

fig2 = px.bar(
    benchmark_df,
    x="channel_name",
    y="engagement_rate",
    title="Channel Engagement Rate (%)",
    template=PLOTLY_DARK_TEMPLATE,
    color_discrete_sequence=[COLORS[1]]
)

st.plotly_chart(style_chart(fig2), use_container_width=True)

# ------------------------------------------------
# Leaderboard Ranking
# ------------------------------------------------
st.markdown("""
<div class="section-header">
<div class="icon">🥇</div>
<h3>Leaderboard Ranking</h3>
</div>
""", unsafe_allow_html=True)

metric = st.selectbox(
    "Select Ranking Metric",
    ["Subscribers", "Total Views", "Videos"]
)

leaderboard_df = leaderboard(metric)

st.dataframe(leaderboard_df, use_container_width=True)

# ------------------------------------------------
# Export Report
# ------------------------------------------------
st.markdown("""
<div class="section-header">
<div class="icon">⬇</div>
<h3>Export Comparison</h3>
</div>
""", unsafe_allow_html=True)

csv = comparison_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download CSV Report",
    csv,
    "channel_comparison.csv",
    "text/csv"
)

# ======================================================
# FOOTER
# ======================================================
st.markdown('<div class="footer-text">© 2026 TubeMetrics — YouTube Analytics Platform</div>', unsafe_allow_html=True)
