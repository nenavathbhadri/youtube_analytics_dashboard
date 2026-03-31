from sqlalchemy import text
import pandas as pd
from database.db import get_engine

engine = get_engine()

# 1️⃣ Top 10 Most Viewed
def top_10_most_viewed(channel_id):
    query = text("""
        SELECT v.title, vs.views
        FROM videos v
        JOIN video_statistics vs
        ON v.video_id = vs.video_id
        WHERE v.channel_id = :channel_id
        ORDER BY vs.views DESC
        LIMIT 10
    """)
    return pd.read_sql(query, engine, params={"channel_id": channel_id})


# 2️⃣ Highest Engagement Videos
def highest_engagement_videos(channel_id):
    query = text("""
        SELECT 
            v.title,
            vs.views,
            vs.likes,
            vs.comments,
            (vs.likes + vs.comments)/vs.views AS engagement_rate
        FROM videos v
        JOIN video_statistics vs
        ON v.video_id = vs.video_id
        WHERE v.channel_id = :channel_id
        AND vs.views > 0
        ORDER BY engagement_rate DESC
        LIMIT 10
    """)
    return pd.read_sql(query, engine, params={"channel_id": channel_id})
import streamlit as st
@st.cache_data(show_spinner=False)
def average_video_duration(channel_id):
    query = text("""
        SELECT 
            AVG(duration_seconds) AS avg_duration_seconds
        FROM videos
        WHERE channel_id = :channel_id
          AND duration_seconds IS NOT NULL
    """)

    return pd.read_sql(query, engine, params={"channel_id": channel_id})


# 4️⃣ Posting Frequency
def posting_frequency_analysis(channel_id):
    query = text("""
        SELECT COUNT(*) AS total_videos
        FROM videos
        WHERE channel_id = :channel_id
    """)
    return pd.read_sql(query, engine, params={"channel_id": channel_id})


# 5️⃣ Monthly Upload Trend
def monthly_upload_trend(channel_id):
    query = text("""
        SELECT 
            DATE_FORMAT(publish_date, '%%Y-%%m') AS month,
            COUNT(*) AS videos_uploaded
        FROM videos
        WHERE channel_id = :channel_id
        GROUP BY month
        ORDER BY month
    """)
    return pd.read_sql(query, engine, params={"channel_id": channel_id})


# 6️⃣ Recently Analyzed Channels
def get_recent_channels(limit=5):
    query = text("""
        SELECT channel_name, channel_id
        FROM channels
        ORDER BY created_date DESC
        LIMIT :limit
    """)
    return pd.read_sql(query, engine, params={"limit": limit})