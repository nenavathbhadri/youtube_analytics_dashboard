import streamlit as st
import plotly.express as px
import pandas as pd
from database.dashboard_queries import (
    get_all_channels,
    get_views_over_time,
    get_top_10_videos,
    get_upload_distribution
)

st.set_page_config(page_title="Visualizations - Part 1", layout="wide")

st.title("📊 Data Visualization Dashboard (Part 1)")

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

# ======================================================
# 1️⃣ Views Over Time (Line Chart)
# ======================================================
st.subheader("📈 Views Over Time")

views_df = get_views_over_time(selected_channel_id)

if not views_df.empty:

    fig1 = px.line(
        views_df,
        x="publish_date",
        y="total_views",
        markers=True,
        template="simple_white",
        title="Views Trend Over Time"
    )

    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("No view trend data available.")

st.divider()

# ======================================================
# 2️⃣ Top 10 Most Viewed Videos (Bar Chart)
# ======================================================
st.subheader("🔝 Top 10 Most Viewed Videos")

top_videos_df = get_top_10_videos(selected_channel_id)

if not top_videos_df.empty:

    fig2 = px.bar(
        top_videos_df,
        x="title",
        y="views",
        hover_data=["likes", "comments"],
        template="simple_white",
        title="Top 10 Videos by Views"
    )

    fig2.update_layout(xaxis_tickangle=-40)

    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No top videos available.")

st.divider()

# ======================================================
# 3️⃣ Monthly Upload Distribution (Pie Chart)
# ======================================================
st.subheader("🗓 Monthly Upload Distribution")

upload_df = get_upload_distribution(selected_channel_id)

if not upload_df.empty:

    fig3 = px.pie(
        upload_df,
        names="upload_month",
        values="total_videos",
        template="simple_white",
        title="Monthly Video Distribution",
        hole=0.4  # Makes it look more modern (donut style)
    )

    fig3.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Videos: %{value}<br>Percentage: %{percent}"
    )

    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("No upload distribution data available.")

st.divider()

# ======================================================
# 4️⃣ Scatter Plot - Views vs Engagement
# ======================================================
st.subheader("📊 Views vs Engagement")

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
        template="simple_white",
        title="Views vs Engagement"
    )

    st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("No scatter data available.")