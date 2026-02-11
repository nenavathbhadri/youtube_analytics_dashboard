import os
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load .env from project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found. Check your .env file.")

youtube = build("youtube", "v3", developerKey=API_KEY)


def extract_channel_data(channel_id):
    try:
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )

        response = request.execute()

        if not response["items"]:
            return None

        data = response["items"][0]

        channel_info = {
            "channel_id": channel_id,
            "channel_name": data["snippet"]["title"],
            "subscriber_count": int(data["statistics"].get("subscriberCount", 0)),
            "total_videos": int(data["statistics"]["videoCount"]),
            "total_views": int(data["statistics"]["viewCount"]),
            "channel_description": data["snippet"]["description"],
            "channel_creation_date": data["snippet"]["publishedAt"],
            "channel_thumbnail_url": data["snippet"]["thumbnails"]["high"]["url"]

        }

        df = pd.DataFrame([channel_info])
        return df

    except HttpError as e:
        print("API Error:", e)
        return None


#Get All Video IDs
def get_channel_videos(channel_id, max_results=50):
    try:
        videos = []
        next_page_token = None

        while True:
            request = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                maxResults=max_results,
                order="date",
                type="video",
                pageToken=next_page_token
            )

            response = request.execute()

            for item in response["items"]:
                videos.append({
                    "video_id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "published_at": item["snippet"]["publishedAt"]
                })

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return videos

    except Exception as e:
        print("Video Fetch Error:", e)
        return []
    
#Video Statistics
def get_video_statistics(video_ids):
    try:
        stats = []

        for i in range(0, len(video_ids), 50):
            request = youtube.videos().list(
                part="statistics",
                id=",".join(video_ids[i:i+50])
            )
            response = request.execute()

            for item in response["items"]:
                stats.append({
                    "video_id": item["id"],
                    "views": int(item["statistics"].get("viewCount", 0)),
                    "likes": int(item["statistics"].get("likeCount", 0)),
                    "comments": int(item["statistics"].get("commentCount", 0))
                })

        return stats

    except Exception as e:
        print("Video Stats Error:", e)
        return []
