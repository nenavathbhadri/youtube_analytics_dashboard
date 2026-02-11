import pandas as pd

def calculate_engagement_rate(likes, comments, views):
    if views == 0:
        return 0
    return (likes + comments) / views
