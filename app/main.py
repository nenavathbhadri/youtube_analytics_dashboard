import os
import sys

# -----------------------------
# Fix Python Path (IMPORTANT)
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv(os.path.join(BASE_DIR, ".env"))

# -----------------------------
# Import Project Modules
# -----------------------------
from data_processing.channel_extractor import (
    extract_channel_data,
    get_channel_videos,
    get_video_statistics
)

from data_processing.video_extractor import extract_full_video_data
from database.insert_data import insert_channel_data, insert_video_data




# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="YouTube Analytics Dashboard",
    layout="wide"
)

# -----------------------------
# Title & Description
# -----------------------------
st.title("📊 YouTube Channel Performance & Engagement Analytics Dashboard")

st.markdown("""
Analyze a YouTube channel and extract:

- Channel level statistics  
- Video level performance  
- Engagement metrics  
- Full video metadata  
- Top performing content  

Enter a valid YouTube Channel ID below to begin.
""")

# -----------------------------
# Input Field
# -----------------------------
channel_id = st.text_input(
    "Enter YouTube Channel ID",
    placeholder="Example: UC_x5XG1OV2P6uZZ5FSM9Ttw"
)

# -----------------------------
# Helper Functions
# -----------------------------
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

# -----------------------------
# Button Action
# -----------------------------
if st.button("🚀 Fetch Channel Data"):

    if not channel_id:
        st.error("Please enter a Channel ID.")
    elif not channel_id.startswith("UC"):
        st.error("Invalid Channel ID format.")
    else:

        with st.spinner("Fetching data from YouTube API..."):

            df = extract_channel_data(channel_id)

            if df is None:
                st.error("Channel not found ❌")
            else:

                st.success("Channel Data Retrieved Successfully ✅")

                # =============================
                # CHANNEL OVERVIEW
                # =============================
                st.markdown("---")
                st.subheader("📌 Channel Overview")

                st.image(df["channel_thumbnail_url"][0], width=150)

                col1, col2, col3 = st.columns(3)

                col1.metric("Subscribers", format_number(df['subscriber_count'][0]))
                col2.metric("Total Videos", format_number(df['total_videos'][0]))
                col3.metric("Total Views", format_number(df['total_views'][0]))

                st.write("### Channel Description")
                st.write(df["channel_description"][0])

                st.write(
                    "**Channel Created On:**",
                    format_date(df["channel_creation_date"][0])
                )

                # =============================
                # FULL VIDEO METADATA
                # =============================
                st.markdown("---")
                st.subheader("📂 Full Video Metadata")

                video_df_full = extract_full_video_data(channel_id)

                if not video_df_full.empty:
                    st.write("Total Videos Fetched:", len(video_df_full))
                    st.dataframe(video_df_full.head(20))
                else:
                    st.warning("No video metadata available.")

                # =============================
                # VIDEO ANALYTICS
                # =============================
                st.markdown("---")
                st.subheader("📈 Video Analytics")

                videos = get_channel_videos(channel_id)
                video_ids = [v["video_id"] for v in videos]

                video_stats = get_video_statistics(video_ids)

                video_df = pd.DataFrame(video_stats)

                if not video_df.empty:

                    video_df["engagement_rate"] = (
                        (video_df["likes"] + video_df["comments"])
                        / video_df["views"]
                    )

                    titles_df = pd.DataFrame(videos)[["video_id", "title"]]
                    video_df = video_df.merge(titles_df, on="video_id")

                    top_videos = (
                        video_df.sort_values("views", ascending=False)
                        .head(10)
                    )

                    st.write("### 🔝 Top 10 Videos by Views")
                    st.dataframe(top_videos[[
                        "title",
                        "views",
                        "likes",
                        "comments",
                        "engagement_rate"
                    ]])

                    st.write("### 📊 Views vs Likes Comparison")
                    st.bar_chart(
                        top_videos.set_index("title")[["views", "likes"]]
                    )

                else:
                    st.warning("No video statistics available.")
insert_channel_data(df)
insert_video_data(video_df_full, channel_id)

st.success("Data Stored in Database Successfully 💾")