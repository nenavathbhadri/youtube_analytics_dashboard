from data_processing.video_extractor import extract_full_video_data
from data_processing.channel_extractor import extract_channel_data
from metrics.metrics_calculator import run_full_transformation

channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Replace with your test channel

channel_df = extract_channel_data(channel_id)
video_df = extract_full_video_data(channel_id)

results = run_full_transformation(
    video_df,
    total_views=channel_df["total_views"][0],
    total_subscribers=channel_df["subscriber_count"][0]
)

print("Average Views:", results["avg_views"])
print("Subscriber/View Ratio:", results["subscriber_view_ratio"])
print(results["transformed_df"].head())