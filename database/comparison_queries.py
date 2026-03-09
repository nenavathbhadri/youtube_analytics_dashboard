from sqlalchemy import text
import pandas as pd
from database.db import get_engine

engine = get_engine()
# ------------------------------------------------
# Channel KPI Comparison
# ------------------------------------------------
def get_channel_comparison(channel_ids):

    query = text("""
        SELECT 
            c.channel_id,
            c.channel_name,
            c.subscribers,
            c.total_views,
            c.total_videos
        FROM channels c
        WHERE c.channel_id IN :channel_ids
    """)

    return pd.read_sql(query, engine, params={"channel_ids": tuple(channel_ids)})


# ------------------------------------------------
# Views Trend Comparison
# ------------------------------------------------
def get_views_trend(channel_ids):

    query = text("""
        SELECT 
            v.channel_id,
            DATE(v.publish_date) AS date,
            SUM(vs.views) AS views
        FROM videos v
        JOIN video_statistics vs
        ON v.video_id = vs.video_id
        WHERE v.channel_id IN :channel_ids
        GROUP BY v.channel_id, DATE(v.publish_date)
        ORDER BY date
    """)

    return pd.read_sql(query, engine, params={"channel_ids": tuple(channel_ids)})


# ------------------------------------------------
# Benchmark Engagement
# ------------------------------------------------
def benchmark_engagement():

    query = text("""
        SELECT 
            c.channel_name,
            AVG((vs.likes + vs.comments) / NULLIF(vs.views,0)) * 100 AS engagement_rate
        FROM channels c
        JOIN videos v
        ON c.channel_id = v.channel_id
        JOIN video_statistics vs
        ON v.video_id = vs.video_id
        GROUP BY c.channel_name
    """)

    return pd.read_sql(query, engine)


# ------------------------------------------------
# Leaderboard Ranking
# ------------------------------------------------
def leaderboard(metric):

    allowed = {
        "Subscribers": "subscribers",
        "Total Views": "total_views",
        "Videos": "total_videos"
    }

    column = allowed.get(metric, "subscribers")

    query = text(f"""
        SELECT 
            channel_name,
            {column} AS metric_value
        FROM channels
        ORDER BY {column} DESC
        LIMIT 10
    """)

    return pd.read_sql(query, engine)