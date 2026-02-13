from sqlalchemy.orm import sessionmaker
from database.db import get_engine
from database.models import Channel, Video, VideoStatistics
from datetime import datetime

engine = get_engine()
Session = sessionmaker(bind=engine)


def insert_channel_data(channel_df):
    session = Session()

    try:
        channel = Channel(
            channel_id=channel_df["channel_id"][0],
            channel_name=channel_df["channel_name"][0],
            description=channel_df["channel_description"][0],
            subscribers=int(channel_df["subscriber_count"][0]),
            total_videos=int(channel_df["total_videos"][0]),
            total_views=int(channel_df["total_views"][0]),
            created_date=datetime.strptime(
                channel_df["channel_creation_date"][0],
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            thumbnail_url=channel_df["channel_thumbnail_url"][0]
        )

        session.merge(channel)  # avoids duplicates
        session.commit()

        print("Channel inserted successfully!")

    except Exception as e:
        session.rollback()
        print("Error inserting channel:", e)

    finally:
        session.close()


def insert_video_data(video_df, channel_id):
    session = Session()

    try:
        for _, row in video_df.iterrows():

            video = Video(
                video_id=row["video_id"],
                channel_id=channel_id,
                title=row["title"],
                description=row["description"],
                publish_date=datetime.strptime(
                    row["publish_date"],
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                duration=row["duration"],
                thumbnail_url=row["thumbnail_url"]
            )

            stats = VideoStatistics(
                video_id=row["video_id"],
                views=int(row["views"]),
                likes=int(row["likes"]),
                comments=int(row["comments"])
            )

            session.merge(video)
            session.merge(stats)

        session.commit()
        print("Videos and statistics inserted successfully!")

    except Exception as e:
        session.rollback()
        print("Error inserting videos:", e)

    finally:
        session.close()
