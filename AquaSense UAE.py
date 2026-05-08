"""
AquaSense UAE: AI-Powered Water Impact Dashboard for Sustainable Campuses
Submitted to: Sustainable Impact Challenge 2026 (UAE National Government Initiative)
Previously Awarded: RAK EISC 2026 – Third Place | RAK Dept. of Knowledge | AED 1,000 Prize
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from datetime import datetime

# ─────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AquaSense UAE | Smart Water Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────
# GLOBAL CSS  — works on both light & dark Streamlit themes
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');

/* ── force a clean white canvas ── */
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    background: #F0F8FC !important;
}
.main .block-container {
    background: #F0F8FC !important;
    padding-top: 1.5rem !important;
    max-width: 1300px !important;
}
/* override any dark-mode leftover on markdown containers */
[data-testid="stMarkdownContainer"] {
    color: #1A2E35 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #003D52 0%, #005670 55%, #0A7EA4 100%) !important;
}
[data-testid="stSidebar"] * { color: #E0F4FB !important; }
[data-testid="stSidebar"] .stRadio > label { display: none; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 6px 2px !important;
    cursor: pointer;
}

/* ── Typography ── */
h1,h2,h3,h4,h5,h6 { font-family: 'Syne', sans-serif !important; color: #003D52 !important; }
body, p, span, div { font-family: 'DM Sans', sans-serif; }

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #003D52 0%, #0A7EA4 55%, #00C5A1 100%);
    border-radius: 20px;
    padding: 44px 48px 38px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content:''; position:absolute; top:-70px; right:-70px;
    width:300px; height:300px; border-radius:50%;
    background:rgba(255,255,255,0.05);
}
.hero-banner::after {
    content:''; position:absolute; bottom:-50px; left:32%;
    width:200px; height:200px; border-radius:50%;
    background:rgba(0,197,161,0.10);
}
.hero-title {
    font-family:'Syne',sans-serif; font-size:2.5rem; font-weight:800;
    color:#FFFFFF !important; margin:0 0 8px; line-height:1.15;
    position:relative; z-index:1;
}
.hero-sub {
    font-size:1.05rem; color:rgba(255,255,255,0.85);
    margin:0 0 20px; position:relative; z-index:1;
}
.badge-row { display:flex; gap:10px; flex-wrap:wrap; position:relative; z-index:1; }
.badge {
    background:rgba(255,255,255,0.18);
    border:1px solid rgba(255,255,255,0.35);
    border-radius:30px; padding:5px 15px;
    font-size:0.78rem; color:#FFFFFF;
    font-family:'DM Sans',sans-serif; font-weight:600;
}

/* ── Section Title ── */
.section-title {
    font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:700;
    color:#003D52 !important; margin:28px 0 16px;
    display:flex; align-items:center; gap:10px;
}
.section-title .dot {
    display:inline-block; width:10px; height:10px;
    border-radius:50%; background:#00C5A1; flex-shrink:0;
}

/* ── Metric Cards ── */
.metric-card {
    background:#FFFFFF; border-radius:16px; padding:22px 24px;
    border:1px solid #D0E8F0;
    box-shadow:0 2px 14px rgba(10,126,164,0.08);
    transition:transform 0.18s ease, box-shadow 0.18s ease;
    margin-bottom:4px;
}
.metric-card:hover { transform:translateY(-3px); box-shadow:0 8px 28px rgba(10,126,164,0.15); }
.metric-icon { font-size:1.6rem; margin-bottom:8px; }
.metric-label {
    font-size:0.73rem; color:#5A7A85; text-transform:uppercase;
    letter-spacing:0.9px; margin-bottom:4px; font-weight:600;
}
.metric-value {
    font-family:'Syne',sans-serif; font-size:1.65rem; font-weight:700;
    color:#003D52 !important; line-height:1;
}
.metric-delta { font-size:0.78rem; margin-top:6px; color:#5A7A85; }
.m-green { border-left:4px solid #00C5A1; }
.m-blue  { border-left:4px solid #0A7EA4; }
.m-red   { border-left:4px solid #E84855; }
.m-warn  { border-left:4px solid #F5A623; }
.m-deep  { border-left:4px solid #003D52; }
.m-gold  { border-left:4px solid #FFD700; }

/* ── Info / Alert Boxes ── */
.box {
    border-radius:12px; padding:16px 20px;
    margin:14px 0; font-size:0.92rem;
    color:#1A2E35 !important; line-height:1.6;
}
.box b, .box strong { color:#003D52 !important; }
.box-info    { background:#E3F4FD; border-left:4px solid #0A7EA4; }
.box-success { background:#E4F9F4; border-left:4px solid #00C5A1; }
.box-warn    { background:#FFF6E3; border-left:4px solid #F5A623; }
.box-danger  { background:#FDECEA; border-left:4px solid #E84855; }
.box-gold    { background:#FFFBEA; border-left:4px solid #FFD700; }
.box-purple  { background:#F3EEFF; border-left:4px solid #7C3AED; }

/* ── Steps (How to Use) ── */
.step-item {
    display:flex; align-items:center; gap:14px;
    padding:10px 14px; background:#FFFFFF;
    border-radius:12px; margin-bottom:8px;
    border:1px solid #D0E8F0;
}
.step-num {
    width:32px; height:32px; border-radius:50%; flex-shrink:0;
    background:linear-gradient(135deg,#0A7EA4,#00C5A1);
    color:#FFFFFF; font-family:'Syne',sans-serif; font-weight:800;
    font-size:0.9rem; display:flex; align-items:center; justify-content:center;
}
.step-text { font-size:0.88rem; color:#1A2E35 !important; font-weight:500; }

/* ── Feature List ── */
.feature-row {
    display:flex; align-items:flex-start; gap:12px;
    padding:10px 0; border-bottom:1px solid #D0E8F0;
}
.feature-icon { font-size:1.05rem; flex-shrink:0; margin-top:1px; }
.feature-text { font-size:0.89rem; color:#1A2E35 !important; line-height:1.45; }

/* ── Award Cards ── */
.award-card {
    background:#FFFFFF; border-radius:14px; padding:18px 20px;
    border:1px solid #D0E8F0; margin-bottom:12px;
    box-shadow:0 2px 10px rgba(10,126,164,0.06);
}
.award-title {
    font-family:'Syne',sans-serif; font-size:1.05rem; font-weight:700;
    color:#003D52 !important; margin:6px 0 2px;
}
.award-sub { font-size:0.82rem; color:#5A7A85; }

/* ── Recommendation Cards ── */
.rec-card {
    background:#FFFFFF; border-radius:14px; padding:20px 22px;
    border:1px solid #D0E8F0; margin-bottom:14px;
    display:flex; gap:16px; align-items:flex-start;
    box-shadow:0 2px 10px rgba(10,126,164,0.05);
}
.rec-icon {
    width:46px; height:46px; border-radius:13px; flex-shrink:0;
    background:linear-gradient(135deg,#0A7EA4,#00C5A1);
    display:flex; align-items:center; justify-content:center;
    font-size:1.3rem;
}
.rec-title {
    font-family:'Syne',sans-serif; font-size:0.97rem; font-weight:700;
    color:#003D52 !important; margin-bottom:5px;
}
.rec-body { font-size:0.86rem; color:#3A5A65 !important; line-height:1.55; }
.rec-tag {
    display:inline-block; background:#E4F9F4; color:#007A60 !important;
    border-radius:20px; padding:3px 11px; font-size:0.75rem;
    font-weight:700; margin-top:7px;
}

/* ── Competition Profile ── */
.comp-hero {
    background:linear-gradient(135deg, #7C3AED 0%, #0A7EA4 60%, #00C5A1 100%);
    border-radius:20px; padding:40px 44px; margin-bottom:24px;
    position:relative; overflow:hidden;
}
.comp-hero::after {
    content:''; position:absolute; top:-60px; right:-60px;
    width:260px; height:260px; border-radius:50%;
    background:rgba(255,255,255,0.06);
}
.comp-title {
    font-family:'Syne',sans-serif; font-size:2.2rem; font-weight:800;
    color:#FFFFFF !important; margin:0 0 8px; position:relative; z-index:1;
}
.comp-sub { color:rgba(255,255,255,0.85); font-size:1rem; position:relative; z-index:1; }
.timeline-item {
    display:flex; gap:14px; align-items:flex-start;
    padding:14px 16px; background:#FFFFFF;
    border-radius:12px; margin-bottom:10px;
    border:1px solid #D0E8F0;
    box-shadow:0 1px 6px rgba(10,126,164,0.05);
}
.timeline-dot {
    width:36px; height:36px; border-radius:50%; flex-shrink:0;
    display:flex; align-items:center; justify-content:center;
    font-size:1rem; font-weight:700;
}
.timeline-title {
    font-family:'Syne',sans-serif; font-size:0.92rem; font-weight:700;
    color:#003D52 !important; margin-bottom:2px;
}
.timeline-sub { font-size:0.81rem; color:#5A7A85 !important; }

/* ── SDG Card ── */
.sdg-card {
    background:linear-gradient(135deg,#0A7EA4,#00C5A1);
    border-radius:16px; padding:24px; color:white; text-align:center;
    margin-bottom:14px;
}
.sdg-num { font-family:'Syne',sans-serif; font-size:2.4rem; font-weight:800; color:#FFFFFF !important; }
.sdg-label { font-size:0.82rem; color:rgba(255,255,255,0.85); margin-top:4px; }

/* ── Impact stat grid ── */
.impact-grid {
    display:grid; grid-template-columns:repeat(2,1fr); gap:12px; margin-top:12px;
}
.impact-stat {
    background:#FFFFFF; border-radius:12px; padding:16px;
    border:1px solid #D0E8F0; text-align:center;
}
.impact-val {
    font-family:'Syne',sans-serif; font-size:1.5rem; font-weight:800;
    color:#0A7EA4 !important;
}
.impact-lbl { font-size:0.76rem; color:#5A7A85 !important; margin-top:3px; }

/* ── Report Hero ── */
.report-card {
    background:linear-gradient(135deg,#003D52,#005670,#0A7EA4);
    border-radius:20px; padding:36px 40px; color:white; margin-bottom:20px;
}
.report-val {
    font-family:'Syne',sans-serif; font-size:2rem; font-weight:800;
    color:#00C5A1 !important;
}
.report-lbl { font-size:0.8rem; color:rgba(255,255,255,0.7) !important; margin-top:4px; }

/* ── Divider ── */
.divider {
    height:2px; border:none; margin:28px 0; border-radius:2px;
    background:linear-gradient(90deg, #00C5A1 0%, rgba(0,197,161,0) 100%);
}

/* ── Progress bar ── */
.stProgress > div > div > div { background:linear-gradient(90deg,#0A7EA4,#00C5A1) !important; }

/* ── Download button ── */
.stDownloadButton button {
    background:linear-gradient(135deg,#0A7EA4,#00C5A1) !important;
    color:white !important; border:none !important;
    border-radius:10px !important; font-weight:600 !important;
    font-family:'DM Sans',sans-serif !important;
}

/* ── Data tables ── */
[data-testid="stDataFrame"] { border-radius:12px; overflow:hidden; }
.stDataFrame thead th { background:#003D52 !important; color:#FFFFFF !important; }

/* ── Upload area ── */
[data-testid="stFileUploader"] section {
    border:2px dashed #0A7EA4 !important;
    border-radius:14px !important;
    background:#F0F8FC !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width:6px; height:6px; }
::-webkit-scrollbar-track { background:#F0F8FC; }
::-webkit-scrollbar-thumb { background:#0A7EA4; border-radius:3px; }

/* ── Footer ── */
.footer {
    text-align:center; padding:22px;
    color:#5A7A85 !important; font-size:0.79rem;
    border-top:1px solid #D0E8F0; margin-top:40px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────────────────
COLORS = ["#0A7EA4","#00C5A1","#003D52","#F5A623","#E84855",
          "#6EC6E6","#4BC8A8","#2D6E8A","#FFD166","#EF8354"]

BASE_LAYOUT = dict(
    font_family="DM Sans",
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=20, r=20, t=44, b=20),
    colorway=COLORS,
    title_font=dict(family="Syne", size=15, color="#003D52"),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)

def T(fig):
    fig.update_layout(**BASE_LAYOUT)
    fig.update_xaxes(showgrid=True, gridcolor="#E8F3F8", linecolor="#D0E8F0", tickfont_color="#5A7A85")
    fig.update_yaxes(showgrid=True, gridcolor="#E8F3F8", linecolor="#D0E8F0", tickfont_color="#5A7A85")
    return fig

# ─────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────
def fmt(n, dec=0):
    if n >= 1_000_000: return f"{n/1_000_000:.2f}M"
    if n >= 1_000:     return f"{n/1_000:.1f}K"
    return f"{n:,.{dec}f}"

def mcard(icon, label, value, delta="", cls="m-blue"):
    d = f"<div class='metric-delta'>{delta}</div>" if delta else ""
    return f"""<div class='metric-card {cls}'>
        <div class='metric-icon'>{icon}</div>
        <div class='metric-label'>{label}</div>
        <div class='metric-value'>{value}</div>{d}
    </div>"""

def stitle(icon, text):
    st.markdown(f"""<div class='section-title'>
        {icon} <span class='dot'></span> {text}
    </div>""", unsafe_allow_html=True)

def hr(): st.markdown("<hr class='divider'>", unsafe_allow_html=True)

def box(content, kind="info"):
    st.markdown(f"<div class='box box-{kind}'>{content}</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# DATA LOADING & PROCESSING
# ─────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_file(b, name):
    return pd.read_csv(io.BytesIO(b)) if name.endswith(".csv") else pd.read_excel(io.BytesIO(b))

def process(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Water_Usage_Liters"] = pd.to_numeric(df["Water_Usage_Liters"], errors="coerce")
    df["Cost_AED"]           = pd.to_numeric(df["Cost_AED"], errors="coerce")
    df = df.dropna(subset=["Date","Water_Usage_Liters","Cost_AED"]).reset_index(drop=True)
    df = df.sort_values("Date").reset_index(drop=True)

    avg   = df["Water_Usage_Liters"].mean()
    std   = df["Water_Usage_Liters"].std()
    thr   = avg + 2 * std

    df["Is_Abnormal"]   = df["Water_Usage_Liters"] > thr
    df["Wasted_Liters"] = np.where(df["Is_Abnormal"], df["Water_Usage_Liters"] - avg, 0)
    df["Month_Label"]   = df["Date"].dt.strftime("%b %Y")
    df["Day_of_Week"]   = df["Date"].dt.day_name()
    return df, avg, std, thr

# ─────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────
for k, v in [("df_raw", None), ("df", None), ("stats", {})]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:22px 0 12px;'>
        <div style='font-size:2.6rem;'>💧</div>
        <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;
                    color:#E0F4FB;line-height:1.2;'>AquaSense UAE</div>
        <div style='font-size:0.68rem;color:rgba(224,244,251,0.6);
                    margin-top:4px;letter-spacing:1.2px;'>SMART WATER DASHBOARD</div>
    </div>
    <hr style='border-color:rgba(255,255,255,0.15);margin:8px 0 16px;'>
    """, unsafe_allow_html=True)

    PAGES = [
        "🏠  Home / Project Overview",
        "🏆  Competition Profile",
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
    page = st.radio("nav", PAGES, label_visibility="collapsed")

    st.markdown("""
    <hr style='border-color:rgba(255,255,255,0.15);margin:16px 0 10px;'>
    <div style='font-size:0.71rem;color:rgba(224,244,251,0.5);
                text-align:center;padding-bottom:8px;line-height:1.8;'>
        🏆 RAK EISC 2026 · 3rd Place<br>
        🎖️ RAK Dept. of Knowledge Award<br>
        💰 AED 1,000 Cash Prize<br>
        🇦🇪 Sustainable Impact Challenge 2026
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# GUARD
# ─────────────────────────────────────────────────────────
def need_data():
    if st.session_state.df is None:
        st.markdown("""<div style='text-align:center;padding:70px 20px;'>
            <div style='font-size:3.5rem;margin-bottom:14px;'>📂</div>
            <div style='font-family:Syne,sans-serif;font-size:1.3rem;
                        font-weight:700;color:#003D52;'>No Data Uploaded Yet</div>
            <div style='font-size:0.9rem;color:#5A7A85;margin-top:8px;'>
                Go to <strong>Upload Water Data</strong> first.
            </div></div>""", unsafe_allow_html=True)
        return False
    return True

# ═════════════════════════════════════════════════════════
# PAGE: HOME
# ═════════════════════════════════════════════════════════
if page.startswith("🏠"):
    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-title'>💧 AquaSense UAE</div>
        <div class='hero-sub'>AI-Powered Water Impact Dashboard for Sustainable Campuses</div>
        <div class='badge-row'>
            <span class='badge'>🏆 RAK EISC 2026 — 3rd Place</span>
            <span class='badge'>🎖️ RAK Dept. of Knowledge</span>
            <span class='badge'>💰 AED 1,000 Prize</span>
            <span class='badge'>🇦🇪 Sustainable Impact Challenge 2026</span>
        </div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        stitle("📌", "About This Project")
        box("""<strong>AquaSense UAE</strong> is a smart water management system built for UAE 
        universities and buildings. It analyses water consumption data, detects potential leaks 
        through AI-powered anomaly detection, estimates the true cost of water waste in AED, 
        and generates actionable recommendations — creating <strong>measurable, sustainable 
        impact</strong> aligned with the UAE Net Zero 2050 strategy.""", "info")

        box("""🌍 <strong>Why Water in the UAE?</strong><br>
        The UAE has one of the highest per-capita water footprints on Earth. Over 
        <strong>90% of freshwater comes from energy-intensive desalination</strong>. 
        Every litre saved = less CO₂, less energy, lower cost. Smart water management 
        is not optional — it is a national priority.""", "success")

        stitle("⚙️", "What This Dashboard Does")
        features = [
            ("📂", "Upload campus water data (CSV or Excel)"),
            ("🔍", "Automatic data quality checks and validation"),
            ("📊", "Daily, monthly, and building-level trend charts"),
            ("🚨", "Statistical anomaly detection for leaks and spikes"),
            ("🌍", "Real environmental & financial waste impact in AED"),
            ("🤖", "AI-style building-specific recommendations"),
            ("📋", "Competition-ready impact report with CSV export"),
        ]
        for icon, text in features:
            st.markdown(f"""<div class='feature-row'>
                <span class='feature-icon'>{icon}</span>
                <span class='feature-text'>{text}</span>
            </div>""", unsafe_allow_html=True)

    with col2:
        stitle("🏆", "Awards & Recognition")
        awards = [
            ("🥉", "3rd Place", "RAK EISC 2026 Competition", "#F5A623"),
            ("🎖️", "Special Recognition", "RAK Department of Knowledge", "#0A7EA4"),
            ("💰", "AED 1,000", "Cash Prize Awarded", "#00C5A1"),
            ("🇦🇪", "Submitted To", "Sustainable Impact Challenge 2026", "#7C3AED"),
        ]
        for icon, title, sub, color in awards:
            st.markdown(f"""<div class='award-card' style='border-left:4px solid {color};'>
                <div style='font-size:1.5rem;'>{icon}</div>
                <div class='award-title'>{title}</div>
                <div class='award-sub'>{sub}</div>
            </div>""", unsafe_allow_html=True)

        stitle("📖", "How to Use")
        steps = [
            ("1", "Navigate to Competition Profile"),
            ("2", "Go to Upload Water Data"),
            ("3", "Work through each analysis section"),
            ("4", "Download the Final Impact Report"),
        ]
        for num, text in steps:
            st.markdown(f"""<div class='step-item'>
                <div class='step-num'>{num}</div>
                <div class='step-text'>{text}</div>
            </div>""", unsafe_allow_html=True)

    hr()
    stitle("📋", "Required Data Columns")
    cols_info = [
        ("📅", "Date", "Any standard date format"),
        ("🏢", "Building", "Building name or block ID"),
        ("💧", "Water_Usage_Liters", "Daily water consumption in litres"),
        ("💰", "Cost_AED", "Cost in UAE Dirhams"),
    ]
    c1, c2, c3, c4 = st.columns(4)
    for c, (icon, name, desc) in zip([c1, c2, c3, c4], cols_info):
        with c:
            st.markdown(mcard(icon, name, name, desc, "m-blue"), unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════
# PAGE: COMPETITION PROFILE
# ═════════════════════════════════════════════════════════
elif page.startswith("🏆"):
    st.markdown("""
    <div class='comp-hero'>
        <div class='comp-title'>🇦🇪 Sustainable Impact Challenge 2026</div>
        <div class='comp-sub'>How AquaSense UAE aligns with this national UAE government initiative</div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        stitle("🎯", "Competition Alignment")
        box("""The <strong>Sustainable Impact Challenge 2026</strong> is a UAE government-led 
        initiative that recognises projects creating <em>measurable social, environmental, 
        and economic impact</em>. AquaSense UAE directly addresses all three dimensions 
        through smart water management powered by AI and data analytics.""", "gold")

        stitle("✅", "How AquaSense UAE Meets Each Criteria")

        criteria = [
            ("🌱", "Environmental Impact",
             "Reduces water waste → less desalination energy → lower CO₂ emissions. "
             "Directly supports UAE Net Zero 2050 and SDG 6 (Clean Water).",
             "Measurable: CO₂ kg saved per year calculated"),
            ("💰", "Economic Impact",
             "Estimates AED losses from abnormal water usage. Projected yearly savings "
             "calculated per campus. ROI demonstrated for leak repairs and fixture upgrades.",
             "Measurable: AED saved per year projected"),
            ("🤝", "Social Impact",
             "Empowers students, facilities managers, and university administration with "
             "clear, actionable data — no data science expertise required.",
             "Measurable: Buildings monitored, abnormal days detected"),
            ("📊", "Innovation & AI",
             "Uses statistical anomaly detection (2σ rule) to flag water leaks automatically. "
             "AI-style recommendation engine tailored to each building's data pattern.",
             "Technology: Python, Streamlit, Plotly, Pandas, NumPy"),
            ("🏗️", "Scalability",
             "Works for any UAE campus or building with CSV/Excel data. Can be deployed "
             "at city-level with minimal modification. Institutional submission via university.",
             "Scalable: Any building, any UAE institution"),
        ]

        for icon, title, body, tag in criteria:
            st.markdown(f"""<div class='rec-card'>
                <div class='rec-icon'>{icon}</div>
                <div>
                    <div class='rec-title'>{title}</div>
                    <div class='rec-body'>{body}</div>
                    <div class='rec-tag'>✓ {tag}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    with col2:
        stitle("📅", "Competition Timeline")
        timeline = [
            ("📝", "Application Phase", "Until 25 May 2026", "Now open", "#00C5A1"),
            ("🗳️", "Public Voting", "June 2026", "Vote for our project!", "#0A7EA4"),
            ("⚖️", "Evaluation & Shortlisting", "After voting phase", "Judges review", "#7C3AED"),
            ("🏆", "Final Event & Winners", "October 2026", "Official UAE event", "#F5A623"),
        ]
        for icon, title, date, note, color in timeline:
            st.markdown(f"""<div class='timeline-item'>
                <div class='timeline-dot' style='background:{color};color:white;font-size:1rem;'>
                    {icon}
                </div>
                <div>
                    <div class='timeline-title'>{title}</div>
                    <div class='timeline-sub'>{date} · {note}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        hr()
        stitle("🌐", "SDG Alignment")
        sdgs = [
            ("SDG 6", "Clean Water & Sanitation", "#0A7EA4"),
            ("SDG 11", "Sustainable Cities", "#00C5A1"),
            ("SDG 13", "Climate Action", "#003D52"),
            ("SDG 17", "Partnerships for Goals", "#F5A623"),
        ]
        c_a, c_b = st.columns(2)
        for i, (num, label, color) in enumerate(sdgs):
            with (c_a if i % 2 == 0 else c_b):
                st.markdown(f"""<div class='sdg-card' style='background:{color};margin-bottom:10px;'>
                    <div class='sdg-num' style='color:white!important;'>{num}</div>
                    <div class='sdg-label'>{label}</div>
                </div>""", unsafe_allow_html=True)

        hr()
        stitle("📋", "Submission Format")
        box("""✅ Team of students developing the idea<br>
        ✅ Supervision by academic staff member<br>
        ✅ Official submission via university<br>
        ✅ Applied through UAE PASS (Digital Identity)<br>
        ✅ Projects must show measurable impact""", "success")

        stitle("🏅", "Prize Structure")
        box("""🥇 <strong>1st Place</strong> — Cash Prize + National Media<br>
        🥈 <strong>2nd Place</strong> — Cash Prize + Recognition<br>
        🥉 <strong>3rd Place</strong> — Cash Prize + Recognition<br>
        🎖️ Selected projects get national media exposure""", "gold")

    hr()
    stitle("📊", "Our Proven Track Record")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(mcard("🥉","Previous Award","3rd Place","RAK EISC 2026","m-warn"), unsafe_allow_html=True)
    with c2: st.markdown(mcard("🎖️","Recognition","Dept. of Knowledge","Official UAE body","m-blue"), unsafe_allow_html=True)
    with c3: st.markdown(mcard("💰","Cash Prize","AED 1,000","Already won","m-green"), unsafe_allow_html=True)
    with c4: st.markdown(mcard("🌍","SDGs Covered","4 Goals","Direct alignment","m-deep"), unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════
# PAGE: UPLOAD
# ═════════════════════════════════════════════════════════
elif page.startswith("📂"):
    st.markdown("""<div class='hero-banner' style='padding:36px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>📂 Upload Water Data</div>
        <div class='hero-sub'>Upload your campus water consumption file to begin analysis</div>
    </div>""", unsafe_allow_html=True)

    col_up, col_info = st.columns([2, 1], gap="large")

    with col_up:
        stitle("⬆️", "Upload Your File")
        uploaded = st.file_uploader(
            "Drag & drop or browse — CSV or Excel accepted",
            type=["csv","xlsx","xls"],
        )

        if uploaded:
            raw = load_file(uploaded.read(), uploaded.name)
            st.session_state.df_raw = raw

            REQUIRED = {"Date","Building","Water_Usage_Liters","Cost_AED"}
            missing  = REQUIRED - set(raw.columns)

            if missing:
                box(f"⚠️ Missing required columns: <strong>{', '.join(missing)}</strong>", "danger")
            else:
                df_p, avg, std, thr = process(raw)
                abn_cost = df_p[df_p["Is_Abnormal"]]["Cost_AED"].sum()
                st.session_state.df = df_p
                st.session_state.stats = dict(
                    avg=avg, std=std, thresh=thr,
                    total_usage=df_p["Water_Usage_Liters"].sum(),
                    total_cost=df_p["Cost_AED"].sum(),
                    total_waste=df_p["Wasted_Liters"].sum(),
                    n_abnormal=int(df_p["Is_Abnormal"].sum()),
                    n_rows=len(df_p),
                    abn_cost=abn_cost,
                )
                box("✅ <strong>File processed successfully!</strong> Navigate to any analysis section.", "success")

            st.markdown("#### 👀 Data Preview")
            st.dataframe(raw.head(10), use_container_width=True, height=260)

            ca, cb, cc = st.columns(3)
            with ca: st.markdown(mcard("📄","Total Rows",f"{len(raw):,}","","m-blue"), unsafe_allow_html=True)
            with cb: st.markdown(mcard("📐","Columns",str(len(raw.columns)),"","m-green"), unsafe_allow_html=True)
            with cc: st.markdown(mcard("💾","File Size",f"{uploaded.size/1024:.1f} KB","","m-deep"), unsafe_allow_html=True)
        else:
            st.markdown("""<div style='text-align:center;padding:60px;color:#5A7A85;'>
                <div style='font-size:3.5rem;margin-bottom:14px;'>📤</div>
                <div style='font-family:Syne,sans-serif;font-size:1.1rem;
                            font-weight:600;color:#003D52;'>No file uploaded yet</div>
                <div style='font-size:0.88rem;margin-top:8px;'>
                    Upload a CSV or Excel file to begin
                </div></div>""", unsafe_allow_html=True)

    with col_info:
        stitle("📋", "File Requirements")
        box("""<strong>Required Columns</strong><br><br>
        ✅ <code>Date</code> — Any date format<br>
        ✅ <code>Building</code> — Name or ID<br>
        ✅ <code>Water_Usage_Liters</code> — Numeric<br>
        ✅ <code>Cost_AED</code> — Numeric<br><br>
        <strong>Accepted Formats</strong><br><br>
        📄 <code>.csv</code> — Comma-separated<br>
        📊 <code>.xlsx</code> — Excel 2007+<br>
        📊 <code>.xls</code> — Excel Legacy""", "info")

        stitle("💡", "Sample Data")
        st.dataframe(pd.DataFrame([
            {"Date":"2024-01-15","Building":"Block A","Water_Usage_Liters":3200,"Cost_AED":16.5},
            {"Date":"2024-01-16","Building":"Block B","Water_Usage_Liters":4100,"Cost_AED":21.2},
        ]), use_container_width=True, hide_index=True)

# ═════════════════════════════════════════════════════════
# PAGE: DATA QUALITY CHECK
# ═════════════════════════════════════════════════════════
elif page.startswith("🔍"):
    st.markdown("""<div class='hero-banner' style='padding:36px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>🔍 Data Quality Check</div>
        <div class='hero-sub'>Validate your dataset before analysis</div>
    </div>""", unsafe_allow_html=True)

    if not need_data(): st.stop()
    df  = st.session_state.df
    raw = st.session_state.df_raw

    c1,c2,c3,c4 = st.columns(4)
    nulls = int(raw.isnull().sum().sum())
    dups  = int(raw.duplicated().sum())
    days  = (df["Date"].max()-df["Date"].min()).days
    with c1: st.markdown(mcard("📄","Total Records",f"{len(raw):,}","","m-blue"), unsafe_allow_html=True)
    with c2: st.markdown(mcard("🚫","Missing Values",str(nulls),"Clean ✅" if nulls==0 else "⚠️ Fix needed","m-green" if nulls==0 else "m-red"), unsafe_allow_html=True)
    with c3: st.markdown(mcard("🔁","Duplicates",str(dups),"None ✅" if dups==0 else "Found ⚠️","m-green" if dups==0 else "m-warn"), unsafe_allow_html=True)
    with c4: st.markdown(mcard("📅","Date Range",f"{days} days",f"{df['Date'].min().date()} → {df['Date'].max().date()}","m-deep"), unsafe_allow_html=True)

    hr()
    col1,col2 = st.columns(2)
    with col1:
        stitle("📋","Column Health Check")
        for col in ["Date","Building","Water_Usage_Liters","Cost_AED"]:
            if col in raw.columns:
                n = int(raw[col].isnull().sum())
                ok = n == 0
                st.markdown(f"""<div style='display:flex;justify-content:space-between;
                    align-items:center;padding:10px 14px;
                    background:{"#E4F9F4" if ok else "#FFF6E3"};
                    border-radius:10px;margin-bottom:8px;font-size:0.88rem;'>
                    <span style='font-weight:600;color:#003D52;'>{col}</span>
                    <span style='color:{"#007A60" if ok else "#B45309"};font-weight:600;'>
                        {"✅ OK" if ok else f"⚠️ {n} missing"}
                    </span></div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style='display:flex;justify-content:space-between;
                    align-items:center;padding:10px 14px;background:#FDECEA;
                    border-radius:10px;margin-bottom:8px;font-size:0.88rem;'>
                    <span style='font-weight:600;color:#003D52;'>{col}</span>
                    <span style='color:#C0392B;font-weight:600;'>❌ Missing column</span>
                </div>""", unsafe_allow_html=True)

    with col2:
        stitle("📈","Statistical Summary")
        st.dataframe(df[["Water_Usage_Liters","Cost_AED"]].describe().round(2),
                     use_container_width=True)

    hr()
    stitle("🏢","Records Per Building")
    bc = df.groupby("Building").size().reset_index(name="Records")
    fig = px.bar(bc, x="Building", y="Records",
                 color="Records", color_continuous_scale=["#6EC6E6","#003D52"],
                 title="Data Records per Building")
    st.plotly_chart(T(fig), use_container_width=True)
    st.dataframe(df[["Date","Building","Water_Usage_Liters","Cost_AED","Is_Abnormal"]],
                 use_container_width=True, height=280)

# ═════════════════════════════════════════════════════════
# PAGE: WATER USAGE DASHBOARD
# ═════════════════════════════════════════════════════════
elif page.startswith("📊"):
    st.markdown("""<div class='hero-banner' style='padding:36px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>📊 Water Usage Dashboard</div>
        <div class='hero-sub'>Campus-wide consumption trends and patterns</div>
    </div>""", unsafe_allow_html=True)

    if not need_data(): st.stop()
    df = st.session_state.df
    s  = st.session_state.stats

    c1,c2,c3,c4,c5 = st.columns(5)
    wp = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0
    with c1: st.markdown(mcard("💧","Total Water Used",fmt(s["total_usage"])+" L","","m-blue"), unsafe_allow_html=True)
    with c2: st.markdown(mcard("💰","Total Cost",f"AED {fmt(s['total_cost'])}","","m-green"), unsafe_allow_html=True)
    with c3: st.markdown(mcard("📏","Avg Daily Usage",fmt(s["avg"])+" L","Per day","m-deep"), unsafe_allow_html=True)
    with c4: st.markdown(mcard("🚨","Abnormal Days",str(s["n_abnormal"]),"Usage spikes","m-red"), unsafe_allow_html=True)
    with c5: st.markdown(mcard("🌊","Est. Wasted",fmt(s["total_waste"])+" L",f"{wp:.1f}% of total","m-warn"), unsafe_allow_html=True)

    hr()
    stitle("📈","Daily Water Usage Trend")
    daily = df.groupby("Date",as_index=False)["Water_Usage_Liters"].sum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily["Date"], y=daily["Water_Usage_Liters"],
        mode="lines", name="Daily Usage", line=dict(color="#0A7EA4",width=2.5),
        fill="tozeroy", fillcolor="rgba(10,126,164,0.07)"))
    fig.add_hline(y=s["avg"], line_dash="dot", line_color="#00C5A1",
                  annotation_text=f"Avg: {s['avg']:.0f} L", annotation_font_color="#007A60")
    fig.add_hline(y=s["thresh"], line_dash="dash", line_color="#E84855",
                  annotation_text="Anomaly Threshold", annotation_font_color="#E84855")
    T(fig); fig.update_layout(title="Daily Water Consumption — All Buildings",
                               xaxis_title="Date", yaxis_title="Litres")
    st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2)
    with col1:
        stitle("💸","Daily Cost (AED)")
        cd = df.groupby("Date",as_index=False)["Cost_AED"].sum()
        fig2 = px.area(cd, x="Date", y="Cost_AED", color_discrete_sequence=["#00C5A1"],
                       title="Daily Cost in AED")
        fig2.update_traces(fillcolor="rgba(0,197,161,0.1)")
        st.plotly_chart(T(fig2), use_container_width=True)

    with col2:
        stitle("📅","Usage by Day of Week")
        dow = df.groupby("Day_of_Week")["Water_Usage_Liters"].mean().reindex(
            ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        ).reset_index()
        dow.columns = ["Day","Avg"]
        fig3 = px.bar(dow, x="Day", y="Avg", color="Avg",
                      color_continuous_scale=["#6EC6E6","#003D52"],
                      title="Avg Usage by Day of Week")
        st.plotly_chart(T(fig3), use_container_width=True)

    stitle("🔵","Usage vs Cost Relationship")
    fig4 = px.scatter(df, x="Water_Usage_Liters", y="Cost_AED",
                      color="Building", size="Water_Usage_Liters",
                      hover_data=["Date","Building"],
                      title="Water Usage (L) vs Cost (AED) by Building",
                      color_discrete_sequence=COLORS)
    st.plotly_chart(T(fig4), use_container_width=True)

# ═════════════════════════════════════════════════════════
# PAGE: MONTHLY SUMMARY
# ═════════════════════════════════════════════════════════
elif page.startswith("📅"):
    st.markdown("""<div class='hero-banner' style='padding:36px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>📅 Monthly Water Summary</div>
        <div class='hero-sub'>Month-by-month consumption and cost breakdown</div>
    </div>""", unsafe_allow_html=True)

    if not need_data(): st.stop()
    df = st.session_state.df

    monthly = df.groupby("Month_Label").agg(
        Usage=("Water_Usage_Liters","sum"), Cost=("Cost_AED","sum"),
        Avg=("Water_Usage_Liters","mean"), Waste=("Wasted_Liters","sum"),
        Abn=("Is_Abnormal","sum")
    ).reset_index()

    fig = make_subplots(specs=[[{"secondary_y":True}]])
    fig.add_trace(go.Bar(x=monthly["Month_Label"], y=monthly["Usage"],
                         name="Usage (L)", marker_color="#0A7EA4"), secondary_y=False)
    fig.add_trace(go.Scatter(x=monthly["Month_Label"], y=monthly["Cost"],
                             name="Cost (AED)", mode="lines+markers",
                             line=dict(color="#00C5A1",width=3),
                             marker=dict(size=8)), secondary_y=True)
    fig.update_layout(title="Monthly Water Usage & Cost", **BASE_LAYOUT)
    fig.update_yaxes(title_text="Litres", secondary_y=False)
    fig.update_yaxes(title_text="AED", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2)
    with col1:
        fig2 = px.bar(monthly, x="Month_Label", y="Waste",
                      color="Waste", color_continuous_scale=["#FFFACD","#E84855"],
                      title="Estimated Wasted Water per Month (L)")
        st.plotly_chart(T(fig2), use_container_width=True)
    with col2:
        fig3 = px.line(monthly, x="Month_Label", y="Avg",
                       markers=True, title="Average Daily Usage per Month",
                       color_discrete_sequence=["#F5A623"])
        fig3.update_traces(line_width=3, marker_size=9)
        st.plotly_chart(T(fig3), use_container_width=True)

    stitle("📋","Monthly Summary Table")
    md = monthly.copy().round(1)
    md.columns = ["Month","Total (L)","Cost (AED)","Avg Daily (L)","Wasted (L)","Abnormal Days"]
    st.dataframe(md, use_container_width=True, hide_index=True)

# ═════════════════════════════════════════════════════════
# PAGE: BUILDING COMPARISON
# ═════════════════════════════════════════════════════════
elif page.startswith("🏢"):
    st.markdown("""<div class='hero-banner' style='padding:36px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>🏢 Building-wise Comparison</div>
        <div class='hero-sub'>Which buildings use the most — and waste the most</div>
    </div>""", unsafe_allow_html=True)

    if not need_data(): st.stop()
    df = st.session_state.df

    bld = df.groupby("Building").agg(
        Usage=("Water_Usage_Liters","sum"), Cost=("Cost_AED","sum"),
        Avg=("Water_Usage_Liters","mean"), Waste=("Wasted_Liters","sum"),
        Abn=("Is_Abnormal","sum"), N=("Water_Usage_Liters","count")
    ).reset_index().sort_values("Usage",ascending=False)

    col1,col2 = st.columns(2)
    with col1:
        fig = px.bar(bld, x="Building", y="Usage", color="Usage",
                     color_continuous_scale=["#6EC6E6","#003D52"],
                     title="Total Water Usage by Building (L)", text="Usage")
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", textfont_size=10)
        st.plotly_chart(T(fig), use_container_width=True)
    with col2:
        fig2 = px.pie(bld, values="Usage", names="Building",
                      color_discrete_sequence=COLORS, hole=0.44,
                      title="Share of Total Water Usage")
        fig2.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(T(fig2), use_container_width=True)

    stitle("💧","Average Daily Usage vs Waste by Building")
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=bld["Building"],y=bld["Avg"],name="Avg Daily",marker_color="#0A7EA4"))
    fig3.add_trace(go.Bar(x=bld["Building"],y=bld["Waste"],name="Est. Wasted",marker_color="#E84855"))
    fig3.update_layout(barmode="group",title="Avg Daily Usage vs Estimated Waste",**BASE_LAYOUT)
    st.plotly_chart(fig3, use_container_width=True)

    col3,col4 = st.columns(2)
    with col3:
        fig4 = px.bar(bld.sort_values("Waste"),x="Waste",y="Building",
                      orientation="h",color="Waste",
                      color_continuous_scale=["#FFF3CC","#E84855"],
                      title="Wasted Water by Building (L)")
        st.plotly_chart(T(fig4), use_container_width=True)
    with col4:
        fig5 = px.scatter(bld,x="Avg",y="Cost",size="Usage",color="Building",
                          title="Avg Daily Usage vs Total Cost",
                          color_discrete_sequence=COLORS,hover_data=["Abn"])
        st.plotly_chart(T(fig5), use_container_width=True)

    stitle("📋","Building Summary Table")
    bd = bld.round(1)
    bd.columns=["Building","Total (L)","Cost (AED)","Avg Daily (L)","Wasted (L)","Abnormal Days","Records"]
    st.dataframe(bd, use_container_width=True, hide_index=True)

