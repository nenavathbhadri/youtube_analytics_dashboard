from sqlalchemy.orm import Session
from database.db import get_engine
from database.models import Channel, Video, VideoStatistics
import pandas as pd
import re
from metrics.metrics_calculator import convert_duration_to_seconds




# ---------------------------------
# Check if channel exists
# ---------------------------------
def channel_exists(session, channel_id):
    return session.query(Channel).filter_by(channel_id=channel_id).first()


# ---------------------------------
# Insert or Update Channel
# ---------------------------------
def insert_or_update_channel(session, channel_data):

    channel = channel_exists(session, channel_data["channel_id"])

    created_dt = pd.to_datetime(
        channel_data["channel_creation_date"],
        errors="coerce"
    )

    if channel:
        channel.channel_name = channel_data["channel_name"]
        channel.description = channel_data["channel_description"]
        channel.subscribers = channel_data["subscriber_count"]
        channel.total_videos = channel_data["total_videos"]
        channel.total_views = channel_data["total_views"]
        channel.created_date = created_dt
        channel.thumbnail_url = channel_data["channel_thumbnail_url"]

        return "updated"

    else:
        new_channel = Channel(
            channel_id=channel_data["channel_id"],
            channel_name=channel_data["channel_name"],
            description=channel_data["channel_description"],
            subscribers=channel_data["subscriber_count"],
            total_videos=channel_data["total_videos"],
            total_views=channel_data["total_views"],
            created_date=created_dt,
            thumbnail_url=channel_data["channel_thumbnail_url"]
        )

        session.add(new_channel)
        return "inserted"


# ---------------------------------
# Insert or Update Video Metadata
# ---------------------------------
def insert_video(session, video_data, channel_id):

    existing = session.query(Video)\
        .filter_by(video_id=video_data["video_id"])\
        .first()

    publish_dt = pd.to_datetime(
        video_data["publish_date"],
        errors="coerce"
    )

    duration_sec = convert_duration_to_seconds(
        video_data.get("duration", "")
    )

    if existing:
        existing.title = video_data["title"]
        existing.description = video_data["description"]
        existing.publish_date = publish_dt
        existing.duration = video_data["duration"]
        existing.duration_seconds = duration_sec
        existing.thumbnail_url = video_data["thumbnail_url"]

    else:
        new_video = Video(
            video_id=video_data["video_id"],
            channel_id=channel_id,
            title=video_data["title"],
            description=video_data["description"],
            publish_date=publish_dt,
            duration=video_data["duration"],
            duration_seconds=duration_sec,
            thumbnail_url=video_data["thumbnail_url"]
        )

        session.add(new_video)


# ---------------------------------
# Insert or Update Video Statistics
# ---------------------------------
def insert_video_statistics(session, stats_data):

    existing = session.query(VideoStatistics)\
        .filter_by(video_id=stats_data["video_id"])\
        .first()

    if existing:
        existing.views = int(stats_data.get("views", 0))
        existing.likes = int(stats_data.get("likes", 0))
        existing.comments = int(stats_data.get("comments", 0))
    else:
        new_stats = VideoStatistics(
            video_id=stats_data["video_id"],
            views=int(stats_data.get("views", 0)),
            likes=int(stats_data.get("likes", 0)),
            comments=int(stats_data.get("comments", 0))
        )
        session.add(new_stats)


# ---------------------------------
# Main Storage Function
# ---------------------------------
def store_channel_data(channel_df, video_df):

    engine = get_engine()

    with Session(engine) as session:

        channel_data = channel_df.iloc[0].to_dict()
        channel_status = insert_or_update_channel(session, channel_data)

        for _, row in video_df.iterrows():

            video_data = row.to_dict()

            insert_video(session, video_data, channel_data["channel_id"])

            stats_data = {
                "video_id": video_data["video_id"],
                "views": video_data.get("views", 0),
                "likes": video_data.get("likes", 0),
                "comments": video_data.get("comments", 0)
            }

            insert_video_statistics(session, stats_data)

        session.commit()

    return channel_status