def build_custom_report(selected_sections, channel_df, video_df):

    report_data = {}

    if "Subscriber Metrics" in selected_sections:
        report_data["Subscribers"] = int(channel_df["subscriber_count"][0])
        report_data["Total Videos"] = len(video_df)
        report_data["Total Views"] = int(channel_df["total_views"][0])

    if "Top Videos" in selected_sections:
        top_videos = (
            video_df.sort_values("views", ascending=False)
            .head(5)[["title", "views"]]
            .to_dict(orient="records")
        )
        report_data["Top Videos"] = top_videos

    if "Engagement Metrics" in selected_sections:
        if "likes" in video_df.columns and "comments" in video_df.columns:
            engagement = (
                (video_df["likes"] + video_df["comments"]) / video_df["views"]
            ).mean()
            report_data["Avg Engagement Rate"] = round(engagement * 100, 2)

    if "Upload Frequency" in selected_sections:
        uploads = video_df.groupby(
            video_df["publish_date"].dt.to_period("M")
        ).size()
        report_data["Upload Frequency"] = uploads.to_dict()

    return report_data