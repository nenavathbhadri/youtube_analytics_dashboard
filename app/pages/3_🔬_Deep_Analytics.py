import os, sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "app"))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from database.dashboard_queries import (
    get_all_channels,
    get_video_timeseries_data
)
from ui_theme import inject_theme, PLOTLY_DARK_TEMPLATE

st.set_page_config(page_title="Deep Analytics — TubeMetrics", layout="wide", page_icon="🔬")
inject_theme()

# ======================================================
# HEADER
# ======================================================
st.title("🔬 Deep Analytics")
st.markdown('<p class="page-subtitle">Heatmaps, distributions, engagement funnels, and advanced metric exploration</p>', unsafe_allow_html=True)

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

# =========================================================
# CHANNEL SELECTION
# =========================================================
channels_df = get_all_channels()

if channels_df.empty:
    st.warning("No channels found in database.")
    st.stop()

channel_options = {
    row["channel_name"]: row["channel_id"]
    for _, row in channels_df.iterrows()
}

selected_channel = st.selectbox(
    "Select Channel",
    list(channel_options.keys())
)

channel_id = channel_options[selected_channel]

df = get_video_timeseries_data(channel_id)

if df.empty:
    st.warning("No video data available.")
    st.stop()

df["publish_date"] = pd.to_datetime(df["publish_date"])
df["month"] = df["publish_date"].dt.month_name()
df["day"] = df["publish_date"].dt.day_name()
df["hour"] = df["publish_date"].dt.hour

# =========================================================
# 1️⃣ HEATMAP – Upload Frequency
# =========================================================
st.markdown("""
<div class="section-header">
<div class="icon">🔥</div>
<h3>Upload Frequency Heatmap</h3>
</div>
""", unsafe_allow_html=True)

heatmap_data = (
    df.groupby(["day", "month"])
    .size()
    .reset_index(name="count")
)

fig_heatmap = px.density_heatmap(
    heatmap_data,
    x="month",
    y="day",
    z="count",
    color_continuous_scale=["#0f0f1a", "#6C63FF", "#00D9FF"],
    template=PLOTLY_DARK_TEMPLATE
)

st.plotly_chart(style_chart(fig_heatmap), use_container_width=True)

# =========================================================
# 2️⃣ HISTOGRAM – View Distribution
# =========================================================
st.markdown("""
<div class="section-header">
<div class="icon">📊</div>
<h3>View Distribution Histogram</h3>
</div>
""", unsafe_allow_html=True)

fig_hist = px.histogram(
    df,
    x="views",
    nbins=40,
    template=PLOTLY_DARK_TEMPLATE,
    color_discrete_sequence=[COLORS[0]]
)

st.plotly_chart(style_chart(fig_hist), use_container_width=True)

# =========================================================
# 3️⃣ MULTI-LINE ENGAGEMENT TREND
# =========================================================
st.markdown("""
<div class="section-header">
<div class="icon">📈</div>
<h3>Engagement Trend Over Time</h3>
</div>
""", unsafe_allow_html=True)

df_sorted = df.sort_values("publish_date")

fig_multi = go.Figure()

fig_multi.add_trace(go.Scatter(
    x=df_sorted["publish_date"],
    y=df_sorted["views"],
    mode="lines",
    name="Views",
    line=dict(color=COLORS[0], width=2)
))

fig_multi.add_trace(go.Scatter(
    x=df_sorted["publish_date"],
    y=df_sorted["likes"],
    mode="lines",
    name="Likes",
    line=dict(color=COLORS[1], width=2)
))

fig_multi.add_trace(go.Scatter(
    x=df_sorted["publish_date"],
    y=df_sorted["comments"],
    mode="lines",
    name="Comments",
    line=dict(color=COLORS[2], width=2)
))

st.plotly_chart(style_chart(fig_multi), use_container_width=True)

# =========================================================
# 4️⃣ FUNNEL CHART – Drop-Off Analysis
# =========================================================
st.markdown("""
<div class="section-header">
<div class="icon">🔻</div>
<h3>Engagement Funnel</h3>
</div>
""", unsafe_allow_html=True)

total_views = df["views"].sum()
total_likes = df["likes"].sum()
total_comments = df["comments"].sum()

fig_funnel = go.Figure(go.Funnel(
    y=["Views", "Likes", "Comments"],
    x=[total_views, total_likes, total_comments],
    marker=dict(color=[COLORS[0], COLORS[1], COLORS[2]])
))

st.plotly_chart(style_chart(fig_funnel), use_container_width=True)

# =========================================================
# 5️⃣ METRIC TOGGLE
# =========================================================
st.markdown("""
<div class="section-header">
<div class="icon">📊</div>
<h3>Metric Selector</h3>
</div>
""", unsafe_allow_html=True)

metric_choice = st.selectbox(
    "Select Metric",
    ["views", "likes", "comments"]
)

fig_toggle = px.line(
    df_sorted,
    x="publish_date",
    y=metric_choice,
    template=PLOTLY_DARK_TEMPLATE,
    color_discrete_sequence=[COLORS[3]]
)

st.plotly_chart(style_chart(fig_toggle), use_container_width=True)

# =========================================================
# 6️⃣ DOWNLOAD CHART DATA
# =========================================================
st.markdown("""
<div class="section-header">
<div class="icon">⬇</div>
<h3>Download Data</h3>
</div>
""", unsafe_allow_html=True)

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Video Data as CSV",
    data=csv,
    file_name="video_data.csv",
    mime="text/csv"
)

# ======================================================
# FOOTER
# ======================================================
st.markdown('<div class="footer-text">© 2026 TubeMetrics — YouTube Analytics Platform</div>', unsafe_allow_html=True)
