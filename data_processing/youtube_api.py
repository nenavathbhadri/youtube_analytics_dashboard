import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found. Check your .env file.")

youtube = build("youtube", "v3", developerKey=API_KEY)


def resolve_to_channel_id(user_input):
    """
    Converts @handle, channel name, or channel ID into a valid channel ID.
    """

    # If already a channel ID
    if user_input.startswith("UC"):
        return user_input

    # Remove @ if present
    if user_input.startswith("@"):
        user_input = user_input[1:]

    try:
        search_response = youtube.search().list(
            part="snippet",
            q=user_input,
            type="channel",
            maxResults=1
        ).execute()

        if search_response["items"]:
            return search_response["items"][0]["snippet"]["channelId"]

        return None

    except HttpError:
        return None


def get_channel_details(user_input):
    try:
        channel_id = resolve_to_channel_id(user_input)

        if not channel_id:
            return None

        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )

        response = request.execute()

        if not response["items"]:
            return None

        data = response["items"][0]

        return {
            "Channel Name": data["snippet"]["title"],
            "Subscribers": data["statistics"].get("subscriberCount", 0),
            "Total Views": data["statistics"]["viewCount"],
            "Total Videos": data["statistics"]["videoCount"]
        }

    except HttpError as e:
        return {"error": f"HTTP Error: {e}"}
    except Exception as e:
        return {"error": str(e)}
