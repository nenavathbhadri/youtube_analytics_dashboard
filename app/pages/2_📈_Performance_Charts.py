import os, sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "app"))

import streamlit as st
import plotly.express as px
import pandas as pd
from database.dashboard_queries import (
    get_all_channels,
    get_views_over_time,
    get_top_10_videos,
    get_upload_distribution
)
from ui_theme import inject_theme, PLOTLY_DARK_TEMPLATE

st.set_page_config(page_title="Performance Charts — TubeMetrics", layout="wide", page_icon="📈")
inject_theme()

# ======================================================
# HEADER
# ======================================================
st.title("📈 Performance Charts")
st.markdown('<p class="page-subtitle">Visualize views, top videos, uploads, and engagement patterns</p>', unsafe_allow_html=True)

# ======================================================
# Sidebar Channel Selection
# ======================================================
st.sidebar.header("Select Channel")

channels_df = get_all_channels()

if channels_df.empty:
    st.warning("No channels available.")
    st.stop()

channel_options = {
    row["channel_name"]: row["channel_id"]
    for _, row in channels_df.iterrows()
}

selected_channel_name = st.sidebar.selectbox(
    "Choose Channel",
    list(channel_options.keys())
)

selected_channel_id = channel_options[selected_channel_name]

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
# 1️⃣ Views Over Time (Line Chart)
# ======================================================
st.markdown("""
<div class="section-header">
<div class="icon">📈</div>
<h3>Views Over Time</h3>
</div>
""", unsafe_allow_html=True)

views_df = get_views_over_time(selected_channel_id)

if not views_df.empty:

    fig1 = px.line(
        views_df,
        x="publish_date",
        y="total_views",
        markers=True,
        template=PLOTLY_DARK_TEMPLATE,
        title="Views Trend Over Time",
        color_discrete_sequence=[COLORS[0]]
    )

    st.plotly_chart(style_chart(fig1), use_container_width=True)
else:
    st.info("No view trend data available.")

st.divider()

# ======================================================
# 2️⃣ Top 10 Most Viewed Videos (Bar Chart)
# ======================================================
st.markdown("""
<div class="section-header">
<div class="icon">🔝</div>
<h3>Top 10 Most Viewed Videos</h3>
</div>
""", unsafe_allow_html=True)

top_videos_df = get_top_10_videos(selected_channel_id)

if not top_videos_df.empty:

    fig2 = px.bar(
        top_videos_df,
        x="title",
        y="views",
        hover_data=["likes", "comments"],
        template=PLOTLY_DARK_TEMPLATE,
        title="Top 10 Videos by Views",
        color_discrete_sequence=[COLORS[1]]
    )

    fig2.update_layout(xaxis_tickangle=-40)

    st.plotly_chart(style_chart(fig2), use_container_width=True)
else:
    st.info("No top videos available.")

st.divider()

# ======================================================
# 3️⃣ Monthly Upload Distribution (Pie Chart)
# ======================================================
st.markdown("""
<div class="section-header">
<div class="icon">🗓</div>
<h3>Monthly Upload Distribution</h3>
</div>
""", unsafe_allow_html=True)

upload_df = get_upload_distribution(selected_channel_id)

if not upload_df.empty:

    fig3 = px.pie(
        upload_df,
        names="upload_month",
        values="total_videos",
        template=PLOTLY_DARK_TEMPLATE,
        title="Monthly Video Distribution",
        hole=0.4,
        color_discrete_sequence=COLORS
    )

    fig3.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Videos: %{value}<br>Percentage: %{percent}"
    )

    st.plotly_chart(style_chart(fig3), use_container_width=True)

else:
    st.info("No upload distribution data available.")

st.divider()

# ======================================================
# 4️⃣ Scatter Plot - Views vs Engagement
# ======================================================
st.markdown("""
<div class="section-header">
<div class="icon">📊</div>
<h3>Views vs Engagement</h3>
</div>
""", unsafe_allow_html=True)

if not top_videos_df.empty:

    top_videos_df["engagement"] = (
        top_videos_df["likes"] + top_videos_df["comments"]
    )

    fig4 = px.scatter(
        top_videos_df,
        x="views",
        y="engagement",
        size="engagement",
        hover_name="title",
        template=PLOTLY_DARK_TEMPLATE,
        title="Views vs Engagement",
        color_discrete_sequence=[COLORS[2]]
    )

    st.plotly_chart(style_chart(fig4), use_container_width=True)
else:
    st.info("No scatter data available.")

# ======================================================
# FOOTER
# ======================================================
st.markdown('<div class="footer-text">© 2026 TubeMetrics — YouTube Analytics Platform</div>', unsafe_allow_html=True)
