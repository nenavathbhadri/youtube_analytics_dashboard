from sqlalchemy import text
import pandas as pd
from database.db import get_engine

engine = get_engine()


def search_videos(
    channel_id=None,
    keyword=None,
    min_views=None,
    max_views=None,
    start_date=None,
    end_date=None,
    min_engagement=None,
    duration_category=None,
    sort_by="Views",
    sort_order="DESC",
    page=1,
    page_size=20
):

    conditions = []
    params = {}

    if channel_id:
        conditions.append("v.channel_id = :channel_id")
        params["channel_id"] = channel_id

    if keyword:
        conditions.append("(v.title LIKE :keyword OR v.description LIKE :keyword)")
        params["keyword"] = f"%{keyword}%"

    if min_views is not None:
        conditions.append("vs.views >= :min_views")
        params["min_views"] = min_views

    if max_views is not None:
        conditions.append("vs.views <= :max_views")
        params["max_views"] = max_views

    if start_date:
        conditions.append("DATE(v.publish_date) >= :start_date")
        params["start_date"] = start_date

    if end_date:
        conditions.append("DATE(v.publish_date) <= :end_date")
        params["end_date"] = end_date

    if min_engagement:
        conditions.append(
            "((vs.likes + vs.comments) / NULLIF(vs.views,0)) >= :min_engagement"
        )
        params["min_engagement"] = min_engagement

    if duration_category:
        if duration_category == "Short":
            conditions.append("v.duration_seconds < 300")
        elif duration_category == "Medium":
            conditions.append("v.duration_seconds BETWEEN 300 AND 900")
        elif duration_category == "Long":
            conditions.append("v.duration_seconds > 900")

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    allowed_sort_columns = {
        "Views": "vs.views",
        "Likes": "vs.likes",
        "Publish Date": "v.publish_date",
        "Engagement": "engagement_rate"
    }

    sort_column = allowed_sort_columns.get(sort_by, "vs.views")

    offset = (page - 1) * page_size

    query = text(f"""
        SELECT 
            v.video_id,
            v.title,
            v.publish_date,
            v.duration_seconds,
            vs.views,
            vs.likes,
            vs.comments,
            ((vs.likes + vs.comments) / NULLIF(vs.views,0)) AS engagement_rate
        FROM videos v
        JOIN video_statistics vs ON v.video_id = vs.video_id
        {where_clause}
        ORDER BY {sort_column} {sort_order}
        LIMIT :limit OFFSET :offset
    """)

    params["limit"] = page_size
    params["offset"] = offset

    return pd.read_sql(query, engine, params=params)