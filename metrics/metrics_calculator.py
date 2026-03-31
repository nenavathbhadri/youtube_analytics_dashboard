import pandas as pd
import numpy as np
import re
import streamlit as st

# ==========================================================
# Convert Duration
# ==========================================================
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
# FULL KPI PIPELINE (Optimized + Cached)
# ==========================================================
@st.cache_data(show_spinner=False)
def run_full_transformation(df, total_views, total_subscribers):

    df = df.copy()

    # Avoid division by zero
    df["views"] = df["views"].replace(0, 1)

    # Duration conversion
    df["duration_seconds"] = df["duration"].apply(convert_duration_to_seconds)

    # Vectorized engagement rate
    df["engagement_rate"] = (
        (df["likes"] + df["comments"]) / df["views"]
    ) * 100

    # Content score (vectorized)
    df["performance_score"] = (
        (df["views"] * 0.5) +
        (df["likes"] * 0.3) +
        (df["comments"] * 0.2)
    )

    # Average views (store once)
    avg_views = df["views"].mean()

    # Benchmark
    df["vs_channel_avg"] = np.where(
        df["views"] >= avg_views,
        "Above Average",
        "Below Average"
    )

    # Subscriber/View ratio
    sub_view_ratio = total_subscribers / total_views if total_views else 0

    # Date processing (vectorized)
    df["publish_date"] = pd.to_datetime(df["publish_date"], errors="coerce")

    # Monthly trend
    df["month"] = df["publish_date"].dt.to_period("M")
    monthly_views = df.groupby("month")["views"].sum().reset_index()
    monthly_views["month"] = monthly_views["month"].astype(str)

    # Optimal posting time
    df["publish_hour"] = df["publish_date"].dt.hour
    optimal_time = df.groupby("publish_hour")["views"].mean().reset_index()

    return {
        "transformed_df": df,
        "avg_views": avg_views,
        "subscriber_view_ratio": sub_view_ratio,
        "optimal_posting_time": optimal_time,
        "monthly_trend": monthly_views
    }