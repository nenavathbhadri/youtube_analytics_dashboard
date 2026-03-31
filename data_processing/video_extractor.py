import os
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load environment variables
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=API_KEY)


# =====================================================
# STEP 1: Get Uploads Playlist ID
# =====================================================
def get_uploads_playlist_id(channel_id):

    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )

    response = request.execute()

    if not response["items"]:
        return None

    uploads_playlist_id = response["items"][0]["contentDetails"] \
        ["relatedPlaylists"]["uploads"]

    return uploads_playlist_id


# =====================================================
# STEP 2: Get All Video IDs from Uploads Playlist
# =====================================================
def get_all_video_ids_from_playlist(playlist_id, max_videos=1000):

    video_ids = []
    next_page_token = None

    while True:

        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )

        response = request.execute()

        for item in response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        # 🔥 Stop if limit reached
        if len(video_ids) >= max_videos:
            break

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return video_ids

# =====================================================
# STEP 3: Fetch Metadata in Batches
# =====================================================
def get_video_metadata(video_ids):

    all_videos = []

    for i in range(0, len(video_ids), 50):

        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=",".join(video_ids[i:i+50])
        )

        response = request.execute()

        for item in response["items"]:

            all_videos.append({
                "video_id": item["id"],
                "title": item["snippet"].get("title", ""),
                "description": item["snippet"].get("description", ""),
                "publish_date": item["snippet"].get("publishedAt", ""),
                "duration": item["contentDetails"].get("duration", ""),
                "views": int(item["statistics"].get("viewCount", 0)),
                "likes": int(item["statistics"].get("likeCount", 0)),
                "comments": int(item["statistics"].get("commentCount", 0)),
                "thumbnail_url": item["snippet"]["thumbnails"]["high"]["url"]
            })

    return pd.DataFrame(all_videos)


# =====================================================
# STEP 4: Full Extraction Pipeline
# =====================================================
import streamlit as st
@st.cache_data(show_spinner=False)
def extract_full_video_data(channel_id):

    playlist_id = get_uploads_playlist_id(channel_id)

    if not playlist_id:
        return pd.DataFrame()

    video_ids = get_all_video_ids_from_playlist(
        playlist_id,
        max_videos=1000   # you can change to 2000 later
    )

    if not video_ids:
        return pd.DataFrame()

    video_df = get_video_metadata(video_ids)

    return video_df