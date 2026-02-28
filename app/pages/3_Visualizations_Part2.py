import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from database.dashboard_queries import (
    get_all_channels,
    get_video_timeseries_data
)

st.set_page_config(page_title="Advanced Visualizations", layout="wide")

st.title("📊 Advanced Analytics & Insights")

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
st.subheader("🔥 Upload Frequency Heatmap")

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
    color_continuous_scale="Blues"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# =========================================================
# 2️⃣ HISTOGRAM – View Distribution
# =========================================================
st.subheader("📊 View Distribution Histogram")

fig_hist = px.histogram(
    df,
    x="views",
    nbins=40,
    template="simple_white"
)

st.plotly_chart(fig_hist, use_container_width=True)

# =========================================================
# 3️⃣ MULTI-LINE ENGAGEMENT TREND
# =========================================================
st.subheader("📈 Engagement Trend Over Time")

df_sorted = df.sort_values("publish_date")

fig_multi = go.Figure()

fig_multi.add_trace(go.Scatter(
    x=df_sorted["publish_date"],
    y=df_sorted["views"],
    mode="lines",
    name="Views"
))

fig_multi.add_trace(go.Scatter(
    x=df_sorted["publish_date"],
    y=df_sorted["likes"],
    mode="lines",
    name="Likes"
))

fig_multi.add_trace(go.Scatter(
    x=df_sorted["publish_date"],
    y=df_sorted["comments"],
    mode="lines",
    name="Comments"
))

st.plotly_chart(fig_multi, use_container_width=True)

# =========================================================
# 4️⃣ FUNNEL CHART – Drop-Off Analysis
# =========================================================
st.subheader("🔻 Engagement Funnel")

total_views = df["views"].sum()
total_likes = df["likes"].sum()
total_comments = df["comments"].sum()

fig_funnel = go.Figure(go.Funnel(
    y=["Views", "Likes", "Comments"],
    x=[total_views, total_likes, total_comments]
))

st.plotly_chart(fig_funnel, use_container_width=True)

# =========================================================
# 5️⃣ METRIC TOGGLE
# =========================================================
st.subheader("📊 Metric Selector")

metric_choice = st.selectbox(
    "Select Metric",
    ["views", "likes", "comments"]
)

fig_toggle = px.line(
    df_sorted,
    x="publish_date",
    y=metric_choice,
    template="simple_white"
)

st.plotly_chart(fig_toggle, use_container_width=True)

# =========================================================
# 6️⃣ DOWNLOAD CHART DATA
# =========================================================
st.subheader("⬇ Download Data")

csv = df.to_csv(index=False)

st.download_button(
    label="Download Video Data as CSV",
    data=csv,
    file_name="video_data.csv",
    mime="text/csv"
)