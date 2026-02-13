from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    BigInteger,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# -----------------------------
# Channels Table
# -----------------------------
class Channel(Base):
    __tablename__ = "channels"

    channel_id = Column(String(100), primary_key=True)
    channel_name = Column(String(200))
    description = Column(Text)
    subscribers = Column(BigInteger)
    total_videos = Column(Integer)
    total_views = Column(BigInteger)
    created_date = Column(DateTime)
    thumbnail_url = Column(Text)

    videos = relationship("Video", back_populates="channel")


# -----------------------------
# Videos Table
# -----------------------------
class Video(Base):
    __tablename__ = "videos"

    video_id = Column(String(100), primary_key=True)
    channel_id = Column(String(100), ForeignKey("channels.channel_id"))
    title = Column(Text)
    description = Column(Text)
    publish_date = Column(DateTime)
    duration = Column(String(50))
    thumbnail_url = Column(Text)

    channel = relationship("Channel", back_populates="videos")
    statistics = relationship("VideoStatistics", back_populates="video", uselist=False)


# -----------------------------
# Video Statistics Table
# -----------------------------
class VideoStatistics(Base):
    __tablename__ = "video_statistics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(String(100), ForeignKey("videos.video_id"))
    views = Column(BigInteger, default=0)
    likes = Column(BigInteger, default=0)
    comments = Column(BigInteger, default=0)

    video = relationship("Video", back_populates="statistics")
