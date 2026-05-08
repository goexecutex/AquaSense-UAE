"""
AquaSense UAE: AI-Powered Water Impact Dashboard for Sustainable Campuses
Built for UAE Sustainability Impact Competition
Award-Recognized Project: AI & Big Data for Climate Action
RAK EISC 2026 – Third Place | RAK Department of Knowledge Recognition | AED 1,000 Cash Prize
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from datetime import datetime

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="AquaSense UAE | Smart Water Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# GLOBAL CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root & Reset ── */
:root {
    --primary:   #0A7EA4;
    --accent:    #00C5A1;
    --deep:      #003D52;
    --light-bg:  #F0F8FC;
    --card-bg:   #FFFFFF;
    --text-main: #1A2E35;
    --text-muted:#5A7A85;
    --danger:    #E84855;
    --warn:      #F5A623;
    --success:   #00C5A1;
    --border:    #D0E8F0;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text-main);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--deep) 0%, #005670 100%) !important;
    border-right: none;
}
[data-testid="stSidebar"] * {
    color: #E0F4FB !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.92rem;
    padding: 6px 0;
}

/* ── Main background ── */
.main .block-container {
    background: var(--light-bg);
    padding-top: 1.5rem;
    max-width: 1300px;
}

/* ── Headers ── */
h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
}

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, var(--deep) 0%, var(--primary) 60%, var(--accent) 100%);
    border-radius: 20px;
    padding: 48px 48px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 280px; height: 280px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: rgba(0,197,161,0.12);
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    color: #FFFFFF;
    margin: 0 0 8px;
    line-height: 1.15;
    position: relative; z-index: 1;
}
.hero-sub {
    font-size: 1.05rem;
    color: rgba(255,255,255,0.82);
    margin: 0 0 20px;
    position: relative; z-index: 1;
}
.badge-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    position: relative; z-index: 1;
}
.badge {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 30px;
    padding: 5px 14px;
    font-size: 0.78rem;
    color: #FFFFFF;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    backdrop-filter: blur(8px);
}

/* ── Section Title ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.45rem;
    font-weight: 700;
    color: var(--deep);
    margin: 28px 0 18px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title span.dot {
    display: inline-block;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--accent);
}

/* ── Metric Cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}
.metric-card {
    background: var(--card-bg);
    border-radius: 16px;
    padding: 22px 24px;
    border: 1px solid var(--border);
    box-shadow: 0 2px 12px rgba(10,126,164,0.07);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 28px rgba(10,126,164,0.13);
}
.metric-icon {
    font-size: 1.7rem;
    margin-bottom: 8px;
}
.metric-label {
    font-size: 0.77rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 4px;
    font-weight: 500;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--deep);
    line-height: 1;
}
.metric-delta {
    font-size: 0.8rem;
    margin-top: 6px;
    color: var(--text-muted);
}
.metric-card.accent-green { border-left: 4px solid var(--accent); }
.metric-card.accent-blue  { border-left: 4px solid var(--primary); }
.metric-card.accent-red   { border-left: 4px solid var(--danger); }
.metric-card.accent-warn  { border-left: 4px solid var(--warn); }
.metric-card.accent-deep  { border-left: 4px solid var(--deep); }

/* ── Info / Alert Boxes ── */
.info-box {
    background: #E8F7FF;
    border-left: 4px solid var(--primary);
    border-radius: 10px;
    padding: 16px 20px;
    margin: 16px 0;
    font-size: 0.93rem;
    color: var(--deep);
}
.warn-box {
    background: #FFF8E8;
    border-left: 4px solid var(--warn);
    border-radius: 10px;
    padding: 16px 20px;
    margin: 16px 0;
    font-size: 0.93rem;
}
.success-box {
    background: #E6FBF6;
    border-left: 4px solid var(--accent);
    border-radius: 10px;
    padding: 16px 20px;
    margin: 16px 0;
    font-size: 0.93rem;
}
.danger-box {
    background: #FDECEA;
    border-left: 4px solid var(--danger);
    border-radius: 10px;
    padding: 16px 20px;
    margin: 16px 0;
    font-size: 0.93rem;
}

/* ── Chart Container ── */
.chart-card {
    background: var(--card-bg);
    border-radius: 16px;
    padding: 24px;
    border: 1px solid var(--border);
    box-shadow: 0 2px 12px rgba(10,126,164,0.06);
    margin-bottom: 20px;
}
.chart-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--deep);
    margin-bottom: 16px;
}

/* ── Table ── */
.styled-table { border-collapse: collapse; width: 100%; font-size: 0.88rem; }
.styled-table th {
    background: var(--deep);
    color: #fff;
    padding: 10px 14px;
    text-align: left;
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
}
.styled-table td { padding: 9px 14px; border-bottom: 1px solid var(--border); }
.styled-table tr:hover td { background: #F0F8FC; }

/* ── Recommendation Cards ── */
.rec-card {
    background: var(--card-bg);
    border-radius: 14px;
    padding: 20px 24px;
    border: 1px solid var(--border);
    margin-bottom: 14px;
    display: flex;
    gap: 16px;
    align-items: flex-start;
    box-shadow: 0 2px 10px rgba(10,126,164,0.05);
}
.rec-icon-box {
    width: 44px; height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--primary), var(--accent));
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
}
.rec-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.98rem;
    font-weight: 700;
    color: var(--deep);
    margin-bottom: 4px;
}
.rec-body { font-size: 0.87rem; color: var(--text-muted); line-height: 1.55; }
.rec-saving {
    display: inline-block;
    background: #E6FBF6;
    color: #007A60;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.76rem;
    font-weight: 600;
    margin-top: 6px;
}

/* ── Report Card ── */
.report-card {
    background: linear-gradient(135deg, var(--deep), #005670);
    border-radius: 20px;
    padding: 36px 40px;
    color: white;
    margin-bottom: 20px;
}
.report-stat {
    text-align: center;
    padding: 16px;
}
.report-stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: var(--accent);
}
.report-stat-label { font-size: 0.8rem; color: rgba(255,255,255,0.7); margin-top: 4px; }

/* ── Divider ── */
.section-divider {
    height: 2px;
    background: linear-gradient(90deg, var(--accent), transparent);
    border: none;
    margin: 30px 0;
    border-radius: 2px;
}

/* ── Upload Area ── */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--primary) !important;
    border-radius: 14px !important;
    background: #F0F8FC !important;
}

/* ── Progress bar ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--primary), var(--accent)) !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F0F8FC; }
::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 3px; }

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 24px;
    color: var(--text-muted);
    font-size: 0.8rem;
    border-top: 1px solid var(--border);
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# PLOTLY THEME
# ──────────────────────────────────────────────
PLOTLY_COLORS = ["#0A7EA4", "#00C5A1", "#003D52", "#F5A623", "#E84855",
                 "#6EC6E6", "#4BC8A8", "#2D6E8A", "#FFD166", "#EF8354"]
PLOTLY_LAYOUT = dict(
    font_family="DM Sans",
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=20, r=20, t=40, b=20),
    colorway=PLOTLY_COLORS,
    title_font=dict(family="Syne", size=16, color="#003D52"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
)

def apply_theme(fig):
    fig.update_layout(**PLOTLY_LAYOUT)
    fig.update_xaxes(showgrid=True, gridcolor="#E8F3F8", linecolor="#D0E8F0")
    fig.update_yaxes(showgrid=True, gridcolor="#E8F3F8", linecolor="#D0E8F0")
    return fig

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
def fmt_num(n, decimals=0):
    if n >= 1_000_000:
        return f"{n/1_000_000:.2f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return f"{n:,.{decimals}f}"

def metric_card(icon, label, value, delta="", color_class="accent-blue"):
    return f"""
    <div class="metric-card {color_class}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {"<div class='metric-delta'>" + delta + "</div>" if delta else ""}
    </div>"""

def section_title(icon, text):
    st.markdown(f"""
    <div class="section-title">
        {icon} <span class="dot"></span> {text}
    </div>""", unsafe_allow_html=True)

def divider():
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# DATA LOADING
# ──────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(file_bytes, file_name):
    if file_name.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(file_bytes))
    else:
        df = pd.read_excel(io.BytesIO(file_bytes))
    return df

def process_data(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date", "Water_Usage_Liters", "Cost_AED"])
    df["Water_Usage_Liters"] = pd.to_numeric(df["Water_Usage_Liters"], errors="coerce")
    df["Cost_AED"] = pd.to_numeric(df["Cost_AED"], errors="coerce")
    df = df.dropna(subset=["Water_Usage_Liters", "Cost_AED"])
    df = df.sort_values("Date").reset_index(drop=True)

    # Analytics
    avg   = df["Water_Usage_Liters"].mean()
    std   = df["Water_Usage_Liters"].std()
    thresh = avg + 2 * std

    df["Is_Abnormal"] = df["Water_Usage_Liters"] > thresh
    df["Wasted_Liters"] = np.where(df["Is_Abnormal"],
                                   df["Water_Usage_Liters"] - avg, 0)
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Month_Name"] = df["Date"].dt.strftime("%b %Y")
    df["Day_of_Week"] = df["Date"].dt.day_name()
    return df, avg, std, thresh

# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px;'>
        <div style='font-size:2.8rem;'>💧</div>
        <div style='font-family:Syne,sans-serif; font-size:1.15rem; font-weight:800;
                    color:#E0F4FB; line-height:1.2;'>AquaSense UAE</div>
        <div style='font-size:0.72rem; color:rgba(224,244,251,0.6);
                    margin-top:4px; letter-spacing:1px;'>SMART WATER DASHBOARD</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.15); margin:10px 0 18px;'>",
                unsafe_allow_html=True)

    pages = [
        "🏠  Home / Project Overview",
        "📂  Upload Water Data",
        "🔍  Data Quality Check",
        "📊  Water Usage Dashboard",
        "📅  Monthly Water Summary",
        "🏢  Building-wise Comparison",
        "🚨  Abnormal Usage / Leak Detection",
        "🌍  Impact Calculator",
        "🤖  AI-Style Recommendations",
        "📋  Final Impact Report",
    ]
    selected = st.radio("Navigation", pages, label_visibility="collapsed")

    st.markdown("<hr style='border-color:rgba(255,255,255,0.15); margin:18px 0 12px;'>",
                unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem; color:rgba(224,244,251,0.5);
                text-align:center; padding-bottom:10px; line-height:1.7;'>
        🏆 RAK EISC 2026 · 3rd Place<br>
        🎖️ RAK Dept. of Knowledge Award<br>
        💰 AED 1,000 Cash Prize
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────
if "df_raw" not in st.session_state:
    st.session_state.df_raw = None
if "df" not in st.session_state:
    st.session_state.df = None
if "stats" not in st.session_state:
    st.session_state.stats = {}

# ──────────────────────────────────────────────
# GUARD: require data for all analysis pages
# ──────────────────────────────────────────────
def require_data():
    if st.session_state.df is None:
        st.markdown("""
        <div style='text-align:center; padding:80px 20px;'>
            <div style='font-size:3.5rem; margin-bottom:16px;'>📂</div>
            <div style='font-family:Syne,sans-serif; font-size:1.3rem;
                        font-weight:700; color:#003D52;'>No Data Uploaded Yet</div>
            <div style='font-size:0.92rem; color:#5A7A85; margin-top:8px;'>
                Please upload your water consumption file in the
                <strong>Upload Water Data</strong> section first.
            </div>
        </div>""", unsafe_allow_html=True)
        return False
    return True

# ──────────────────────────────────────────────
# PAGE: HOME
# ──────────────────────────────────────────────
if selected.startswith("🏠"):
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">💧 AquaSense UAE</div>
        <div class="hero-sub">AI-Powered Water Impact Dashboard for Sustainable Campuses</div>
        <div class="badge-row">
            <span class="badge">🏆 RAK EISC 2026 — 3rd Place</span>
            <span class="badge">🎖️ RAK Dept. of Knowledge Recognition</span>
            <span class="badge">💰 AED 1,000 Cash Prize</span>
            <span class="badge">🌱 UAE Sustainability Initiative</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        section_title("📌", "About This Project")
        st.markdown("""
        <div class="info-box">
        <strong>AquaSense UAE</strong> is a smart water management system designed to help 
        UAE universities and buildings identify water waste, detect potential leaks, and 
        take data-driven action toward water conservation — a critical need in one of the 
        world's most water-scarce regions.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="success-box">
        🌍 <strong>Why Water Matters in the UAE</strong><br>
        The UAE has one of the highest per-capita water consumption rates globally. 
        With desalination accounting for over 90% of freshwater supply, every litre 
        saved directly reduces carbon emissions and national energy costs.
        </div>
        """, unsafe_allow_html=True)

        section_title("⚙️", "What This Dashboard Does")
        features = [
            ("📂", "Upload & validate campus water consumption data (CSV or Excel)"),
            ("🔍", "Run automatic data quality checks and flag missing entries"),
            ("📊", "Visualise daily, monthly, and building-level water trends"),
            ("🚨", "Detect abnormal usage spikes that may indicate leaks or waste"),
            ("🌍", "Calculate real environmental & financial impact of water waste"),
            ("🤖", "Generate AI-style, building-specific water-saving recommendations"),
            ("📋", "Produce a final competition-ready impact report summary"),
        ]
        for icon, text in features:
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:12px; padding:8px 0;
                        border-bottom:1px solid #D0E8F0;'>
                <span style='font-size:1.1rem;'>{icon}</span>
                <span style='font-size:0.9rem; color:#1A2E35;'>{text}</span>
            </div>""", unsafe_allow_html=True)

    with col2:
        section_title("🏆", "Project Awards")
        awards = [
            ("🥉", "3rd Place", "RAK EISC 2026 Competition", "#F5A623"),
            ("🎖️", "Special Recognition", "RAK Department of Knowledge", "#0A7EA4"),
            ("💰", "AED 1,000", "Cash Prize Awarded", "#00C5A1"),
            ("🌱", "UAE SDG Aligned", "Sustainable Development Goal 6", "#003D52"),
        ]
        for icon, title, sub, color in awards:
            st.markdown(f"""
            <div class="metric-card" style='border-left:4px solid {color}; margin-bottom:12px;'>
                <div style='font-size:1.5rem;'>{icon}</div>
                <div style='font-family:Syne,sans-serif; font-size:1.05rem;
                            font-weight:700; color:#003D52;'>{title}</div>
                <div style='font-size:0.82rem; color:#5A7A85; margin-top:2px;'>{sub}</div>
            </div>""", unsafe_allow_html=True)

        section_title("📖", "How to Use")
        steps = [
            ("1", "Go to Upload Water Data"),
            ("2", "Upload your CSV or Excel file"),
            ("3", "Navigate through each section"),
            ("4", "Download the Final Report"),
        ]
        for num, step in steps:
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:12px; padding:9px 14px;
                        background:#F0F8FC; border-radius:10px; margin-bottom:8px;'>
                <div style='width:26px; height:26px; border-radius:50%;
                            background:linear-gradient(135deg,#0A7EA4,#00C5A1);
                            color:white; font-family:Syne,sans-serif; font-weight:700;
                            font-size:0.8rem; display:flex; align-items:center;
                            justify-content:center; flex-shrink:0;'>{num}</div>
                <span style='font-size:0.88rem;'>{step}</span>
            </div>""", unsafe_allow_html=True)

    # Required columns info
    divider()
    section_title("📋", "Required Data Columns")
    cols_info = [
        ("Date", "Date of water reading (any standard date format)", "📅"),
        ("Building", "Name or ID of the building / block", "🏢"),
        ("Water_Usage_Liters", "Water consumed that day in litres", "💧"),
        ("Cost_AED", "Cost in UAE Dirhams for that reading", "💰"),
    ]
    c1, c2, c3, c4 = st.columns(4)
    containers = [c1, c2, c3, c4]
    for i, (col, desc, icon) in enumerate(cols_info):
        with containers[i]:
            st.markdown(f"""
            <div class="metric-card accent-blue">
                <div style='font-size:1.4rem;'>{icon}</div>
                <div style='font-family:Syne,sans-serif; font-size:0.95rem;
                            font-weight:700; color:#003D52;'>{col}</div>
                <div style='font-size:0.78rem; color:#5A7A85; margin-top:4px;'>{desc}</div>
            </div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# PAGE: UPLOAD
# ──────────────────────────────────────────────
elif selected.startswith("📂"):
    st.markdown("""
    <div class="hero-banner" style='padding:36px 40px;'>
        <div class="hero-title" style='font-size:1.9rem;'>📂 Upload Water Data</div>
        <div class="hero-sub">Upload your campus water consumption file to begin analysis</div>
    </div>
    """, unsafe_allow_html=True)

    col_up, col_info = st.columns([2, 1], gap="large")

    with col_up:
        section_title("⬆️", "Upload Your File")
        uploaded = st.file_uploader(
            "Drag & drop or browse your file",
            type=["csv", "xlsx", "xls"],
            help="Supported formats: CSV, Excel (.xlsx, .xls)"
        )

        if uploaded:
            with st.spinner("🔄 Reading your file…"):
                raw = load_data(uploaded.read(), uploaded.name)
                st.session_state.df_raw = raw

            st.markdown('<div class="success-box">✅ File loaded successfully! Navigate to <strong>Data Quality Check</strong> or any analysis section.</div>',
                        unsafe_allow_html=True)

            REQUIRED = {"Date", "Building", "Water_Usage_Liters", "Cost_AED"}
            missing_cols = REQUIRED - set(raw.columns)
            if missing_cols:
                st.markdown(f'<div class="danger-box">⚠️ Missing required columns: <strong>{", ".join(missing_cols)}</strong></div>',
                            unsafe_allow_html=True)
            else:
                df_proc, avg, std, thresh = process_data(raw)
                st.session_state.df = df_proc
                st.session_state.stats = {
                    "avg": avg, "std": std, "thresh": thresh,
                    "total_usage": df_proc["Water_Usage_Liters"].sum(),
                    "total_cost":  df_proc["Cost_AED"].sum(),
                    "total_waste": df_proc["Wasted_Liters"].sum(),
                    "n_abnormal":  df_proc["Is_Abnormal"].sum(),
                    "n_rows":      len(df_proc),
                }

            st.markdown("#### 👀 Data Preview")
            st.dataframe(raw.head(10), use_container_width=True, height=280)

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown(metric_card("📄", "Total Rows", f"{len(raw):,}", "", "accent-blue"), unsafe_allow_html=True)
            with col_b:
                st.markdown(metric_card("📐", "Columns", str(len(raw.columns)), "", "accent-green"), unsafe_allow_html=True)
            with col_c:
                size_kb = uploaded.size / 1024
                st.markdown(metric_card("💾", "File Size", f"{size_kb:.1f} KB", "", "accent-deep"), unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style='text-align:center; padding:60px 20px; color:#5A7A85;'>
                <div style='font-size:3.5rem; margin-bottom:16px;'>📤</div>
                <div style='font-family:Syne,sans-serif; font-size:1.1rem;
                            font-weight:600; color:#003D52;'>No file uploaded yet</div>
                <div style='font-size:0.88rem; margin-top:8px;'>
                    Upload a CSV or Excel file to start the analysis
                </div>
            </div>""", unsafe_allow_html=True)

    with col_info:
        section_title("📋", "File Requirements")
        st.markdown("""
        <div class="info-box">
        <strong>Required Columns</strong><br><br>
        ✅ <code>Date</code> — Any date format<br>
        ✅ <code>Building</code> — Name / Block ID<br>
        ✅ <code>Water_Usage_Liters</code> — Numeric<br>
        ✅ <code>Cost_AED</code> — Numeric<br><br>
        <strong>Supported Formats</strong><br><br>
        📄 <code>.csv</code> — Comma-separated<br>
        📊 <code>.xlsx</code> — Excel 2007+<br>
        📊 <code>.xls</code> — Excel Legacy
        </div>
        """, unsafe_allow_html=True)

        section_title("💡", "Sample Row")
        sample = pd.DataFrame([
            {"Date": "2024-01-15", "Building": "Block A",
             "Water_Usage_Liters": 3200, "Cost_AED": 16.5},
            {"Date": "2024-01-16", "Building": "Block B",
             "Water_Usage_Liters": 4100, "Cost_AED": 21.2},
        ])
        st.dataframe(sample, use_container_width=True, hide_index=True)

# ──────────────────────────────────────────────
# PAGE: DATA QUALITY CHECK
# ──────────────────────────────────────────────
elif selected.startswith("🔍"):
    st.markdown("""
    <div class="hero-banner" style='padding:36px 40px;'>
        <div class="hero-title" style='font-size:1.9rem;'>🔍 Data Quality Check</div>
        <div class="hero-sub">Validate your dataset before running analysis</div>
    </div>""", unsafe_allow_html=True)

    if not require_data():
        st.stop()

    df = st.session_state.df
    raw = st.session_state.df_raw

    section_title("📊", "Overview Statistics")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card("📄", "Total Records", f"{len(raw):,}", "", "accent-blue"), unsafe_allow_html=True)
    with c2:
        null_count = raw.isnull().sum().sum()
        st.markdown(metric_card("🚫", "Missing Values", str(null_count),
                                "Clean ✅" if null_count == 0 else "Needs attention ⚠️",
                                "accent-green" if null_count == 0 else "accent-red"),
                    unsafe_allow_html=True)
    with c3:
        dup_count = raw.duplicated().sum()
        st.markdown(metric_card("🔁", "Duplicate Rows", str(dup_count),
                                "None found ✅" if dup_count == 0 else "Found duplicates ⚠️",
                                "accent-green" if dup_count == 0 else "accent-warn"),
                    unsafe_allow_html=True)
    with c4:
        date_range = (df["Date"].max() - df["Date"].min()).days
        st.markdown(metric_card("📅", "Date Range", f"{date_range} days",
                                f"{df['Date'].min().date()} → {df['Date'].max().date()}",
                                "accent-deep"), unsafe_allow_html=True)

    divider()

    col1, col2 = st.columns(2)
    with col1:
        section_title("📋", "Column Health Check")
        REQUIRED = ["Date", "Building", "Water_Usage_Liters", "Cost_AED"]
        for col in REQUIRED:
            if col in raw.columns:
                null_n = raw[col].isnull().sum()
                status = "✅ OK" if null_n == 0 else f"⚠️ {null_n} missing"
                color  = "#E6FBF6" if null_n == 0 else "#FFF8E8"
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; align-items:center;
                            padding:10px 14px; background:{color}; border-radius:10px;
                            margin-bottom:8px; font-size:0.88rem;'>
                    <span style='font-weight:600;'>{col}</span>
                    <span>{status}</span>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; align-items:center;
                            padding:10px 14px; background:#FDECEA; border-radius:10px;
                            margin-bottom:8px; font-size:0.88rem;'>
                    <span style='font-weight:600;'>{col}</span>
                    <span>❌ Column missing</span>
                </div>""", unsafe_allow_html=True)

    with col2:
        section_title("📈", "Data Statistics Summary")
        stats_df = df[["Water_Usage_Liters", "Cost_AED"]].describe().round(2)
        st.dataframe(stats_df, use_container_width=True)

    divider()
    section_title("🏢", "Records Per Building")
    building_counts = df.groupby("Building").size().reset_index(name="Records")
    fig = px.bar(building_counts, x="Building", y="Records",
                 color="Records", color_continuous_scale=["#6EC6E6", "#003D52"],
                 title="Number of Data Records per Building")
    apply_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

    section_title("🗓️", "Full Cleaned Dataset")
    st.dataframe(df[["Date", "Building", "Water_Usage_Liters", "Cost_AED", "Is_Abnormal"]],
                 use_container_width=True, height=300)

# ──────────────────────────────────────────────
# PAGE: WATER USAGE DASHBOARD
# ──────────────────────────────────────────────
elif selected.startswith("📊"):
    st.markdown("""
    <div class="hero-banner" style='padding:36px 40px;'>
        <div class="hero-title" style='font-size:1.9rem;'>📊 Water Usage Dashboard</div>
        <div class="hero-sub">Campus-wide water consumption trends and patterns</div>
    </div>""", unsafe_allow_html=True)

    if not require_data():
        st.stop()

    df = st.session_state.df
    stats = st.session_state.stats

    section_title("🔢", "Key Metrics")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(metric_card("💧", "Total Water Used",
                                fmt_num(stats["total_usage"]) + " L", "", "accent-blue"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("💰", "Total Cost",
                                f"AED {fmt_num(stats['total_cost'])}", "", "accent-green"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("📏", "Daily Avg Usage",
                                fmt_num(stats["avg"]) + " L", "Per day average", "accent-deep"), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card("🚨", "Abnormal Days",
                                str(stats["n_abnormal"]), "Usage spikes detected", "accent-red"), unsafe_allow_html=True)
    with c5:
        waste_pct = (stats["total_waste"] / stats["total_usage"] * 100) if stats["total_usage"] else 0
        st.markdown(metric_card("🌊", "Est. Wasted Water",
                                fmt_num(stats["total_waste"]) + " L",
                                f"{waste_pct:.1f}% of total usage", "accent-warn"), unsafe_allow_html=True)

    divider()

    # Daily trend
    section_title("📈", "Daily Water Usage Trend")
    daily = df.groupby("Date", as_index=False)["Water_Usage_Liters"].sum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily["Date"], y=daily["Water_Usage_Liters"],
        mode="lines", name="Daily Usage",
        line=dict(color="#0A7EA4", width=2.5),
        fill="tozeroy", fillcolor="rgba(10,126,164,0.08)"
    ))
    fig.add_hline(y=stats["avg"], line_dash="dot",
                  line_color="#00C5A1", annotation_text=f"Average: {stats['avg']:.0f} L",
                  annotation_font=dict(color="#00C5A1"))
    fig.add_hline(y=stats["thresh"], line_dash="dash",
                  line_color="#E84855", annotation_text="Abnormal Threshold",
                  annotation_font=dict(color="#E84855"))
    apply_theme(fig)
    fig.update_layout(title="Daily Water Consumption (All Buildings Combined)",
                      xaxis_title="Date", yaxis_title="Water Usage (Litres)")
    st.plotly_chart(fig, use_container_width=True)

    # Cost trend
    col1, col2 = st.columns(2)
    with col1:
        section_title("💸", "Daily Cost Trend (AED)")
        cost_daily = df.groupby("Date", as_index=False)["Cost_AED"].sum()
        fig2 = px.area(cost_daily, x="Date", y="Cost_AED",
                       color_discrete_sequence=["#00C5A1"],
                       title="Daily Cost in AED")
        apply_theme(fig2)
        fig2.update_traces(fillcolor="rgba(0,197,161,0.12)")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        section_title("📅", "Usage by Day of Week")
        dow = df.groupby("Day_of_Week")["Water_Usage_Liters"].mean().reindex(
            ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        ).reset_index()
        dow.columns = ["Day", "Avg_Usage"]
        fig3 = px.bar(dow, x="Day", y="Avg_Usage",
                      color="Avg_Usage", color_continuous_scale=["#6EC6E6","#003D52"],
                      title="Average Usage by Day of Week")
        apply_theme(fig3)
        st.plotly_chart(fig3, use_container_width=True)

    # Scatter: usage vs cost
    section_title("🔵", "Water Usage vs Cost Relationship")
    fig4 = px.scatter(df, x="Water_Usage_Liters", y="Cost_AED",
                      color="Building", size="Water_Usage_Liters",
                      hover_data=["Date", "Building"],
                      title="Water Usage (L) vs Cost (AED) — by Building",
                      color_discrete_sequence=PLOTLY_COLORS)
    apply_theme(fig4)
    st.plotly_chart(fig4, use_container_width=True)

# ──────────────────────────────────────────────
# PAGE: MONTHLY SUMMARY
# ──────────────────────────────────────────────
elif selected.startswith("📅"):
    st.markdown("""
    <div class="hero-banner" style='padding:36px 40px;'>
        <div class="hero-title" style='font-size:1.9rem;'>📅 Monthly Water Usage Summary</div>
        <div class="hero-sub">Month-by-month breakdown of consumption and costs</div>
    </div>""", unsafe_allow_html=True)

    if not require_data():
        st.stop()

    df = st.session_state.df

    monthly = df.groupby("Month_Name").agg(
        Total_Usage=("Water_Usage_Liters", "sum"),
        Total_Cost=("Cost_AED", "sum"),
        Avg_Daily=("Water_Usage_Liters", "mean"),
        Waste=("Wasted_Liters", "sum"),
        Abnormal_Days=("Is_Abnormal", "sum")
    ).reset_index()

    section_title("📊", "Monthly Consumption Overview")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=monthly["Month_Name"], y=monthly["Total_Usage"],
                         name="Total Usage (L)", marker_color="#0A7EA4"), secondary_y=False)
    fig.add_trace(go.Scatter(x=monthly["Month_Name"], y=monthly["Total_Cost"],
                             name="Cost (AED)", mode="lines+markers",
                             line=dict(color="#00C5A1", width=3),
                             marker=dict(size=8)), secondary_y=True)
    fig.update_layout(title="Monthly Water Usage & Cost", **PLOTLY_LAYOUT)
    fig.update_yaxes(title_text="Water Usage (L)", secondary_y=False)
    fig.update_yaxes(title_text="Cost (AED)", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig2 = px.bar(monthly, x="Month_Name", y="Waste",
                      color="Waste", color_continuous_scale=["#FFFACD","#E84855"],
                      title="Estimated Wasted Water per Month (L)")
        apply_theme(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        fig3 = px.line(monthly, x="Month_Name", y="Avg_Daily",
                       markers=True, title="Average Daily Usage per Month",
                       color_discrete_sequence=["#F5A623"])
        fig3.update_traces(line_width=3, marker_size=9)
        apply_theme(fig3)
        st.plotly_chart(fig3, use_container_width=True)

    section_title("📋", "Monthly Summary Table")
    monthly_display = monthly.copy()
    monthly_display.columns = ["Month", "Total Usage (L)", "Total Cost (AED)",
                                "Avg Daily (L)", "Wasted (L)", "Abnormal Days"]
    for col in ["Total Usage (L)", "Total Cost (AED)", "Avg Daily (L)", "Wasted (L)"]:
        monthly_display[col] = monthly_display[col].round(1)
    st.dataframe(monthly_display, use_container_width=True, hide_index=True)

# ──────────────────────────────────────────────
# PAGE: BUILDING COMPARISON
# ──────────────────────────────────────────────
elif selected.startswith("🏢"):
    st.markdown("""
    <div class="hero-banner" style='padding:36px 40px;'>
        <div class="hero-title" style='font-size:1.9rem;'>🏢 Building-wise Water Comparison</div>
        <div class="hero-sub">Identify which buildings use the most — and waste the most</div>
    </div>""", unsafe_allow_html=True)

    if not require_data():
        st.stop()

    df = st.session_state.df

    bld = df.groupby("Building").agg(
        Total_Usage=("Water_Usage_Liters", "sum"),
        Total_Cost=("Cost_AED", "sum"),
        Avg_Daily=("Water_Usage_Liters", "mean"),
        Wasted=("Wasted_Liters", "sum"),
        Abnormal_Days=("Is_Abnormal", "sum"),
        Days=("Water_Usage_Liters", "count")
    ).reset_index().sort_values("Total_Usage", ascending=False)

    section_title("🏆", "Building Rankings")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(bld, x="Building", y="Total_Usage",
                     color="Total_Usage", color_continuous_scale=["#6EC6E6", "#003D52"],
                     title="Total Water Usage by Building (L)",
                     text="Total_Usage")
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside",
                          textfont_size=10)
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.pie(bld, values="Total_Usage", names="Building",
                      title="Share of Total Water Usage",
                      color_discrete_sequence=PLOTLY_COLORS,
                      hole=0.42)
        fig2.update_traces(textposition="inside", textinfo="percent+label")
        apply_theme(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    section_title("💧", "Average Daily Usage vs Waste by Building")
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=bld["Building"], y=bld["Avg_Daily"],
                          name="Avg Daily Usage", marker_color="#0A7EA4"))
    fig3.add_trace(go.Bar(x=bld["Building"], y=bld["Wasted"],
                          name="Estimated Wasted", marker_color="#E84855"))
    fig3.update_layout(barmode="group",
                       title="Average Daily Usage vs Estimated Waste per Building",
                       **PLOTLY_LAYOUT)
    st.plotly_chart(fig3, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig4 = px.bar(bld.sort_values("Wasted", ascending=True),
                      x="Wasted", y="Building", orientation="h",
                      color="Wasted", color_continuous_scale=["#FFF3CC","#E84855"],
                      title="Wasted Water by Building (L)")
        apply_theme(fig4)
        st.plotly_chart(fig4, use_container_width=True)

    with col4:
        fig5 = px.scatter(bld, x="Avg_Daily", y="Total_Cost",
                          size="Total_Usage", color="Building",
                          title="Avg Daily Usage vs Total Cost",
                          color_discrete_sequence=PLOTLY_COLORS,
                          hover_data=["Abnormal_Days"])
        apply_theme(fig5)
        st.plotly_chart(fig5, use_container_width=True)

    section_title("📋", "Building Summary Table")
    bld_display = bld.round(1)
    bld_display.columns = ["Building", "Total Usage (L)", "Total Cost (AED)",
                            "Avg Daily (L)", "Wasted (L)", "Abnormal Days", "Total Records"]
    st.dataframe(bld_display, use_container_width=True, hide_index=True)

# ──────────────────────────────────────────────
# PAGE: ABNORMAL DETECTION
# ──────────────────────────────────────────────
elif selected.startswith("🚨"):
    st.markdown("""
    <div class="hero-banner" style='padding:36px 40px;'>
        <div class="hero-title" style='font-size:1.9rem;'>🚨 Abnormal Usage / Leak Detection</div>
        <div class="hero-sub">Statistical anomaly detection to flag potential leaks and waste</div>
    </div>""", unsafe_allow_html=True)

    if not require_data():
        st.stop()

    df = st.session_state.df
    stats = st.session_state.stats

    section_title("📐", "Detection Method")
    st.markdown(f"""
    <div class="info-box">
    <strong>How Abnormal Usage is Detected:</strong><br><br>
    We use a statistical method called the <strong>2-Standard-Deviation Rule</strong>. 
    Any day where water usage exceeds the <em>campus average + 2× standard deviation</em> 
    is flagged as abnormal — this may indicate a <strong>leak, broken valve, or unusual 
    consumption event</strong>.<br><br>
    📏 Campus Average: <strong>{stats['avg']:,.1f} L/day</strong> &nbsp;|&nbsp; 
    📊 Std Dev: <strong>{stats['std']:,.1f} L</strong> &nbsp;|&nbsp; 
    🚨 Threshold: <strong>{stats['thresh']:,.1f} L/day</strong>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    abn = df[df["Is_Abnormal"]]
    with c1:
        st.markdown(metric_card("🚨", "Abnormal Days", str(stats["n_abnormal"]),
                                f"Out of {stats['n_rows']} records", "accent-red"), unsafe_allow_html=True)
    with c2:
        pct = stats["n_abnormal"] / stats["n_rows"] * 100 if stats["n_rows"] else 0
        st.markdown(metric_card("📊", "Abnormal Rate",
                                f"{pct:.1f}%", "Of total data", "accent-warn"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("💧", "Est. Water Wasted",
                                fmt_num(stats["total_waste"]) + " L",
                                "From abnormal days", "accent-blue"), unsafe_allow_html=True)
    with c4:
        waste_cost = abn["Cost_AED"].sum() if len(abn) > 0 else 0
        st.markdown(metric_card("💰", "AED Loss (Abnormal)",
                                f"AED {fmt_num(waste_cost)}", "From abnormal days", "accent-deep"), unsafe_allow_html=True)

    divider()

    section_title("📈", "Usage Trend with Anomaly Markers")
    daily = df.groupby("Date").agg(
        Usage=("Water_Usage_Liters", "sum"),
        Abnormal=("Is_Abnormal", "any")
    ).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily["Date"], y=daily["Usage"],
        mode="lines", name="Daily Usage",
        line=dict(color="#0A7EA4", width=2),
        fill="tozeroy", fillcolor="rgba(10,126,164,0.07)"
    ))
    abn_daily = daily[daily["Abnormal"]]
    fig.add_trace(go.Scatter(
        x=abn_daily["Date"], y=abn_daily["Usage"],
        mode="markers", name="⚠️ Abnormal Day",
        marker=dict(color="#E84855", size=12, symbol="circle",
                    line=dict(color="white", width=2))
    ))
    fig.add_hline(y=stats["thresh"], line_dash="dash", line_color="#E84855",
                  annotation_text=f"Threshold: {stats['thresh']:,.0f} L",
                  annotation_font=dict(color="#E84855"))
    fig.add_hline(y=stats["avg"], line_dash="dot", line_color="#00C5A1",
                  annotation_text=f"Average: {stats['avg']:,.0f} L",
                  annotation_font=dict(color="#00C5A1"))
    apply_theme(fig)
    fig.update_layout(title="Daily Usage with Abnormal Days Highlighted",
                      xaxis_title="Date", yaxis_title="Usage (L)")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        section_title("🏢", "Abnormal Days by Building")
        abn_bld = df.groupby("Building")["Is_Abnormal"].sum().reset_index()
        abn_bld.columns = ["Building", "Abnormal_Days"]
        abn_bld = abn_bld[abn_bld["Abnormal_Days"] > 0].sort_values("Abnormal_Days", ascending=False)
        if len(abn_bld):
            fig2 = px.bar(abn_bld, x="Building", y="Abnormal_Days",
                          color="Abnormal_Days",
                          color_continuous_scale=["#FFD166", "#E84855"],
                          title="Number of Abnormal Days per Building")
            apply_theme(fig2)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No abnormal days detected by building.")

    with col2:
        section_title("📦", "Usage Distribution")
        fig3 = go.Figure()
        fig3.add_trace(go.Histogram(
            x=df["Water_Usage_Liters"], nbinsx=30,
            marker_color="#0A7EA4", opacity=0.7, name="Usage"
        ))
        fig3.add_vline(x=stats["avg"], line_dash="dot", line_color="#00C5A1",
                       annotation_text="Average")
        fig3.add_vline(x=stats["thresh"], line_dash="dash", line_color="#E84855",
                       annotation_text="Threshold")
        apply_theme(fig3)
        fig3.update_layout(title="Distribution of Daily Water Usage",
                           xaxis_title="Water Usage (L)", yaxis_title="Frequency")
        st.plotly_chart(fig3, use_container_width=True)

    section_title("📋", "Abnormal Usage Records")
    if len(abn):
        abn_display = abn[["Date", "Building", "Water_Usage_Liters", "Cost_AED", "Wasted_Liters"]].copy()
        abn_display.columns = ["Date", "Building", "Usage (L)", "Cost (AED)", "Wasted (L)"]
        abn_display = abn_display.sort_values("Wasted (L)", ascending=False)
        st.dataframe(abn_display.round(2), use_container_width=True, hide_index=True)
    else:
        st.markdown('<div class="success-box">✅ No abnormal usage records detected in this dataset.</div>',
                    unsafe_allow_html=True)

# ──────────────────────────────────────────────
# PAGE: IMPACT CALCULATOR
# ──────────────────────────────────────────────
elif selected.startswith("🌍"):
    st.markdown("""
    <div class="hero-banner" style='padding:36px 40px;'>
        <div class="hero-title" style='font-size:1.9rem;'>🌍 Water Impact Calculator</div>
        <div class="hero-sub">Understand the real-world environmental and financial cost of water waste</div>
    </div>""", unsafe_allow_html=True)

    if not require_data():
        st.stop()

    df = st.session_state.df
    stats = st.session_state.stats

    total_waste = stats["total_waste"]
    total_usage = stats["total_usage"]
    total_cost  = stats["total_cost"]
    abn_cost    = df[df["Is_Abnormal"]]["Cost_AED"].sum()

    # Yearly projections
    days_in_data = (df["Date"].max() - df["Date"].min()).days + 1
    daily_waste  = total_waste / days_in_data if days_in_data else 0
    yearly_waste = daily_waste * 365
    yearly_saving_50 = yearly_waste * 0.5
    yearly_cost_saving = (abn_cost / days_in_data) * 365 * 0.5 if days_in_data else 0

    # Environmental conversions
    CO2_PER_LITER      = 0.000344   # kg CO2 per litre desalinated
    KWH_PER_LITER      = 0.004      # kWh energy per litre
    BOTTLES_PER_LITER  = 2          # 500ml bottles
    TREES_PER_1000L    = 0.05       # tree equivalent

    co2_saved   = yearly_saving_50 * CO2_PER_LITER
    kwh_saved   = yearly_saving_50 * KWH_PER_LITER
    bottles     = yearly_saving_50 * BOTTLES_PER_LITER
    trees_equiv = yearly_saving_50 * TREES_PER_1000L / 1000

    section_title("📊", "Current Waste Metrics")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card("💧", "Total Wasted Water",
                                fmt_num(total_waste) + " L", "From abnormal days", "accent-red"), unsafe_allow_html=True)
    with c2:
        waste_pct = total_waste / total_usage * 100 if total_usage else 0
        st.markdown(metric_card("📊", "Waste Percentage",
                                f"{waste_pct:.1f}%", "Of total consumption", "accent-warn"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("💰", "AED Cost of Waste",
                                f"AED {fmt_num(abn_cost)}", "From abnormal records", "accent-blue"), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card("📅", "Data Period",
                                f"{days_in_data} Days",
                                f"{df['Date'].min().date()} – {df['Date'].max().date()}", "accent-deep"), unsafe_allow_html=True)

    divider()

    section_title("🌱", "Projected Yearly Impact (If 50% Waste is Reduced)")
    st.markdown("""
    <div class="info-box">
    The following projections show what could be saved annually if abnormal water usage is 
    reduced by <strong>50%</strong> through leak repairs and behavioural changes — a realistic 
    and achievable target for most campuses.
    </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card("💧", "Water Saved / Year",
                                fmt_num(yearly_saving_50) + " L", "50% of yearly waste", "accent-green"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("💰", "AED Saved / Year",
                                f"AED {fmt_num(yearly_cost_saving)}", "Projected financial saving", "accent-blue"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("🌿", "CO₂ Reduced",
                                f"{co2_saved:,.1f} kg", "Less carbon from desalination", "accent-deep"), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card("⚡", "Energy Saved",
                                f"{kwh_saved:,.1f} kWh", "Desalination energy reduction", "accent-warn"), unsafe_allow_html=True)

    c5, c6, _, _ = st.columns(4)
    with c5:
        st.markdown(metric_card("🍶", "Plastic Bottles Equiv.",
                                fmt_num(bottles), "500ml bottles saved from waste", "accent-red"), unsafe_allow_html=True)
    with c6:
        st.markdown(metric_card("🌳", "Tree CO₂ Equiv.",
                                f"{trees_equiv:,.0f}", "Trees equivalent in CO₂ offset", "accent-green"), unsafe_allow_html=True)

    divider()

    section_title("📊", "Waste vs. Normal Usage Breakdown")
    pie_data = pd.DataFrame({
        "Category": ["Normal Usage", "Estimated Waste"],
        "Litres": [total_usage - total_waste, total_waste]
    })
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(pie_data, values="Litres", names="Category",
                     color_discrete_sequence=["#0A7EA4", "#E84855"],
                     title="Normal vs Wasted Water", hole=0.5)
        fig.update_traces(textinfo="percent+label")
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Savings waterfall
        fig2 = go.Figure(go.Waterfall(
            name="Savings Breakdown",
            orientation="v",
            measure=["relative", "relative", "relative", "total"],
            x=["Total Waste", "50% Reduction", "Remaining Waste", "Net Saving"],
            y=[yearly_waste, -yearly_saving_50, yearly_saving_50, 0],
            connector={"line": {"color": "#D0E8F0"}},
            increasing={"marker": {"color": "#E84855"}},
            decreasing={"marker": {"color": "#00C5A1"}},
            totals={"marker": {"color": "#0A7EA4"}},
        ))
        apply_theme(fig2)
        fig2.update_layout(title="Projected Yearly Waste & Savings (L)")
        st.plotly_chart(fig2, use_container_width=True)

    # Custom slider
    divider()
    section_title("🎛️", "Custom Reduction Scenario")
    reduction_pct = st.slider("Select waste reduction target (%)", 10, 90, 50, 5)
    custom_saving = yearly_waste * (reduction_pct / 100)
    custom_cost   = yearly_cost_saving * (reduction_pct / 50)
    custom_co2    = custom_saving * CO2_PER_LITER

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(metric_card("💧", f"Water Saved at {reduction_pct}%",
                                fmt_num(custom_saving) + " L/yr", "", "accent-blue"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("💰", "AED Saved",
                                f"AED {fmt_num(custom_cost)}/yr", "", "accent-green"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("🌿", "CO₂ Avoided",
                                f"{custom_co2:,.2f} kg/yr", "", "accent-deep"), unsafe_allow_html=True)

# ──────────────────────────────────────────────
# PAGE: AI RECOMMENDATIONS
# ──────────────────────────────────────────────
elif selected.startswith("🤖"):
    st.markdown("""
    <div class="hero-banner" style='padding:36px 40px;'>
        <div class="hero-title" style='font-size:1.9rem;'>🤖 AI-Style Water Saving Recommendations</div>
        <div class="hero-sub">Smart, data-driven actions tailored to your campus usage patterns</div>
    </div>""", unsafe_allow_html=True)

    if not require_data():
        st.stop()

    df = st.session_state.df
    stats = st.session_state.stats

    buildings = df["Building"].unique().tolist()
    waste_pct  = stats["total_waste"] / stats["total_usage"] * 100 if stats["total_usage"] else 0

    st.markdown(f"""
    <div class="warn-box">
    ⚠️ <strong>Waste Alert:</strong> Your campus is wasting an estimated 
    <strong>{waste_pct:.1f}%</strong> of its total water on abnormal usage days. 
    The recommendations below are generated based on your specific data patterns.
    </div>""", unsafe_allow_html=True)

    # Building-specific recs
    bld_abn = df.groupby("Building").agg(
        Abnormal_Days=("Is_Abnormal", "sum"),
        Wasted=("Wasted_Liters", "sum"),
        Avg_Usage=("Water_Usage_Liters", "mean")
    ).reset_index().sort_values("Abnormal_Days", ascending=False)

    top_offenders = bld_abn[bld_abn["Abnormal_Days"] > 0]["Building"].tolist()

    section_title("🏢", "Building-Specific Alerts")
    if top_offenders:
        for bld in top_offenders[:5]:
            row = bld_abn[bld_abn["Building"] == bld].iloc[0]
            st.markdown(f"""
            <div class="danger-box">
            🚨 <strong>{bld}</strong> — {int(row['Abnormal_Days'])} abnormal day(s) detected, 
            with an estimated <strong>{row['Wasted']:,.0f} L</strong> of wasted water. 
            Immediate inspection recommended.
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-box">✅ No buildings with critical abnormal usage detected.</div>',
                    unsafe_allow_html=True)

    divider()

    section_title("💡", "Smart Water-Saving Recommendations")

    RECS = [
        ("🔧", "Fix Leaks Immediately",
         f"Your data shows {stats['n_abnormal']} abnormal usage days. "
         "Even a small dripping tap can waste over 10,000 litres per year. "
         "Conduct a full plumbing inspection in all flagged buildings.",
         "Potential saving: 30–50% of wasted water"),
        ("📱", "Install Smart Water Meters",
         "Deploy IoT-enabled water meters in each building to get real-time alerts "
         "when usage exceeds normal thresholds — the same statistical logic this "
         "dashboard uses, running live 24/7.",
         "Enables instant leak detection"),
        ("🚿", "Upgrade to Low-Flow Fixtures",
         "Replacing standard taps, showers, and toilets with low-flow alternatives can "
         "reduce water consumption by 30–50% with no change in user behaviour. "
         "Prioritise buildings with highest average daily usage.",
         "Typical saving: 30–45% per fixture"),
        ("🌿", "Greywater Recycling System",
         "Implement greywater recycling to reuse sink and shower water for toilet flushing "
         "and landscape irrigation. UAE campuses with greywater systems report savings of "
         "up to 40% in potable water demand.",
         "Up to 40% potable water reduction"),
        ("👥", "Water Awareness Campaign",
         "Launch a monthly sustainability challenge on campus. Behavioural change programmes "
         "at UAE universities have achieved 15–25% consumption reductions within 3 months "
         "through student and staff engagement.",
         "15–25% usage reduction"),
        ("🗓️", "Scheduled Maintenance Programme",
         "Set up quarterly plumbing audits for all campus buildings. "
         "Preventive maintenance is 10× cheaper than emergency repairs and "
         "prevents the slow leaks that are hardest to detect without data.",
         "Reduces abnormal days by 60–80%"),
        ("☀️", "Solar-Powered Water Heating",
         "Switching to solar water heaters reduces energy costs and aligns with the "
         "UAE Net Zero 2050 strategy. Combine with insulated pipes to eliminate "
         "heat-loss waste.",
         "Reduces energy+water waste by 20%"),
        ("🌱", "Drought-Resistant Landscaping",
         "Replace water-intensive grass with UAE-native plants and drip irrigation systems. "
         "Landscape irrigation accounts for up to 50% of campus water use in hot months.",
         "Up to 50% irrigation saving"),
    ]

    for icon, title, body, saving in RECS:
        st.markdown(f"""
        <div class="rec-card">
            <div class="rec-icon-box">{icon}</div>
            <div>
                <div class="rec-title">{title}</div>
                <div class="rec-body">{body}</div>
                <div class="rec-saving">💚 {saving}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    divider()

    section_title("📊", "Recommended Priority Matrix")
    priority_data = pd.DataFrame({
        "Action": ["Fix Leaks", "Smart Meters", "Low-Flow Fixtures",
                   "Greywater System", "Awareness Campaign"],
        "Impact_Score": [95, 85, 75, 70, 55],
        "Ease_Score": [80, 50, 70, 35, 90],
        "Cost_AED_000": [5, 80, 40, 150, 2],
    })
    fig = px.scatter(priority_data,
                     x="Ease_Score", y="Impact_Score",
                     size="Cost_AED_000", text="Action",
                     color="Impact_Score",
                     color_continuous_scale=["#6EC6E6","#003D52"],
                     title="Priority Matrix: Impact vs. Ease of Implementation",
                     labels={"Ease_Score": "Ease of Implementation →",
                             "Impact_Score": "Water Saving Impact ↑"})
    fig.update_traces(textposition="top center")
    apply_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

# ──────────────────────────────────────────────
# PAGE: FINAL REPORT
# ──────────────────────────────────────────────
elif selected.startswith("📋"):
    st.markdown("""
    <div class="hero-banner" style='padding:36px 40px;'>
        <div class="hero-title" style='font-size:1.9rem;'>📋 Final Impact Report Summary</div>
        <div class="hero-sub">Competition-ready summary of your campus water sustainability analysis</div>
    </div>""", unsafe_allow_html=True)

    if not require_data():
        st.stop()

    df = st.session_state.df
    stats = st.session_state.stats

    total_usage   = stats["total_usage"]
    total_cost    = stats["total_cost"]
    total_waste   = stats["total_waste"]
    n_abnormal    = stats["n_abnormal"]
    avg           = stats["avg"]
    thresh        = stats["thresh"]
    abn_cost      = df[df["Is_Abnormal"]]["Cost_AED"].sum()
    days_in_data  = (df["Date"].max() - df["Date"].min()).days + 1
    waste_pct     = total_waste / total_usage * 100 if total_usage else 0
    yearly_waste  = (total_waste / days_in_data) * 365
    yearly_save   = yearly_waste * 0.5
    yearly_aed    = (abn_cost / days_in_data) * 365 * 0.5
    co2_save      = yearly_save * 0.000344
    buildings_n   = df["Building"].nunique()

    # Report header card
    st.markdown(f"""
    <div class="report-card">
        <div style='font-family:Syne,sans-serif; font-size:1.4rem; font-weight:800;
                    color:#FFFFFF; margin-bottom:6px;'>
            🏆 AquaSense UAE — Campus Water Impact Report
        </div>
        <div style='color:rgba(255,255,255,0.7); font-size:0.88rem; margin-bottom:24px;'>
            Generated: {datetime.now().strftime("%d %B %Y, %H:%M")} &nbsp;|&nbsp;
            Data Range: {df['Date'].min().date()} → {df['Date'].max().date()} &nbsp;|&nbsp;
            Buildings Analysed: {buildings_n}
        </div>
        <div style='display:grid; grid-template-columns:repeat(4,1fr); gap:16px;'>
            <div class="report-stat">
                <div class="report-stat-val">{fmt_num(total_usage)} L</div>
                <div class="report-stat-label">Total Water Consumed</div>
            </div>
            <div class="report-stat">
                <div class="report-stat-val">AED {fmt_num(total_cost)}</div>
                <div class="report-stat-label">Total Water Cost</div>
            </div>
            <div class="report-stat">
                <div class="report-stat-val">{n_abnormal}</div>
                <div class="report-stat-label">Abnormal Usage Days</div>
            </div>
            <div class="report-stat">
                <div class="report-stat-val">{waste_pct:.1f}%</div>
                <div class="report-stat-label">Water Wasted (Est.)</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    section_title("🌱", "Projected Yearly Savings (50% Waste Reduction)")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card("💧", "Water Saved / Year",
                                fmt_num(yearly_save) + " L", "Projected annual saving", "accent-green"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("💰", "AED Saved / Year",
                                f"AED {fmt_num(yearly_aed)}", "Financial saving potential", "accent-blue"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("🌿", "CO₂ Avoided",
                                f"{co2_save:,.1f} kg", "Less carbon emissions", "accent-deep"), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card("🏢", "Buildings Analysed",
                                str(buildings_n), "Campus buildings", "accent-warn"), unsafe_allow_html=True)

    divider()

    col1, col2 = st.columns(2)
    with col1:
        section_title("📊", "Usage vs Waste Breakdown")
        pie = pd.DataFrame({
            "Category": ["Normal Usage", "Estimated Waste"],
            "Value": [total_usage - total_waste, total_waste]
        })
        fig = px.pie(pie, values="Value", names="Category",
                     color_discrete_sequence=["#0A7EA4","#E84855"],
                     hole=0.5, title="Total Water: Normal vs Wasted")
        apply_theme(fig)
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_title("🏢", "Building Usage Share")
        bld_share = df.groupby("Building")["Water_Usage_Liters"].sum().reset_index()
        fig2 = px.pie(bld_share, values="Water_Usage_Liters", names="Building",
                      color_discrete_sequence=PLOTLY_COLORS,
                      hole=0.5, title="Water Usage Share by Building")
        apply_theme(fig2)
        fig2.update_traces(textinfo="percent+label")
        st.plotly_chart(fig2, use_container_width=True)

    # Monthly trend
    section_title("📅", "Monthly Consumption Trend")
    monthly = df.groupby("Month_Name").agg(
        Usage=("Water_Usage_Liters","sum"),
        Cost=("Cost_AED","sum")
    ).reset_index()
    fig3 = px.bar(monthly, x="Month_Name", y="Usage",
                  color="Usage", color_continuous_scale=["#6EC6E6","#003D52"],
                  title="Monthly Total Water Usage (L)")
    apply_theme(fig3)
    st.plotly_chart(fig3, use_container_width=True)

    divider()

    section_title("📝", "Key Findings & Conclusions")
    findings = [
        f"📍 Campus consumed a total of **{total_usage:,.0f} litres** of water over the analysis period ({days_in_data} days).",
        f"💰 Total cost incurred: **AED {total_cost:,.2f}** — averaging AED {total_cost/days_in_data:,.2f} per day.",
        f"🚨 **{n_abnormal} abnormal usage events** were detected using the 2σ statistical rule (threshold: {thresh:,.0f} L/day).",
        f"🌊 An estimated **{total_waste:,.0f} litres** of water was wasted through abnormal events, representing **{waste_pct:.1f}%** of total usage.",
        f"🌱 With a **50% reduction in abnormal usage**, the campus could save **{yearly_save:,.0f} L/year** and **AED {yearly_aed:,.2f}/year**.",
        f"🌿 This would prevent approximately **{co2_save:,.2f} kg of CO₂** from desalination energy — aligning with UAE Net Zero 2050.",
        f"🏢 **{buildings_n} buildings** were analysed; targeted interventions in the highest-waste buildings offer the greatest return.",
    ]
    for finding in findings:
        st.markdown(finding)

    divider()

    section_title("🎯", "Top 3 Recommended Actions")
    top3 = [
        ("1", "🔧", "Immediate Plumbing Inspection",
         f"Inspect and repair all flagged buildings. {n_abnormal} abnormal days detected — "
         "likely caused by leaking pipes or faulty valves."),
        ("2", "📱", "Deploy Smart Water Meters",
         "Install IoT sensors in all buildings for real-time monitoring and instant "
         "anomaly alerts — automate what this dashboard detects manually."),
        ("3", "🚿", "Low-Flow Fixture Upgrade",
         "Upgrade taps and toilets in the highest-usage buildings first. "
         "ROI typically within 12–18 months in UAE campus conditions."),
    ]
    for num, icon, title, body in top3:
        st.markdown(f"""
        <div class="rec-card">
            <div style='width:44px; height:44px; border-radius:12px;
                        background:linear-gradient(135deg,#003D52,#0A7EA4);
                        color:white; font-family:Syne,sans-serif; font-weight:800;
                        font-size:1.2rem; display:flex; align-items:center;
                        justify-content:center; flex-shrink:0;'>{num}</div>
            <div>
                <div class="rec-title">{icon} {title}</div>
                <div class="rec-body">{body}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    # Export
    divider()
    section_title("⬇️", "Export Report Data")

    export_df = df[["Date","Building","Water_Usage_Liters","Cost_AED",
                    "Is_Abnormal","Wasted_Liters"]].copy()
    export_df.columns = ["Date","Building","Water_Usage_L","Cost_AED",
                         "Is_Abnormal","Wasted_L"]

    csv_bytes = export_df.to_csv(index=False).encode("utf-8")
    col_dl1, col_dl2, _ = st.columns([1, 1, 2])
    with col_dl1:
        st.download_button(
            label="📥 Download Full Dataset (CSV)",
            data=csv_bytes,
            file_name="aquasense_water_report.csv",
            mime="text/csv",
            use_container_width=True
        )

    summary_rows = {
        "Metric": [
            "Total Water Usage (L)", "Total Cost (AED)", "Analysis Period (days)",
            "Number of Buildings", "Average Daily Usage (L)", "Abnormal Days Detected",
            "Estimated Wasted Water (L)", "Waste as % of Total",
            "Projected Yearly Waste (L)", "Projected Yearly Saving 50% (L)",
            "Projected AED Saving/Year", "CO2 Avoided/Year (kg)"
        ],
        "Value": [
            f"{total_usage:,.1f}", f"{total_cost:,.2f}", str(days_in_data),
            str(buildings_n), f"{avg:,.1f}", str(n_abnormal),
            f"{total_waste:,.1f}", f"{waste_pct:.2f}%",
            f"{yearly_waste:,.1f}", f"{yearly_save:,.1f}",
            f"{yearly_aed:,.2f}", f"{co2_save:,.4f}"
        ]
    }
    summary_csv = pd.DataFrame(summary_rows).to_csv(index=False).encode("utf-8")
    with col_dl2:
        st.download_button(
            label="📊 Download Summary Report (CSV)",
            data=summary_csv,
            file_name="aquasense_summary_report.csv",
            mime="text/csv",
            use_container_width=True
        )

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown("""
<div class="footer">
    💧 <strong>AquaSense UAE</strong> — AI-Powered Water Impact Dashboard for Sustainable Campuses<br>
    🏆 RAK EISC 2026 · Third Place &nbsp;|&nbsp; 🎖️ RAK Department of Knowledge Recognition &nbsp;|&nbsp; 💰 AED 1,000 Cash Prize<br>
    <span style='color:#B0C8D0; font-size:0.75rem;'>Built with Streamlit · Plotly · Pandas · NumPy &nbsp;|&nbsp; UAE Sustainability Initiative</span>
</div>""", unsafe_allow_html=True)
