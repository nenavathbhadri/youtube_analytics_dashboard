from sqlalchemy import text
import pandas as pd
from database.db import get_engine

engine = get_engine()

# =====================================================
# 1️⃣ Get All Channels (for sidebar dropdown)
# =====================================================
def get_all_channels():
    query = text("""
        SELECT channel_id, channel_name
        FROM channels
        ORDER BY channel_name
    """)
    return pd.read_sql(query, engine)


# =====================================================
# 2️⃣ Get Channel KPI Metrics
# =====================================================
def get_channel_kpis(channel_id):
    query = text("""
        SELECT 
            c.channel_name,
            c.subscribers,
            c.total_videos,
            c.total_views,
            AVG(
                CASE 
                    WHEN vs.views > 0 
                    THEN (vs.likes + vs.comments) / vs.views
                    ELSE 0
                END
            ) * 100 AS avg_engagement
        FROM channels c
        JOIN videos v ON c.channel_id = v.channel_id
        JOIN video_statistics vs ON v.video_id = vs.video_id
        WHERE c.channel_id = :channel_id
        GROUP BY 
            c.channel_name,
            c.subscribers,
            c.total_videos,
            c.total_views
    """)

    return pd.read_sql(
        query,
        engine,
        params={"channel_id": channel_id}
    )
# =====================================================
# Views Over Time
# =====================================================
def get_views_over_time(channel_id):
    query = text("""
        SELECT 
            DATE(v.publish_date) as publish_date,
            SUM(vs.views) as total_views
        FROM videos v
        JOIN video_statistics vs 
            ON v.video_id = vs.video_id
        WHERE v.channel_id = :channel_id
        GROUP BY DATE(v.publish_date)
        ORDER BY publish_date
    """)
    return pd.read_sql(query, engine, params={"channel_id": channel_id})


# =====================================================
# Top 10 Most Viewed Videos
# =====================================================
def get_top_10_videos(channel_id):
    query = text("""
        SELECT 
            v.title,
            vs.views,
            vs.likes,
            vs.comments
        FROM videos v
        JOIN video_statistics vs 
            ON v.video_id = vs.video_id
        WHERE v.channel_id = :channel_id
        ORDER BY vs.views DESC
        LIMIT 10
    """)
    return pd.read_sql(query, engine, params={"channel_id": channel_id})


# =====================================================
# Upload Distribution By Year
# =====================================================
def get_upload_distribution(channel_id):
    query = text("""
        SELECT 
            DATE_FORMAT(publish_date, '%Y-%m') as upload_month,
            COUNT(*) as total_videos
        FROM videos
        WHERE channel_id = :channel_id
        GROUP BY upload_month
        ORDER BY upload_month
    """)
    return pd.read_sql(query, engine, params={"channel_id": channel_id})


def get_video_timeseries_data(channel_id):
    query = text("""
        SELECT v.video_id,
               v.title,
               v.publish_date,
               s.views,
               s.likes,
               s.comments
        FROM videos v
        JOIN video_statistics s
        ON v.video_id = s.video_id
        WHERE v.channel_id = :channel_id
    """)
    return pd.read_sql(query, engine, params={"channel_id": channel_id})