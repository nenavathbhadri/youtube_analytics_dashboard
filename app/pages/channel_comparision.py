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

st.set_page_config(page_title="Channel Comparison", layout="wide")

st.title("📊 Channel Comparative Analytics")

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
st.subheader("📊 Channel KPI Comparison")

comparison_df = get_channel_comparison(channel_ids)

st.dataframe(comparison_df, use_container_width=True)

# ------------------------------------------------
# Trend Comparison Chart
# ------------------------------------------------
st.subheader("📈 Views Trend Comparison")

trend_df = get_views_trend(channel_ids)

if not trend_df.empty:

    fig = px.line(
        trend_df,
        x="date",
        y="views",
        color="channel_id",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------
# Benchmark Analysis
# ------------------------------------------------
st.subheader("🏆 Benchmark Engagement")

benchmark_df = benchmark_engagement()

fig2 = px.bar(
    benchmark_df,
    x="channel_name",
    y="engagement_rate",
    title="Channel Engagement Rate (%)"
)

st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------------------
# Leaderboard Ranking
# ------------------------------------------------
st.subheader("🥇 Leaderboard Ranking")

metric = st.selectbox(
    "Select Ranking Metric",
    ["Subscribers", "Total Views", "Videos"]
)

leaderboard_df = leaderboard(metric)

st.dataframe(leaderboard_df, use_container_width=True)

# ------------------------------------------------
# Export Report
# ------------------------------------------------
st.subheader("⬇ Export Comparison")

csv = comparison_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV Report",
    csv,
    "channel_comparison.csv",
    "text/csv"
)