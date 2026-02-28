import streamlit as st
import pandas as pd
from database.dashboard_queries import (
    get_all_channels,
    get_channel_kpis
)

st.set_page_config(page_title="Channel Overview", layout="wide")

st.title("📊 Channel Overview Dashboard")

# ======================================================
# SIDEBAR - Channel Selection
# ======================================================

st.sidebar.header("🔎 Select Channel")

channels_df = get_all_channels()

if channels_df.empty:
    st.warning("No channels found in database.")
    st.stop()

channel_options = {
    row["channel_name"]: row["channel_id"]
    for _, row in channels_df.iterrows()
}

selected_channel_name = st.sidebar.selectbox(
    "Choose Channel",
    list(channel_options.keys())
)

selected_channel_id = channel_options[selected_channel_name]

# ------------------------------------------------------
# Date Range Filter (UI Ready for Task 12 Integration)
# ------------------------------------------------------

st.sidebar.subheader("📅 Date Range Filter")

date_range = st.sidebar.date_input(
    "Select Date Range",
    []
)

# ------------------------------------------------------
# Channel Comparison
# ------------------------------------------------------

compare_channels = st.sidebar.multiselect(
    "Compare With Other Channels",
    list(channel_options.keys())
)

# ======================================================
# MAIN KPI SECTION
# ======================================================

kpi_df = get_channel_kpis(selected_channel_id)

if kpi_df.empty:
    st.warning("No KPI data available.")
    st.stop()

data = kpi_df.iloc[0]

st.subheader(f"Overview for {selected_channel_name}")
st.markdown("### 📌 Key Performance Indicators(KPI)")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Subscribers",
    f"{int(data['subscribers']):,}"
)

col2.metric(
    "Total Videos",
    f"{int(data['total_videos']):,}"
)

col3.metric(
    "Total Views",
    f"{int(data['total_views']):,}"
)

col4.metric(
    "Avg Engagement %",
    round(data["avg_engagement"], 2)
)

st.markdown("---")

# ======================================================
# CHANNEL COMPARISON SECTION
# ======================================================

if compare_channels:

    st.subheader("📈 Channel Comparison")

    comparison_data = []

    for ch in compare_channels:
        ch_id = channel_options[ch]
        df = get_channel_kpis(ch_id)
        if not df.empty:
            comparison_data.append(df)

    if comparison_data:
        compare_df = pd.concat(comparison_data).reset_index(drop=True)

        # Professional formatting
        compare_df["subscribers"] = compare_df["subscribers"].apply(lambda x: f"{int(x):,}")
        compare_df["total_videos"] = compare_df["total_videos"].apply(lambda x: f"{int(x):,}")
        compare_df["total_views"] = compare_df["total_views"].apply(lambda x: f"{int(x):,}")
        compare_df["avg_engagement"] = compare_df["avg_engagement"].round(2)

        st.dataframe(
            compare_df,
            use_container_width=True
        )