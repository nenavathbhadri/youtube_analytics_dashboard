import os, sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "app"))

import streamlit as st
import pandas as pd
from database.search_queries import search_videos
from database.dashboard_queries import get_all_channels
from ui_theme import inject_theme

st.set_page_config(page_title="Video Explorer — TubeMetrics", layout="wide", page_icon="🔍")
inject_theme()

# ======================================================
# HEADER
# ======================================================
st.title("🔍 Video Explorer")
st.markdown('<p class="page-subtitle">Search, filter, and discover videos with advanced sorting and pagination</p>', unsafe_allow_html=True)

# =========================================
# SESSION STATE INIT
# =========================================
if "page" not in st.session_state:
    st.session_state.page = 1

if "keyword" not in st.session_state:
    st.session_state.keyword = ""

if "min_views" not in st.session_state:
    st.session_state.min_views = 0

if "max_views" not in st.session_state:
    st.session_state.max_views = 500000

if "min_engagement" not in st.session_state:
    st.session_state.min_engagement = 0.0

if "duration_category" not in st.session_state:
    st.session_state.duration_category = "All"

if "sort_by" not in st.session_state:
    st.session_state.sort_by = "Views"

if "sort_order" not in st.session_state:
    st.session_state.sort_order = "DESC"


# =========================================
# SIDEBAR FILTERS
# =========================================
st.sidebar.header("🎛 Filters")

channels_df = get_all_channels()

if channels_df.empty:
    st.warning("No channels available.")
    st.stop()

channel_options = {
    row["channel_name"]: row["channel_id"]
    for _, row in channels_df.iterrows()
}

selected_channel_name = st.sidebar.selectbox(
    "Select Channel",
    list(channel_options.keys())
)

selected_channel_id = channel_options[selected_channel_name]

# Search
st.session_state.keyword = st.sidebar.text_input(
    "Search Title or Description",
    value=st.session_state.keyword
)

# View Range
view_range = st.sidebar.slider(
    "View Count Range",
    0,
    10000000,
    (st.session_state.min_views, st.session_state.max_views)
)

st.session_state.min_views = view_range[0]
st.session_state.max_views = view_range[1]

# Engagement
st.session_state.min_engagement = st.sidebar.slider(
    "Minimum Engagement (%)",
    0.0,
    20.0,
    st.session_state.min_engagement
)

# Duration
st.session_state.duration_category = st.sidebar.selectbox(
    "Video Duration",
    ["All", "Short", "Medium", "Long"],
    index=["All", "Short", "Medium", "Long"].index(st.session_state.duration_category)
)

# Sorting
st.session_state.sort_by = st.sidebar.selectbox(
    "Sort By",
    ["Views", "Likes", "Publish Date", "Engagement"],
    index=["Views", "Likes", "Publish Date", "Engagement"].index(st.session_state.sort_by)
)

st.session_state.sort_order = st.sidebar.radio(
    "Order",
    ["DESC", "ASC"],
    index=["DESC", "ASC"].index(st.session_state.sort_order)
)

# =========================================
# CLEAR FILTER BUTTON
# =========================================
if st.sidebar.button("🗑 Clear Filters"):
    for key in [
        "keyword",
        "min_views",
        "max_views",
        "min_engagement",
        "duration_category",
        "sort_by",
        "sort_order"
    ]:
        del st.session_state[key]

    st.session_state.page = 1
    st.rerun()

# =========================================
# FETCH RESULTS
# =========================================
results = search_videos(
    channel_id=selected_channel_id,
    keyword=st.session_state.keyword if st.session_state.keyword else None,
    min_views=st.session_state.min_views,
    max_views=st.session_state.max_views,
    min_engagement=st.session_state.min_engagement / 100 if st.session_state.min_engagement else None,
    duration_category=None if st.session_state.duration_category == "All" else st.session_state.duration_category,
    sort_by=st.session_state.sort_by,
    sort_order=st.session_state.sort_order,
    page=st.session_state.page,
    page_size=20
)

# =========================================
# DISPLAY RESULTS
# =========================================
st.markdown("""
<div class="section-header">
<div class="icon">📊</div>
<h3>Filtered Results</h3>
</div>
""", unsafe_allow_html=True)

if results.empty:
    st.warning("No videos match selected filters.")
else:
    st.info(f"Results Returned: {len(results)}")

    st.dataframe(results, use_container_width=True)

    csv = results.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download CSV",
        csv,
        "filtered_videos.csv",
        "text/csv"
    )

# =========================================
# PAGINATION
# =========================================
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⬅ Previous"):
        if st.session_state.page > 1:
            st.session_state.page -= 1
            st.rerun()

with col2:
    st.markdown(
        f'<p style="text-align:center; color:#9CA3AF; font-size:0.9rem;">Page {st.session_state.page}</p>',
        unsafe_allow_html=True
    )

with col3:
    if st.button("Next ➡"):
        st.session_state.page += 1
        st.rerun()

# ======================================================
# FOOTER
# ======================================================
st.markdown('<div class="footer-text">© 2026 TubeMetrics — YouTube Analytics Platform</div>', unsafe_allow_html=True)
