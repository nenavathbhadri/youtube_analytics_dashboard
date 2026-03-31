import os
import sys
import time
import re
import logging

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
from database.analytics_queries import get_recent_channels
from ui_theme import inject_theme

# ---------------- CONFIG ----------------
st.set_page_config(page_title="YouTube Analytics", layout="wide")
load_dotenv(os.path.join(BASE_DIR, ".env"))

logging.basicConfig(filename="app.log", level=logging.ERROR)

# ---------------- THEME ----------------
inject_theme()

# ---------------- HELPERS ----------------
def is_valid_channel_id(channel_id):
    return bool(re.match(r"^UC[a-zA-Z0-9_-]{22}$", channel_id))

def format_large_number(num):
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num/1_000:.2f}K"
    return str(num)

# ---------------- SESSION ----------------
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "page" not in st.session_state:
    st.session_state.page = 1

# ---------------- MODERN HEADER ----------------
st.markdown("""
<style>
.main-title {font-size:38px;font-weight:700;color:#2563eb;}
.card {padding:25px;border-radius:12px;border:1px solid #e5e7eb;}
.tip {padding:15px;background:#eff6ff;border-radius:10px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">YouTube Analytics — Dashboard</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3,1])

with col1:
    st.markdown("""
    <div class="card">
    <h3>Analyze YouTube Channels</h3>
    <p style="color:#6b7280;">Get deep insights into performance & engagement.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="tip">💡 Enter Channel ID below</div>', unsafe_allow_html=True)

st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## 📂 Recent Channels")
show_perf = st.sidebar.checkbox("⚡ Show Performance Metrics")

recent_channels = get_recent_channels(limit=5)
for _, row in recent_channels.iterrows():
    st.sidebar.write(row["channel_name"])

# ---------------- INPUT ----------------
channel_id = st.text_input("Enter YouTube Channel ID")

# ---------------- ANALYZE ----------------
if st.button("🚀 Analyze Channel"):

    try:
        if not is_valid_channel_id(channel_id):
            st.error("❌ Invalid Channel ID")
            st.stop()

        with st.spinner("Fetching data..."):

            start = time.time()
            channel_df = extract_channel_data(channel_id)
            video_df = extract_full_video_data(channel_id)
            st.session_state.fetch_time = round(time.time() - start, 2)

        if channel_df is None or video_df is None:
            st.error("Failed to fetch data")
            st.stop()

        start = time.time()
        results = run_full_transformation(
            video_df,
            channel_df["total_views"][0],
            channel_df["subscriber_count"][0]
        )
        st.session_state.transform_time = round(time.time() - start, 2)

        start = time.time()
        store_channel_data(channel_df, video_df)
        st.session_state.db_time = round(time.time() - start, 2)

        st.session_state.analysis_done = True
        st.session_state.channel_df = channel_df
        st.session_state.video_df = video_df
        st.session_state.results = results

    except Exception as e:
        logging.error(str(e))
        st.error("Something went wrong")

# ---------------- DASHBOARD ----------------
if st.session_state.analysis_done:

    channel_df = st.session_state.channel_df
    video_df = st.session_state.video_df
    results = st.session_state.results
    transformed_df = results["transformed_df"]

    tab1, tab2, tab3, tab4 = st.tabs([
        "📌 Overview",
        "🎥 Videos",
        "📊 Metrics",
        "📈 Trends"
    ])

    # -------- TAB 1 --------
    with tab1:
        k1, k2, k3 = st.columns(3)

        k1.metric("Subscribers", format_large_number(channel_df["subscriber_count"][0]))
        k2.metric("Videos", format_large_number(len(video_df)))
        k3.metric("Views", format_large_number(channel_df["total_views"][0]))

    # -------- TAB 2 --------
    with tab2:
        st.subheader("Video Data")

        page_size = 20
        start = (st.session_state.page - 1) * page_size
        end = start + page_size

        st.dataframe(video_df.iloc[start:end], use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("«") and st.session_state.page > 1:
                st.session_state.page -= 1

        with col2:
            if st.button("»") and end < len(video_df):
                st.session_state.page += 1

    # -------- TAB 3 --------
    with tab3:

        avg_duration = transformed_df["duration_seconds"].mean()
        avg_duration = 0 if pd.isna(avg_duration) else avg_duration

        k1, k2, k3, k4 = st.columns(4)

        k1.metric("Avg Views", round(results["avg_views"], 2),
                  help="Average views per video")

        k2.metric("Sub/View Ratio", round(results["subscriber_view_ratio"], 4),
                  help="Reach efficiency")

        k3.metric("Engagement %",
                  round(transformed_df["engagement_rate"].mean(), 2),
                  help="(Likes+Comments)/Views × 100")

        k4.metric("Avg Duration", f"{avg_duration:.2f}s")

    # -------- TAB 4 --------
    with tab4:

        st.subheader("Monthly Trend")
        fig1 = px.line(results["monthly_trend"], x="month", y="views")
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("Best Posting Time")
        fig2 = px.bar(results["optimal_posting_time"],
                      x="publish_hour", y="views")
        st.plotly_chart(fig2, use_container_width=True)

    # -------- PERFORMANCE --------
    if show_perf and "fetch_time" in st.session_state:

        st.divider()
        st.subheader("⚡ Performance Metrics")

        c1, c2, c3 = st.columns(3)
        c1.metric("Fetch Time", f"{st.session_state.fetch_time}s")
        c2.metric("Transform", f"{st.session_state.transform_time}s")
        c3.metric("DB Insert", f"{st.session_state.db_time}s")

# ---------------- FOOTER ----------------
st.caption("© 2026 YouTube Analytics Platform")