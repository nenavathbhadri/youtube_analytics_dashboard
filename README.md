# 🎬 YouTube Analytics Dashboard

A full-stack **Streamlit** web application for analyzing YouTube channel performance. Fetch real-time data via the YouTube Data API, store it in MySQL, and visualize insights through interactive charts, comparisons, and exportable reports.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Channel Analysis** | Fetch subscribers, views, and video data using a Channel ID |
| 📊 **KPI Dashboard** | View key metrics — subscribers, total views, engagement rate |
| 📈 **Interactive Charts** | Line charts, bar charts, scatter plots, pie charts, heatmaps, funnels |
| ⚔ **Channel Comparison** | Compare up to 3 channels side-by-side with leaderboards |
| 🔍 **Video Explorer** | Search, filter, and sort videos with pagination |
| 📄 **Reports Hub** | Export data as CSV, Excel, or PDF; save custom report templates |
| 🌙 **Dark / Light Theme** | Toggle between dark and light mode from any page |
| 💾 **MySQL Storage** | Persistent storage of channel and video data |
| ⚡ **Performance Metrics** | Track fetch, transform, and DB insert times |

---

## 📁 Project Structure

```
youtube_analytics_dashboard/
├── app/
│   ├── main.py                          # Home page — analyze channels
│   ├── ui_theme.py                      # Shared dark/light theme CSS
│   └── pages/
│       ├── 1_📊_Channel_Insights.py     # Channel KPIs & comparison
│       ├── 2_📈_Performance_Charts.py   # Views, top videos, uploads
│       ├── 3_🔬_Deep_Analytics.py       # Heatmaps, funnels, histograms
│       ├── 4_⚔_Channel_Comparison.py    # Head-to-head comparison
│       ├── 5_🔍_Video_Explorer.py       # Search & filter engine
│       └── 6_📄_Reports_Hub.py          # Export & report templates
├── data_processing/
│   ├── channel_extractor.py             # YouTube API — channel data
│   ├── video_extractor.py               # YouTube API — video data
│   └── youtube_api.py                   # API client setup
├── database/
│   ├── db.py                            # MySQL connection
│   ├── models.py                        # Table definitions
│   ├── data_insertion.py                # Insert channel/video data
│   ├── analytics_queries.py             # Analytics SQL queries
│   ├── dashboard_queries.py             # Dashboard SQL queries
│   ├── comparison_queries.py            # Comparison SQL queries
│   └── search_queries.py               # Search & filter queries
├── metrics/
│   └── metrics_calculator.py            # KPI calculations & transformations
├── reports/
│   ├── export_utils.py                  # CSV & Excel export
│   ├── pdf_report.py                    # PDF report generation
│   ├── report_builder.py               # Custom report builder
│   └── template_manager.py             # Save/load report templates
├── credentials/                         # API credentials (gitignored)
├── requirements.txt                     # Python dependencies
├── test_metrics.py                      # Unit tests
└── .env                                 # Environment variables
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit, Plotly |
| **Backend** | Python |
| **Database** | MySQL (via PyMySQL + SQLAlchemy) |
| **API** | YouTube Data API v3 |
| **Reports** | ReportLab (PDF), XlsxWriter (Excel) |
| **Styling** | Custom CSS (Inter font, glassmorphism, dark/light themes) |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+**
- **MySQL** server running locally
- **YouTube Data API key** ([Get one here](https://console.cloud.google.com/apis/credentials))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nenavathbhadri/youtube_analytics_dashboard.git
   cd youtube_analytics_dashboard
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   # source venv/bin/activate   # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:
   ```env
   YOUTUBE_API_KEY=your_api_key_here
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=youtube_analytics
   ```

5. **Set up the database**

   Create a MySQL database named `youtube_analytics` and run the table creation script.

6. **Run the application**
   ```bash
   streamlit run app/main.py
   ```

   Open `http://localhost:8501` in your browser.

---

## 📖 How to Use

1. Enter a **YouTube Channel ID** (starts with `UC`, 24 characters) on the Home page
2. Click **Analyze Channel** to fetch and store data
3. Navigate through the sidebar pages:
   - **Channel Insights** — KPIs with cross-channel comparison
   - **Performance Charts** — Views over time, top videos, upload distribution
   - **Deep Analytics** — Heatmaps, engagement funnels, metric selectors
   - **Channel Comparison** — Compare up to 3 channels with leaderboards
   - **Video Explorer** — Advanced search with filters and sorting
   - **Reports Hub** — Export as CSV/Excel/PDF, save report templates
4. Toggle 🌙/☀️ at the top-right of any page for **dark/light mode**

---

## 🧪 Running Tests

```bash
python -m pytest test_metrics.py
```

---

## 📄 License

This project is for educational and personal use.

---

<p align="center">
  Built with ❤️ using Streamlit & Python
</p>