# ═════════════════════════════════════════════════════════
# PAGE: ABNORMAL DETECTION
# ═════════════════════════════════════════════════════════
elif page.startswith("🚨"):
    st.markdown("""<div class='hero-banner' style='padding:36px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>🚨 Abnormal Usage / Leak Detection</div>
        <div class='hero-sub'>Statistical AI anomaly detection to flag potential leaks</div>
    </div>""", unsafe_allow_html=True)

    if not need_data(): st.stop()
    df = st.session_state.df
    s  = st.session_state.stats

    box(f"""<strong>Detection Method — 2 Standard Deviation Rule:</strong> Any day where 
    water usage exceeds <em>Campus Average + 2× Std Dev</em> is flagged as abnormal. 
    This may indicate a <strong>leak, broken valve, or unusual consumption event</strong>.<br><br>
    📏 Average: <strong>{s['avg']:,.1f} L/day</strong> &nbsp;|&nbsp; 
    📊 Std Dev: <strong>{s['std']:,.1f} L</strong> &nbsp;|&nbsp; 
    🚨 Threshold: <strong>{s['thresh']:,.1f} L/day</strong>""", "info")

    abn = df[df["Is_Abnormal"]]
    c1,c2,c3,c4 = st.columns(4)
    pct = s["n_abnormal"]/s["n_rows"]*100 if s["n_rows"] else 0
    with c1: st.markdown(mcard("🚨","Abnormal Days",str(s["n_abnormal"]),f"of {s['n_rows']} records","m-red"), unsafe_allow_html=True)
    with c2: st.markdown(mcard("📊","Abnormal Rate",f"{pct:.1f}%","Of total data","m-warn"), unsafe_allow_html=True)
    with c3: st.markdown(mcard("💧","Est. Wasted",fmt(s["total_waste"])+" L","From anomaly days","m-blue"), unsafe_allow_html=True)
    with c4: st.markdown(mcard("💰","AED Loss",f"AED {fmt(s['abn_cost'])}","From anomaly days","m-deep"), unsafe_allow_html=True)

    hr()
    stitle("📈","Usage Trend with Anomaly Markers")
    daily = df.groupby("Date").agg(U=("Water_Usage_Liters","sum"),A=("Is_Abnormal","any")).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily["Date"],y=daily["U"],mode="lines",name="Daily Usage",
        line=dict(color="#0A7EA4",width=2.5),fill="tozeroy",fillcolor="rgba(10,126,164,0.07)"))
    ad = daily[daily["A"]]
    fig.add_trace(go.Scatter(x=ad["Date"],y=ad["U"],mode="markers",name="⚠️ Abnormal",
        marker=dict(color="#E84855",size=13,symbol="circle",line=dict(color="white",width=2))))
    fig.add_hline(y=s["thresh"],line_dash="dash",line_color="#E84855",
                  annotation_text=f"Threshold: {s['thresh']:,.0f} L",annotation_font_color="#E84855")
    fig.add_hline(y=s["avg"],line_dash="dot",line_color="#00C5A1",
                  annotation_text=f"Average: {s['avg']:,.0f} L",annotation_font_color="#007A60")
    T(fig); fig.update_layout(title="Daily Usage with Anomalies Highlighted",xaxis_title="Date",yaxis_title="Litres")
    st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2)
    with col1:
        stitle("🏢","Abnormal Days by Building")
        ab = df.groupby("Building")["Is_Abnormal"].sum().reset_index()
        ab.columns = ["Building","Abnormal"]
        ab = ab[ab["Abnormal"]>0].sort_values("Abnormal",ascending=False)
        if len(ab):
            fig2=px.bar(ab,x="Building",y="Abnormal",color="Abnormal",
                        color_continuous_scale=["#FFD166","#E84855"],
                        title="Abnormal Days per Building")
            st.plotly_chart(T(fig2), use_container_width=True)
        else:
            box("✅ No buildings with critical abnormal usage.", "success")

    with col2:
        stitle("📦","Usage Distribution")
        fig3=go.Figure()
        fig3.add_trace(go.Histogram(x=df["Water_Usage_Liters"],nbinsx=30,
                                    marker_color="#0A7EA4",opacity=0.75,name="Usage"))
        fig3.add_vline(x=s["avg"],line_dash="dot",line_color="#00C5A1",annotation_text="Average")
        fig3.add_vline(x=s["thresh"],line_dash="dash",line_color="#E84855",annotation_text="Threshold")
        T(fig3); fig3.update_layout(title="Distribution of Daily Water Usage",
                                     xaxis_title="Litres",yaxis_title="Frequency")
        st.plotly_chart(fig3, use_container_width=True)

    stitle("📋","Flagged Abnormal Records")
    if len(abn):
        ad2 = abn[["Date","Building","Water_Usage_Liters","Cost_AED","Wasted_Liters"]].copy()
        ad2.columns = ["Date","Building","Usage (L)","Cost (AED)","Wasted (L)"]
        st.dataframe(ad2.round(2).sort_values("Wasted (L)",ascending=False),
                     use_container_width=True, hide_index=True)
    else:
        box("✅ No abnormal records found in this dataset.", "success")

