import os
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load environment variables
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=API_KEY)


# -----------------------------------------
# STEP 1: Get All Video IDs (Pagination)
# -----------------------------------------
def get_all_video_ids(channel_id):

    video_ids = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,
            type="video",
            pageToken=next_page_token
        )

        response = request.execute()

        for item in response["items"]:
            video_ids.append(item["id"]["videoId"])

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return video_ids


# -----------------------------------------
# STEP 2: Fetch Video Details in Batches
# -----------------------------------------
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


# -----------------------------------------
# STEP 3: Full Extraction Pipeline
# -----------------------------------------
def extract_full_video_data(channel_id):

    video_ids = get_all_video_ids(channel_id)

    if not video_ids:
        return pd.DataFrame()

    video_df = get_video_metadata(video_ids)

    return video_df
