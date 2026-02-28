import os
import sys

# -----------------------------
# Path Setup
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

import streamlit as st
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv

from metrics.metrics_calculator import run_full_transformation
from data_processing.channel_extractor import extract_channel_data
from data_processing.video_extractor import extract_full_video_data
from database.data_insertion import store_channel_data
from database.analytics_queries import (
    average_video_duration,
    get_recent_channels
)

# -----------------------------
# Page Config (MUST BE FIRST)
# -----------------------------
st.set_page_config(
    page_title="YouTube Analytics Platform",
    layout="wide"
)

# -----------------------------
# Global Styling (Enterprise)
# -----------------------------
st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

div[data-testid="metric-container"] {
    background-color: #f8f9fc;
    border: 1px solid #e6e9ef;
    padding: 15px;
    border-radius: 12px;
}

section[data-testid="stSidebar"] {
    background-color: #fafbfc;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Environment
# -----------------------------
load_dotenv(os.path.join(BASE_DIR, ".env"))

# ======================================================
# PROFESSIONAL HEADER (Clean SaaS Style)
# ======================================================

st.markdown("""
<div style="padding: 10px 0 20px 0;">
    <h1 style="
        font-size:42px;
        margin-bottom:5px;
        font-weight:700;
        color:#111827;
    ">
        📊 YouTube Channel Analytics Platform
    </h1>
    <p style="
        color:#6b7280;
        font-size:16px;
        margin-top:0;
    ">
        Advanced Performance Intelligence & Engagement Insights
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# =========================================
# Sidebar - Recently Analyzed
# =========================================
st.sidebar.markdown("## 📂 Recently Analyzed")

recent_channels = get_recent_channels(limit=5)

if not recent_channels.empty:
    for _, row in recent_channels.iterrows():
        st.sidebar.markdown(
            f"""
            <div style="
                padding:10px 12px;
                margin-bottom:8px;
                border-radius:8px;
                background-color:#f8fafc;">
            {row['channel_name']}
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.sidebar.info("No channels analyzed yet.")

# ======================================================
# INPUT
# ======================================================
channel_id = st.text_input("Enter YouTube Channel ID")

# ======================================================
# BUTTON ACTION
# ======================================================
if st.button("🚀 Analyze Channel"):

    if not channel_id:
        st.error("Please enter a Channel ID")
        st.stop()

    if not channel_id.startswith("UC"):
        st.error("Invalid Channel ID format")
        st.stop()

    try:
        progress = st.progress(0)
        status = st.empty()

        # STEP 1 – Fetch Channel
        status.write("🔍 Fetching channel data...")
        channel_df = extract_channel_data(channel_id)
        progress.progress(25)

        if channel_df is None:
            st.error("Channel not found")
            st.stop()

        # STEP 2 – Fetch Videos
        status.write("📂 Fetching video metadata...")
        video_df = extract_full_video_data(channel_id)
        progress.progress(50)

        # Derived metrics
        results = run_full_transformation(
            video_df,
            total_views=channel_df["total_views"][0],
            total_subscribers=channel_df["subscriber_count"][0]
        )

        transformed_df = results["transformed_df"]

        # STEP 3 – Store in Database
        status.write("💾 Storing data into database...")
        channel_status = store_channel_data(channel_df, video_df)
        progress.progress(75)

        status.write("📊 Preparing analytics...")
        progress.progress(100)

        st.success("Workflow Completed Successfully ✅")

        # ======================================================
        # ENTERPRISE TABS
        # ======================================================
        tab1, tab2, tab3, tab4 = st.tabs([
            "📌 Overview",
            "🎥 Video Analytics",
            "📊 Advanced Metrics",
            "📈 Trends"
        ])

        # ======================================================
        # TAB 1 – OVERVIEW
        # ======================================================
        with tab1:

            col1, col2 = st.columns([1, 3])

            with col1:
                st.image(channel_df["channel_thumbnail_url"][0], width=170)

            with col2:
                st.markdown(f"### {channel_df['channel_name'][0]}")
                st.write(channel_df["channel_description"][0])

            st.divider()

            k1, k2, k3 = st.columns(3)

            k1.metric("Subscribers", f"{channel_df['subscriber_count'][0]:,}")
            k2.metric("Total Videos", len(video_df))
            k3.metric("Total Views", f"{channel_df['total_views'][0]:,}")

        # ======================================================
        # TAB 2 – VIDEO ANALYTICS
        # ======================================================
        with tab2:

            st.subheader("Top 10 Most Viewed Videos")

            top_videos = video_df.sort_values("views", ascending=False).head(10)

            fig1 = px.bar(
                top_videos,
                x="title",
                y="views",
                template="simple_white"
            )

            fig1.update_layout(
                height=450,
                xaxis_tickangle=-40,
                margin=dict(l=20, r=20, t=40, b=20)
            )

            col1, col2 = st.columns([2, 1])

            with col1:
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                st.metric("Total Videos", len(video_df))
                st.metric("Avg Views", round(video_df["views"].mean()))

            st.dataframe(top_videos, use_container_width=True)

        # ======================================================
        # TAB 3 – ADVANCED METRICS
        # ======================================================
        with tab3:

            st.subheader("Performance KPIs")

            duration_df = average_video_duration(channel_id)

            avg_duration = (
                duration_df["avg_duration_seconds"][0]
                if not duration_df.empty and
                duration_df["avg_duration_seconds"][0] is not None
                else 0
            )

            k1, k2, k3, k4 = st.columns(4)

            k1.metric("Avg Views / Video", round(results["avg_views"], 2))
            k2.metric("Subscriber / View Ratio", round(results["subscriber_view_ratio"], 4))
            k3.metric("Avg Engagement Rate (%)",
                      round(transformed_df["engagement_rate"].mean(), 2))
            k4.metric("Avg Duration (sec)", round(avg_duration, 2))

            st.divider()

            st.subheader("Video Performance Benchmark")

            benchmark_df = transformed_df.sort_values("views", ascending=False)

            st.dataframe(
                benchmark_df[[
                    "title",
                    "views",
                    "engagement_rate",
                    "vs_channel_avg"
                ]],
                use_container_width=True
            )

        # ======================================================
        # TAB 4 – TRENDS
        # ======================================================
        with tab4:

            st.subheader("Monthly Upload Trend")

            monthly = results["monthly_trend"]

            fig2 = px.line(
                monthly,
                x="month",
                y="views",
                markers=True,
                template="simple_white"
            )

            fig2.update_layout(
                height=450,
                margin=dict(l=20, r=20, t=40, b=20)
            )

            st.plotly_chart(fig2, use_container_width=True)

            st.divider()

            st.subheader("Optimal Posting Hour")

            optimal = results["optimal_posting_time"]

            fig3 = px.bar(
                optimal,
                x="publish_hour",
                y="views",
                template="simple_white"
            )

            fig3.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=40, b=20)
            )

            st.plotly_chart(fig3, use_container_width=True)

        st.divider()
        st.caption("© 2026 YouTube Analytics Platform | Built with Streamlit & SQLAlchemy")

    except Exception as e:
        st.error(f"Something went wrong: {e}")