# ═════════════════════════════════════════════════════════
# PAGE: IMPACT CALCULATOR
# ═════════════════════════════════════════════════════════
elif page.startswith("🌍"):
    st.markdown("""<div class='hero-banner' style='padding:36px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>🌍 Water Impact Calculator</div>
        <div class='hero-sub'>Real environmental and financial cost of water waste</div>
    </div>""", unsafe_allow_html=True)

    if not need_data(): st.stop()
    df = st.session_state.df
    s  = st.session_state.stats

    days    = (df["Date"].max()-df["Date"].min()).days+1
    y_waste = (s["total_waste"]/days)*365
    y_save  = y_waste*0.5
    y_aed   = (s["abn_cost"]/days)*365*0.5
    co2     = y_save*0.000344
    kwh     = y_save*0.004
    bottles = y_save*2
    trees   = y_save*0.05/1000
    wp      = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0

    stitle("📊","Current Waste Metrics")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(mcard("💧","Water Wasted",fmt(s["total_waste"])+" L","From anomalies","m-red"), unsafe_allow_html=True)
    with c2: st.markdown(mcard("📊","Waste %",f"{wp:.1f}%","Of total usage","m-warn"), unsafe_allow_html=True)
    with c3: st.markdown(mcard("💰","AED Loss",f"AED {fmt(s['abn_cost'])}","Anomaly cost","m-blue"), unsafe_allow_html=True)
    with c4: st.markdown(mcard("📅","Data Period",f"{days} days",f"{df['Date'].min().date()}","m-deep"), unsafe_allow_html=True)

    hr()
    stitle("🌱","Projected Yearly Savings — 50% Waste Reduction")
    box("""These projections show what is achievable if abnormal water usage is reduced by 
    <strong>50%</strong> through leak repairs and smarter behaviour — a realistic, 
    <strong>measurable target</strong> for this competition.""", "gold")

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(mcard("💧","Water Saved/Year",fmt(y_save)+" L","50% of yearly waste","m-green"), unsafe_allow_html=True)
    with c2: st.markdown(mcard("💰","AED Saved/Year",f"AED {fmt(y_aed)}","Projected saving","m-blue"), unsafe_allow_html=True)
    with c3: st.markdown(mcard("🌿","CO₂ Avoided",f"{co2:,.1f} kg","Less desalination","m-deep"), unsafe_allow_html=True)
    with c4: st.markdown(mcard("⚡","Energy Saved",f"{kwh:,.1f} kWh","Desal energy cut","m-warn"), unsafe_allow_html=True)

    c5,c6,_,_ = st.columns(4)
    with c5: st.markdown(mcard("🍶","Plastic Bottles",fmt(bottles),"500ml equivalents","m-red"), unsafe_allow_html=True)
    with c6: st.markdown(mcard("🌳","Trees Equiv.",f"{trees:,.0f}","CO₂ offset equiv.","m-green"), unsafe_allow_html=True)

    hr()
    col1,col2 = st.columns(2)
    with col1:
        pie = pd.DataFrame({"Category":["Normal Usage","Estimated Waste"],
                            "Litres":[s["total_usage"]-s["total_waste"],s["total_waste"]]})
        fig=px.pie(pie,values="Litres",names="Category",
                   color_discrete_sequence=["#0A7EA4","#E84855"],hole=0.5,
                   title="Normal vs Wasted Water")
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(T(fig), use_container_width=True)
    with col2:
        fig2=go.Figure(go.Waterfall(
            orientation="v", measure=["relative","relative","relative","total"],
            x=["Total Waste","50% Reduction","Remaining","Net Saving"],
            y=[y_waste,-y_save,y_save,0],
            connector={"line":{"color":"#D0E8F0"}},
            increasing={"marker":{"color":"#E84855"}},
            decreasing={"marker":{"color":"#00C5A1"}},
            totals={"marker":{"color":"#0A7EA4"}},
        ))
        T(fig2); fig2.update_layout(title="Yearly Waste & Saving Waterfall (L)")
        st.plotly_chart(fig2, use_container_width=True)

    hr()
    stitle("🎛️","Custom Reduction Scenario")
    pct = st.slider("Select waste reduction target (%)", 10, 90, 50, 5)
    cs  = y_waste*(pct/100)
    ca  = y_aed*(pct/50)
    cc  = cs*0.000344
    c1,c2,c3 = st.columns(3)
    with c1: st.markdown(mcard("💧",f"Saved at {pct}%",fmt(cs)+" L/yr","","m-blue"), unsafe_allow_html=True)
    with c2: st.markdown(mcard("💰","AED Saved",f"AED {fmt(ca)}/yr","","m-green"), unsafe_allow_html=True)
    with c3: st.markdown(mcard("🌿","CO₂ Avoided",f"{cc:,.2f} kg/yr","","m-deep"), unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════
# PAGE: RECOMMENDATIONS
# ═════════════════════════════════════════════════════════
elif page.startswith("🤖"):
    st.markdown("""<div class='hero-banner' style='padding:36px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>🤖 AI-Style Recommendations</div>
        <div class='hero-sub'>Data-driven actions tailored to your campus patterns</div>
    </div>""", unsafe_allow_html=True)

    if not need_data(): st.stop()
    df = st.session_state.df
    s  = st.session_state.stats
    wp = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0

    box(f"""⚠️ <strong>Waste Alert:</strong> Your campus wastes an estimated 
    <strong>{wp:.1f}%</strong> of its water through abnormal usage events. 
    <strong>{s['n_abnormal']}</strong> anomaly days detected. 
    The recommendations below are generated from your specific data patterns.""", "danger")

    ba = df.groupby("Building").agg(A=("Is_Abnormal","sum"),W=("Wasted_Liters","sum")).reset_index()
    top = ba[ba["A"]>0].sort_values("A",ascending=False)["Building"].tolist()

    if top:
        stitle("🏢","Building-Specific Alerts")
        for bld in top[:5]:
            r = ba[ba["Building"]==bld].iloc[0]
            box(f"""🚨 <strong>{bld}</strong> — {int(r['A'])} abnormal day(s) detected · 
            Estimated <strong>{r['W']:,.0f} L</strong> wasted. 
            <strong>Immediate inspection recommended.</strong>""", "danger")

    hr()
    stitle("💡","Smart Recommendations")

    RECS = [
        ("🔧","Fix Leaks Immediately",
         f"Your data flagged {s['n_abnormal']} abnormal usage days. Even a small "
         "dripping tap wastes 10,000+ L/year. Full plumbing inspection recommended for all flagged buildings.",
         "30–50% waste reduction"),
        ("📱","Install Smart Water Meters",
         "IoT-enabled meters provide real-time alerts when usage exceeds thresholds — "
         "automating exactly what this dashboard detects, running 24/7 without manual uploads.",
         "Instant leak detection"),
        ("🚿","Upgrade to Low-Flow Fixtures",
         "Replacing standard taps and toilets with low-flow equivalents cuts consumption "
         "by 30–50% with no change in user behaviour. Prioritise highest-usage buildings first.",
         "30–45% per fixture"),
        ("🌿","Greywater Recycling System",
         "Reuse sink and shower water for toilet flushing and irrigation. UAE campuses with "
         "greywater systems report up to 40% reduction in potable water demand.",
         "Up to 40% potable saving"),
        ("👥","Student Awareness Campaign",
         "Monthly sustainability challenges at UAE universities have achieved 15–25% "
         "consumption reductions within 3 months through student and staff engagement.",
         "15–25% usage reduction"),
        ("🗓️","Quarterly Plumbing Audits",
         "Preventive maintenance is 10× cheaper than emergency repairs. Scheduled audits "
         "eliminate slow leaks that are invisible without data — like this dashboard provides.",
         "60–80% fewer anomaly days"),
        ("☀️","Solar Water Heating",
         "Switching to solar heaters aligns with UAE Net Zero 2050. Combined with insulated "
         "pipes, this eliminates heat-loss waste and cuts energy bills significantly.",
         "20% energy + water saving"),
        ("🌱","Drought-Resistant Landscaping",
         "UAE-native plants with drip irrigation cut landscape water use dramatically. "
         "Irrigation accounts for up to 50% of campus water in summer months.",
         "Up to 50% irrigation saving"),
    ]

    for icon,title,body,saving in RECS:
        st.markdown(f"""<div class='rec-card'>
            <div class='rec-icon'>{icon}</div>
            <div>
                <div class='rec-title'>{title}</div>
                <div class='rec-body'>{body}</div>
                <div class='rec-tag'>💚 {saving}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    hr()
    stitle("📊","Priority Matrix — Impact vs Ease")
    pri = pd.DataFrame({
        "Action":["Fix Leaks","Smart Meters","Low-Flow Fixtures","Greywater System","Awareness Campaign"],
        "Impact":[95,85,75,70,55], "Ease":[80,50,70,35,90], "Cost_K_AED":[5,80,40,150,2],
    })
    fig=px.scatter(pri,x="Ease",y="Impact",size="Cost_K_AED",text="Action",color="Impact",
                   color_continuous_scale=["#6EC6E6","#003D52"],
                   title="Priority Matrix: Impact vs Ease of Implementation",
                   labels={"Ease":"← Harder    Ease of Implementation    Easier →",
                            "Impact":"Lower    Impact Score    Higher ↑"})
    fig.update_traces(textposition="top center")
    st.plotly_chart(T(fig), use_container_width=True)

# ═════════════════════════════════════════════════════════
# PAGE: FINAL REPORT
# ═════════════════════════════════════════════════════════
elif page.startswith("📋"):
    st.markdown("""<div class='hero-banner' style='padding:36px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>📋 Final Impact Report Summary</div>
        <div class='hero-sub'>Competition-ready summary for Sustainable Impact Challenge 2026</div>
    </div>""", unsafe_allow_html=True)

    if not need_data(): st.stop()
    df = st.session_state.df
    s  = st.session_state.stats

    days    = (df["Date"].max()-df["Date"].min()).days+1
    y_waste = (s["total_waste"]/days)*365
    y_save  = y_waste*0.5
    y_aed   = (s["abn_cost"]/days)*365*0.5
    co2     = y_save*0.000344
    wp      = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0
    bld_n   = df["Building"].nunique()

    # Hero report card
    st.markdown(f"""<div class='report-card'>
        <div style='font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;
                    color:#FFFFFF;margin-bottom:6px;'>
            🏆 AquaSense UAE — Campus Water Impact Report
        </div>
        <div style='color:rgba(255,255,255,0.75);font-size:0.86rem;margin-bottom:26px;'>
            Generated: {datetime.now().strftime("%d %B %Y, %H:%M")} &nbsp;|&nbsp; 
            Period: {df['Date'].min().date()} → {df['Date'].max().date()} &nbsp;|&nbsp; 
            Buildings: {bld_n} &nbsp;|&nbsp; 
            Submitted to: Sustainable Impact Challenge 2026
        </div>
        <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:16px;'>
            <div style='text-align:center;'>
                <div class='report-val'>{fmt(s['total_usage'])} L</div>
                <div class='report-lbl'>Total Water Consumed</div>
            </div>
            <div style='text-align:center;'>
                <div class='report-val'>AED {fmt(s['total_cost'])}</div>
                <div class='report-lbl'>Total Cost</div>
            </div>
            <div style='text-align:center;'>
                <div class='report-val'>{s['n_abnormal']}</div>
                <div class='report-lbl'>Anomaly Days Detected</div>
            </div>
            <div style='text-align:center;'>
                <div class='report-val'>{wp:.1f}%</div>
                <div class='report-lbl'>Est. Water Wasted</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    stitle("🌱","Projected Yearly Savings — 50% Waste Reduction")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(mcard("💧","Water Saved/Year",fmt(y_save)+" L","","m-green"), unsafe_allow_html=True)
    with c2: st.markdown(mcard("💰","AED Saved/Year",f"AED {fmt(y_aed)}","","m-blue"), unsafe_allow_html=True)
    with c3: st.markdown(mcard("🌿","CO₂ Avoided",f"{co2:,.1f} kg","","m-deep"), unsafe_allow_html=True)
    with c4: st.markdown(mcard("🏢","Buildings",str(bld_n),"Analysed","m-warn"), unsafe_allow_html=True)

    hr()
    col1,col2 = st.columns(2)
    with col1:
        stitle("📊","Usage vs Waste")
        pie=pd.DataFrame({"Cat":["Normal","Wasted"],"V":[s["total_usage"]-s["total_waste"],s["total_waste"]]})
        fig=px.pie(pie,values="V",names="Cat",color_discrete_sequence=["#0A7EA4","#E84855"],
                   hole=0.5,title="Normal vs Wasted Water")
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(T(fig), use_container_width=True)
    with col2:
        stitle("🏢","Building Share")
        bs=df.groupby("Building")["Water_Usage_Liters"].sum().reset_index()
        fig2=px.pie(bs,values="Water_Usage_Liters",names="Building",
                    color_discrete_sequence=COLORS,hole=0.5,title="Usage by Building")
        fig2.update_traces(textinfo="percent+label")
        st.plotly_chart(T(fig2), use_container_width=True)

    stitle("📅","Monthly Trend")
    mn=df.groupby("Month_Label")["Water_Usage_Liters"].sum().reset_index()
    fig3=px.bar(mn,x="Month_Label",y="Water_Usage_Liters",color="Water_Usage_Liters",
                color_continuous_scale=["#6EC6E6","#003D52"],title="Monthly Total Water Usage (L)")
    st.plotly_chart(T(fig3), use_container_width=True)

    hr()
    stitle("📝","Key Findings")
    findings = [
        f"🏫 Campus consumed **{s['total_usage']:,.0f} L** total over {days} days — avg **AED {s['total_cost']/days:,.2f}/day**.",
        f"🚨 **{s['n_abnormal']} anomaly events** detected (2σ threshold: {s['thresh']:,.0f} L/day).",
        f"🌊 Estimated **{s['total_waste']:,.0f} L wasted** ({wp:.1f}% of total) through abnormal events.",
        f"💰 AED loss from anomalies: **AED {s['abn_cost']:,.2f}** over the analysis period.",
        f"🌱 **50% waste reduction** would save **{y_save:,.0f} L/year** and **AED {y_aed:,.2f}/year**.",
        f"🌿 This prevents approximately **{co2:,.2f} kg CO₂/year** from desalination — supporting UAE Net Zero 2050.",
        f"🏢 **{bld_n} buildings** analysed — targeted interventions in top waste buildings offer the highest ROI.",
    ]
    for f in findings:
        st.markdown(f)

    hr()
    stitle("🏆","Top 3 Priority Actions")
    top3=[
        ("1","🔧","Immediate Leak Inspection",
         f"Inspect all {s['n_abnormal']} flagged anomaly days. Even a small leak costs thousands of AED/year."),
        ("2","📱","Deploy Smart Water Meters",
         "Automate what this dashboard does manually — 24/7 real-time anomaly alerts per building."),
        ("3","🚿","Low-Flow Fixture Upgrade",
         "Upgrade top-usage buildings first. ROI within 12–18 months under UAE conditions."),
    ]
    for num,icon,title,body in top3:
        st.markdown(f"""<div class='rec-card'>
            <div style='width:44px;height:44px;border-radius:13px;flex-shrink:0;
                        background:linear-gradient(135deg,#003D52,#0A7EA4);color:white;
                        font-family:Syne,sans-serif;font-weight:800;font-size:1.2rem;
                        display:flex;align-items:center;justify-content:center;'>{num}</div>
            <div>
                <div class='rec-title'>{icon} {title}</div>
                <div class='rec-body'>{body}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    hr()
    stitle("⬇️","Export Data")
    exp = df[["Date","Building","Water_Usage_Liters","Cost_AED","Is_Abnormal","Wasted_Liters"]].copy()
    exp.columns=["Date","Building","Water_Usage_L","Cost_AED","Is_Abnormal","Wasted_L"]
    summ = pd.DataFrame({
        "Metric":["Total Usage (L)","Total Cost (AED)","Period (days)","Buildings",
                  "Avg Daily (L)","Anomaly Days","Wasted (L)","Waste %",
                  "Yearly Waste (L)","Yearly Saving 50% (L)","AED Saving/Year","CO2 Avoided (kg/yr)"],
        "Value":[f"{s['total_usage']:,.1f}",f"{s['total_cost']:,.2f}",str(days),str(bld_n),
                 f"{s['avg']:,.1f}",str(s['n_abnormal']),f"{s['total_waste']:,.1f}",f"{wp:.2f}%",
                 f"{y_waste:,.1f}",f"{y_save:,.1f}",f"{y_aed:,.2f}",f"{co2:,.4f}"]
    })
    col_a,col_b,_ = st.columns([1,1,2])
    with col_a:
        st.download_button("📥 Full Dataset (CSV)",
            exp.to_csv(index=False).encode("utf-8"),
            "aquasense_data.csv","text/csv",use_container_width=True)
    with col_b:
        st.download_button("📊 Summary Report (CSV)",
            summ.to_csv(index=False).encode("utf-8"),
            "aquasense_summary.csv","text/csv",use_container_width=True)

# ─────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────
st.markdown("""<div class='footer'>
    💧 <strong>AquaSense UAE</strong> — AI-Powered Water Impact Dashboard for Sustainable Campuses<br>
    🏆 RAK EISC 2026 · Third Place &nbsp;|&nbsp; 🎖️ RAK Department of Knowledge Recognition 
    &nbsp;|&nbsp; 💰 AED 1,000 Cash Prize &nbsp;|&nbsp; 🇦🇪 Submitted: Sustainable Impact Challenge 2026<br>
    <span style='color:#B0C8D0;font-size:0.74rem;'>
        Built with Streamlit · Plotly · Pandas · NumPy &nbsp;|&nbsp; 
        Aligned with UAE Net Zero 2050 · SDG 6 · SDG 11 · SDG 13
    </span>
</div>""", unsafe_allow_html=True)
