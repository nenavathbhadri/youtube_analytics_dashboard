import pandas as pd
import numpy as np

import re

def convert_duration_to_seconds(duration):
    if not isinstance(duration, str):
        return 0

    hours = minutes = seconds = 0

    hour_match = re.search(r'(\d+)H', duration)
    minute_match = re.search(r'(\d+)M', duration)
    second_match = re.search(r'(\d+)S', duration)

    if hour_match:
        hours = int(hour_match.group(1))
    if minute_match:
        minutes = int(minute_match.group(1))
    if second_match:
        seconds = int(second_match.group(1))

    return hours * 3600 + minutes * 60 + seconds
# ==========================================================
# 1️⃣ Engagement Rate
# ==========================================================
def calculate_engagement_rate(df):

    df["engagement_rate"] = np.where(
        df["views"] > 0,
        ((df["likes"] + df["comments"]) / df["views"]) * 100,
        0
    )

    return df


# ==========================================================
# 2️⃣ Average Views Per Video
# ==========================================================
def calculate_average_views(df):
    return df["views"].mean()


# ==========================================================
# 3️⃣ Subscriber to View Ratio
# ==========================================================
def calculate_subscriber_view_ratio(total_views, total_subscribers):

    if total_subscribers == 0:
        return 0

    return total_views / total_subscribers


# ==========================================================
# 4️⃣ Content Performance Score
# ==========================================================
def calculate_content_score(df):

    # Weighted scoring model
    df["performance_score"] = (
        (df["views"] * 0.5) +
        (df["likes"] * 0.3) +
        (df["comments"] * 0.2)
    )

    return df


# ==========================================================
# 5️⃣ Optimal Posting Time
# ==========================================================
def analyze_optimal_posting_time(df):

    df["publish_date"] = pd.to_datetime(df["publish_date"], errors="coerce")

    df["publish_hour"] = df["publish_date"].dt.hour

    optimal = (
        df.groupby("publish_hour")["views"]
        .mean()
        .reset_index()
        .sort_values("views", ascending=False)
    )

    return optimal


# ==========================================================
# 6️⃣ Monthly Trend Analysis
# ==========================================================
def monthly_trend(df):

    df["publish_date"] = pd.to_datetime(df["publish_date"], errors="coerce")

    df["month"] = df["publish_date"].dt.to_period("M")

    trend = (
        df.groupby("month")["views"]
        .sum()
        .reset_index()
    )

    trend["month"] = trend["month"].astype(str)

    return trend


# ==========================================================
# 7️⃣ Benchmark Videos vs Channel Average
# ==========================================================
def benchmark_videos(df):

    avg_views = df["views"].mean()

    df["vs_channel_avg"] = np.where(
        df["views"] >= avg_views,
        "Above Average",
        "Below Average"
    )

    return df


# ==========================================================
# 8️⃣ Prepare Full KPI Pipeline
# ==========================================================
def run_full_transformation(df, total_views, total_subscribers):
    df["duration_seconds"] = df["duration"].apply(convert_duration_to_seconds)
    df = calculate_engagement_rate(df)
    df = calculate_content_score(df)
    df = benchmark_videos(df)

    avg_views = calculate_average_views(df)
    sub_view_ratio = calculate_subscriber_view_ratio(
        total_views, total_subscribers
    )

    optimal_time = analyze_optimal_posting_time(df)
    monthly_views = monthly_trend(df)

    return {
        "transformed_df": df,
        "avg_views": avg_views,
        "subscriber_view_ratio": sub_view_ratio,
        "optimal_posting_time": optimal_time,
        "monthly_trend": monthly_views
    }
  