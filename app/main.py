import os
import sys
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from data_processing.channel_extractor import (
    extract_channel_data,
    get_channel_videos,
    get_video_statistics
)


from data_processing.channel_extractor import extract_channel_data

st.title("📊 YouTube Channel Analytics Dashboard")

channel_id = st.text_input("Enter YouTube Channel ID")

def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    return date_obj.strftime("%B %d, %Y")

def format_number(num):
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(num)


if st.button("Fetch Channel Data"):

    if not channel_id:
        st.warning("Please enter a Channel ID")
    else:
        df = extract_channel_data(channel_id)

        if df is None:
            st.error("Channel not found ❌")
        else:
            
            st.success("Channel Data Retrieved Successfully ✅")
            

            st.subheader("Channel Overview")
            st.image(df["channel_thumbnail_url"][0], width=150)

            col1, col2, col3 = st.columns(3)

            col1.metric("Subscribers", format_number(df['subscriber_count'][0]))
            col2.metric("Total Videos", format_number(df['total_videos'][0]))
            col3.metric("Total Views", format_number(df['total_views'][0]))
            st.write("### Raw Data")
            st.write(df["channel_description"][0])
            st.write("**Channel Created On:**", format_date(df["channel_creation_date"][0]))
            
           
            


            st.dataframe(df)
st.write("## 📈 Video Analytics")

videos = get_channel_videos(channel_id)
video_ids = [v["video_id"] for v in videos]

video_stats = get_video_statistics(video_ids)

import pandas as pd

video_df = pd.DataFrame(video_stats)

if not video_df.empty:

    video_df["engagement_rate"] = (
        (video_df["likes"] + video_df["comments"]) / video_df["views"]
    )

    # Merge titles
    titles_df = pd.DataFrame(videos)[["video_id", "title"]]
    video_df = video_df.merge(titles_df, on="video_id")

    # Top 10 by views
    top_videos = video_df.sort_values("views", ascending=False).head(10)

    st.write("### 🔝 Top 10 Videos by Views")
    st.dataframe(top_videos[[
        "title", "views", "likes", "comments", "engagement_rate"
    ]])

    st.write("### 📊 Views vs Likes Chart")
    st.bar_chart(top_videos.set_index("title")[["views", "likes"]])
           
