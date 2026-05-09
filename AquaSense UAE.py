"""
AquaSense UAE — AI-Powered Water Impact Dashboard
Dark theme · Full-screen · Multi-dataset management
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io, json
from datetime import datetime

# ── Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="AquaSense UAE",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════
# DESIGN SYSTEM — DARK THEME
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

/* ── RESET ALL STREAMLIT CHROME TO DARK ── */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
[data-testid="stMain"],
.main .block-container,
[data-testid="stVerticalBlock"],
section.main { background: #080D1A !important; }

.main .block-container {
    padding: 0 2rem 3rem 2rem !important;
    max-width: 100% !important;
}

/* kill default Streamlit top padding/space */
[data-testid="stHeader"] { background: transparent !important; height: 0 !important; }
[data-testid="stDecoration"] { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0C1220 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: #0C1220 !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
[data-testid="stSidebar"] .stRadio > label { display: none !important; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    gap: 2px !important; display: flex; flex-direction: column;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.875rem !important;
    color: #8B9BB4 !important;
    padding: 8px 16px !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    margin: 1px 8px !important;
    border: 1px solid transparent !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: rgba(0,212,255,0.06) !important;
    color: #E2E8F0 !important;
    border-color: rgba(0,212,255,0.15) !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-baseweb="radio"] { display: none !important; }
/* hide radio circles */
[data-testid="stSidebar"] .stRadio input { display: none !important; }
[data-testid="stSidebar"] .stRadio span[data-testid="stMarkdownContainer"] p { margin: 0 !important; }
/* selected radio */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked),
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[aria-checked="true"] {
    background: rgba(0,212,255,0.10) !important;
    color: #00D4FF !important;
    border-color: rgba(0,212,255,0.25) !important;
    font-weight: 600 !important;
}

/* ── GLOBAL TEXT ── */
h1,h2,h3,h4,h5,h6 {
    font-family: 'Syne', sans-serif !important;
    color: #F0F6FF !important;
}
p, span, div, label, li {
    font-family: 'Inter', sans-serif !important;
    color: #CBD5E1 !important;
}
code { color: #00D4FF !important; background: rgba(0,212,255,0.1) !important; border-radius: 4px; padding: 1px 5px; }

/* ── PLOTLY MODEBAR ── */
.modebar { background: transparent !important; }
.modebar-btn svg { fill: #8B9BB4 !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0C1220; }
::-webkit-scrollbar-thumb { background: #2D3748; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #00D4FF; }

/* ── STREAMLIT WIDGET OVERRIDES ── */
[data-testid="stFileUploader"] {
    background: #0F1623 !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"] section {
    background: #111827 !important;
    border: 2px dashed rgba(0,212,255,0.3) !important;
    border-radius: 12px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"] section:hover { border-color: rgba(0,212,255,0.6) !important; }
[data-testid="stFileUploader"] * { color: #8B9BB4 !important; }

[data-testid="stDataFrame"] { background: #0F1623 !important; border-radius: 12px !important; }
[data-testid="stDataFrame"] * { color: #CBD5E1 !important; }
.dvn-scroller { background: #0F1623 !important; }

div[data-testid="stSlider"] { padding: 8px 0 !important; }
div[data-testid="stSlider"] * { color: #CBD5E1 !important; }
div[data-testid="stSlider"] [data-testid="stMarkdownContainer"] p { color: #CBD5E1 !important; }
.stSlider > div > div > div > div { background: #00D4FF !important; }
.stSlider [data-baseweb="slider"] div:first-child { background: #1E2740 !important; }

.stSelectbox > div { background: #111827 !important; border: 1px solid #2D3748 !important; border-radius: 8px !important; }
.stSelectbox * { color: #CBD5E1 !important; }

.stTextInput input { background: #111827 !important; border: 1px solid #2D3748 !important; color: #F0F6FF !important; border-radius: 8px !important; font-family: 'Inter' !important; }
.stTextInput input:focus { border-color: #00D4FF !important; box-shadow: 0 0 0 3px rgba(0,212,255,0.12) !important; }

button[kind="primary"], .stButton > button {
    background: linear-gradient(135deg, #00D4FF, #0066CC) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 8px 16px !important;
    transition: opacity 0.2s, transform 0.15s !important;
}
button[kind="primary"]:hover, .stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }

.stDownloadButton button {
    background: rgba(0,255,157,0.1) !important;
    color: #00FF9D !important;
    border: 1px solid rgba(0,255,157,0.3) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
    transition: all 0.2s !important;
}
.stDownloadButton button:hover { background: rgba(0,255,157,0.18) !important; }

.stProgress > div > div > div { background: linear-gradient(90deg,#00D4FF,#00FF9D) !important; }

[data-testid="stMetric"] { background: #0F1623 !important; }
[data-testid="stMetric"] * { color: #CBD5E1 !important; }

hr { border-color: rgba(255,255,255,0.07) !important; }

div[data-testid="column"] { gap: 0 !important; }

/* ══════════════════════════════════════
   CUSTOM COMPONENTS
══════════════════════════════════════ */

/* ── Top Bar ── */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 20px 0 16px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 28px;
}
.topbar-title { font-family:'Syne',sans-serif; font-size:1.5rem; font-weight:800; color:#F0F6FF; }
.topbar-sub   { font-size:0.8rem; color:#8B9BB4; margin-top:2px; font-family:'Inter',sans-serif; }
.topbar-right { display:flex; gap:10px; align-items:center; }

/* ── Stat Cards ── */
.scard {
    background: #0F1623;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 20px 22px;
    position: relative; overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
}
.scard:hover { border-color: rgba(0,212,255,0.25); transform: translateY(-2px); }
.scard::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    border-radius: 16px 16px 0 0;
}
.scard-blue::before   { background: linear-gradient(90deg,#00D4FF,transparent); }
.scard-green::before  { background: linear-gradient(90deg,#00FF9D,transparent); }
.scard-red::before    { background: linear-gradient(90deg,#FF4757,transparent); }
.scard-yellow::before { background: linear-gradient(90deg,#FFD166,transparent); }
.scard-purple::before { background: linear-gradient(90deg,#A78BFA,transparent); }

.scard-icon   { font-size: 1.5rem; margin-bottom: 10px; }
.scard-label  { font-size: 0.7rem; color: #4A5568; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; font-weight: 600; font-family:'Inter',sans-serif; }
.scard-value  { font-family:'Syne',sans-serif; font-size: 1.7rem; font-weight: 800; color: #F0F6FF; line-height: 1; }
.scard-delta  { font-size: 0.75rem; color: #8B9BB4; margin-top: 6px; font-family:'Inter',sans-serif; }
.scard-blue   .scard-value { color: #00D4FF; }
.scard-green  .scard-value { color: #00FF9D; }
.scard-red    .scard-value { color: #FF4757; }
.scard-yellow .scard-value { color: #FFD166; }
.scard-purple .scard-value { color: #A78BFA; }

/* ── Chart container ── */
.chart-wrap {
    background: #0F1623; border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 20px; margin-bottom: 16px;
    overflow: hidden;
}
.chart-title { font-family:'Syne',sans-serif; font-size:0.95rem; font-weight:700; color:#E2E8F0; margin-bottom:14px; }

/* ── Info boxes ── */
.ibox { border-radius:12px; padding:14px 16px; margin:10px 0; font-size:0.875rem; font-family:'Inter',sans-serif; line-height:1.6; }
.ibox b, .ibox strong { font-weight:700; }
.ibox-info    { background:rgba(0,212,255,0.08);  border-left:3px solid #00D4FF;  color:#A8D8EA; }
.ibox-success { background:rgba(0,255,157,0.08);  border-left:3px solid #00FF9D;  color:#7FEBB8; }
.ibox-warn    { background:rgba(255,209,102,0.08); border-left:3px solid #FFD166;  color:#FFD166; }
.ibox-danger  { background:rgba(255,71,87,0.08);   border-left:3px solid #FF4757;  color:#FF8591; }

/* ── Section title ── */
.sec-title {
    display:flex; align-items:center; gap:10px;
    font-family:'Syne',sans-serif; font-size:1.15rem; font-weight:700;
    color:#E2E8F0; margin:24px 0 14px;
}
.sec-dot { width:8px; height:8px; border-radius:50%; background:#00D4FF; flex-shrink:0; }

/* ── Divider ── */
.vdivider { height:1px; background:rgba(255,255,255,0.06); margin:24px 0; border:none; }

/* ── Hero banner (page header) ── */
.page-header {
    background: linear-gradient(135deg, rgba(0,212,255,0.08) 0%, rgba(0,255,157,0.04) 100%);
    border: 1px solid rgba(0,212,255,0.12);
    border-radius: 16px; padding: 28px 32px; margin-bottom: 24px;
    position: relative; overflow: hidden;
}
.page-header::after {
    content:''; position:absolute; top:-40px; right:-40px;
    width:200px; height:200px; border-radius:50%;
    background: radial-gradient(circle, rgba(0,212,255,0.06) 0%, transparent 70%);
}
.page-header-title { font-family:'Syne',sans-serif; font-size:1.6rem; font-weight:800; color:#F0F6FF; margin:0 0 4px; }
.page-header-sub   { font-size:0.875rem; color:#8B9BB4; font-family:'Inter',sans-serif; }

/* ── Dataset chip ── */
.ds-chip {
    display:inline-flex; align-items:center; gap:8px;
    background:#111827; border:1px solid #2D3748;
    border-radius:8px; padding:8px 12px; margin:4px;
    font-family:'Inter',sans-serif; font-size:0.8rem; color:#CBD5E1;
    cursor:pointer; transition:all 0.15s;
}
.ds-chip:hover { border-color:#00D4FF; color:#00D4FF; }
.ds-chip.active { background:rgba(0,212,255,0.1); border-color:#00D4FF; color:#00D4FF; font-weight:600; }
.ds-chip-del { color:#FF4757; margin-left:4px; font-weight:700; cursor:pointer; }

/* ── Rec card ── */
.rec-card {
    background:#0F1623; border:1px solid rgba(255,255,255,0.07);
    border-radius:14px; padding:18px 20px; margin-bottom:12px;
    display:flex; gap:14px; align-items:flex-start;
    transition:border-color 0.2s;
}
.rec-card:hover { border-color:rgba(0,212,255,0.2); }
.rec-icon-box {
    width:42px; height:42px; border-radius:11px; flex-shrink:0;
    background:rgba(0,212,255,0.1); border:1px solid rgba(0,212,255,0.2);
    display:flex; align-items:center; justify-content:center; font-size:1.2rem;
}
.rec-title { font-family:'Syne',sans-serif; font-size:0.92rem; font-weight:700; color:#E2E8F0; margin-bottom:4px; }
.rec-body  { font-size:0.82rem; color:#8B9BB4; line-height:1.55; font-family:'Inter',sans-serif; }
.rec-tag   {
    display:inline-block; background:rgba(0,255,157,0.08);
    color:#00FF9D; border-radius:20px; padding:2px 10px;
    font-size:0.72rem; font-weight:700; margin-top:6px;
    font-family:'Inter',sans-serif; border:1px solid rgba(0,255,157,0.2);
}

/* ── Report card ── */
.report-card {
    background: linear-gradient(135deg, #0F1A2E 0%, #0C1B33 50%, #0F2040 100%);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 20px; padding: 32px 36px; margin-bottom: 20px;
    position: relative; overflow: hidden;
}
.report-card::before {
    content:''; position:absolute; bottom:-60px; right:-60px;
    width:240px; height:240px; border-radius:50%;
    background: radial-gradient(circle, rgba(0,212,255,0.07) 0%, transparent 70%);
}
.rval { font-family:'Syne',sans-serif; font-size:2rem; font-weight:800; color:#00D4FF; }
.rlbl { font-size:0.77rem; color:rgba(255,255,255,0.5); margin-top:3px; font-family:'Inter',sans-serif; }

/* ── Health row ── */
.health-row {
    display:flex; justify-content:space-between; align-items:center;
    padding:10px 14px;
    border-radius:10px; margin-bottom:8px;
}
.health-label { font-weight:600; color:#E2E8F0; font-family:'Inter',sans-serif; font-size:0.875rem; }
.health-ok   { background:rgba(0,255,157,0.06); border:1px solid rgba(0,255,157,0.12); }
.health-warn { background:rgba(255,209,102,0.06); border:1px solid rgba(255,209,102,0.12); }
.health-bad  { background:rgba(255,71,87,0.06); border:1px solid rgba(255,71,87,0.12); }
.tag-ok   { color:#00FF9D; font-size:0.8rem; font-weight:600; font-family:'Inter',sans-serif; }
.tag-warn { color:#FFD166; font-size:0.8rem; font-weight:600; font-family:'Inter',sans-serif; }
.tag-bad  { color:#FF4757; font-size:0.8rem; font-weight:600; font-family:'Inter',sans-serif; }

/* ── Step row ── */
.step-row {
    display:flex; align-items:center; gap:12px;
    padding:10px 12px; background:#0F1623;
    border:1px solid rgba(255,255,255,0.06);
    border-radius:10px; margin-bottom:7px;
}
.step-num {
    width:28px; height:28px; border-radius:50%; flex-shrink:0;
    background:rgba(0,212,255,0.12); border:1px solid rgba(0,212,255,0.3);
    color:#00D4FF; font-family:'Syne',sans-serif; font-weight:800; font-size:0.8rem;
    display:flex; align-items:center; justify-content:center;
}
.step-text { font-size:0.84rem; color:#8B9BB4; font-family:'Inter',sans-serif; }

/* ── Sidebar logo block ── */
.sb-logo {
    padding: 24px 16px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 8px;
}
.sb-logo-icon { font-size:2rem; }
.sb-logo-name { font-family:'Syne',sans-serif; font-size:1.05rem; font-weight:800; color:#F0F6FF; margin-top:6px; }
.sb-logo-sub  { font-size:0.63rem; color:#4A5568; letter-spacing:1.5px; text-transform:uppercase; margin-top:2px; }

.sb-section { padding:12px 16px 4px; font-size:0.65rem; color:#4A5568; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; font-family:'Inter',sans-serif; }

/* ── Dataset manager in sidebar ── */
.ds-item {
    display:flex; align-items:center; justify-content:space-between;
    padding:8px 12px; margin:3px 8px;
    border-radius:8px; border:1px solid rgba(255,255,255,0.05);
    background:rgba(255,255,255,0.02);
    font-family:'Inter',sans-serif; font-size:0.8rem;
    transition: all 0.15s;
}
.ds-item.active-ds {
    background:rgba(0,212,255,0.08); border-color:rgba(0,212,255,0.2);
}
.ds-name { color:#CBD5E1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:130px; }
.ds-active-tag { font-size:0.62rem; color:#00D4FF; background:rgba(0,212,255,0.1); padding:1px 7px; border-radius:10px; border:1px solid rgba(0,212,255,0.2); }

/* ── Priority matrix labels ── */
.pm-quad-label { font-size:0.7rem; color:#4A5568; font-family:'Inter',sans-serif; }

/* ── Empty state ── */
.empty-state {
    text-align:center; padding:80px 20px;
    background:#0F1623; border:1px dashed rgba(255,255,255,0.08);
    border-radius:20px; margin:20px 0;
}
.empty-icon  { font-size:3rem; margin-bottom:14px; }
.empty-title { font-family:'Syne',sans-serif; font-size:1.2rem; font-weight:700; color:#4A5568; }
.empty-sub   { font-size:0.875rem; color:#2D3748; margin-top:6px; font-family:'Inter',sans-serif; }

/* ── Footer ── */
.app-footer {
    text-align:center; padding:20px;
    border-top:1px solid rgba(255,255,255,0.06);
    margin-top:40px; font-family:'Inter',sans-serif;
    font-size:0.75rem; color:#4A5568;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PLOTLY DARK THEME
# ══════════════════════════════════════════════════════════
_COLORS = ["#00D4FF","#00FF9D","#A78BFA","#FFD166","#FF4757",
           "#38BDF8","#34D399","#818CF8","#FBBF24","#F87171"]

_DARK_LAYOUT = dict(
    font=dict(family="Inter", color="#8B9BB4"),
    plot_bgcolor="#0F1623", paper_bgcolor="#0F1623",
    margin=dict(l=20, r=20, t=40, b=20),
    colorway=_COLORS,
    title_font=dict(family="Syne", size=14, color="#E2E8F0"),
    legend=dict(bgcolor="rgba(0,0,0,0)", font_color="#8B9BB4", bordercolor="rgba(255,255,255,0.06)"),
    xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.08)",
               tickfont_color="#4A5568", title_font_color="#8B9BB4", zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.08)",
               tickfont_color="#4A5568", title_font_color="#8B9BB4", zeroline=False),
)

def T(fig, secondary_y=False):
    fig.update_layout(**_DARK_LAYOUT)
    if not secondary_y:
        fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.04)",
                         linecolor="rgba(255,255,255,0.08)", tickfont_color="#4A5568", zeroline=False)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.04)",
                         linecolor="rgba(255,255,255,0.08)", tickfont_color="#4A5568", zeroline=False)
    return fig

_SEQ_BLUE  = [[0,"#0C1220"],[0.5,"#0A4D6E"],[1,"#00D4FF"]]
_SEQ_GREEN = [[0,"#0C1220"],[0.5,"#064E3B"],[1,"#00FF9D"]]
_SEQ_RED   = [[0,"#0C1220"],[0.5,"#7F1D1D"],[1,"#FF4757"]]

# ══════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════
def fmt(n, d=0):
    if abs(n) >= 1_000_000: return f"{n/1_000_000:.2f}M"
    if abs(n) >= 1_000:     return f"{n/1_000:.1f}K"
    return f"{n:,.{d}f}"

def scard(icon, label, value, delta="", cls="scard-blue"):
    dh = f"<div class='scard-delta'>{delta}</div>" if delta else ""
    return f"""<div class='scard {cls}'>
        <div class='scard-icon'>{icon}</div>
        <div class='scard-label'>{label}</div>
        <div class='scard-value'>{value}</div>{dh}
    </div>"""

def sec(icon, text):
    st.markdown(f"""<div class='sec-title'>
        <span class='sec-dot'></span>{icon}&nbsp;{text}
    </div>""", unsafe_allow_html=True)

def ibox(content, kind="info"):
    st.markdown(f"<div class='ibox ibox-{kind}'>{content}</div>", unsafe_allow_html=True)

def vdiv():
    st.markdown("<hr class='vdivider'>", unsafe_allow_html=True)

def page_header(title, subtitle=""):
    st.markdown(f"""<div class='page-header'>
        <div class='page-header-title'>{title}</div>
        {"<div class='page-header-sub'>" + subtitle + "</div>" if subtitle else ""}
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# DATA PROCESSING
# ══════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def load_bytes(b, name):
    return pd.read_csv(io.BytesIO(b)) if name.lower().endswith(".csv") else pd.read_excel(io.BytesIO(b))

def compute_stats(raw):
    df = raw.copy()
    df["Date"]               = pd.to_datetime(df["Date"], errors="coerce")
    df["Water_Usage_Liters"] = pd.to_numeric(df["Water_Usage_Liters"], errors="coerce")
    df["Cost_AED"]           = pd.to_numeric(df["Cost_AED"], errors="coerce")
    df = df.dropna(subset=["Date","Water_Usage_Liters","Cost_AED"]).sort_values("Date").reset_index(drop=True)
    if len(df) == 0:
        return None, None, None, None
    avg = df["Water_Usage_Liters"].mean()
    std = df["Water_Usage_Liters"].std(ddof=1) if len(df) > 1 else 0.0
    thr = avg + 2 * std
    df["Is_Abnormal"]   = df["Water_Usage_Liters"] > thr
    df["Wasted_Liters"] = np.where(df["Is_Abnormal"], df["Water_Usage_Liters"] - avg, 0)
    df["Month_Label"]   = df["Date"].dt.strftime("%b %Y")
    df["Day_of_Week"]   = df["Date"].dt.day_name()
    abn_cost            = df[df["Is_Abnormal"]]["Cost_AED"].sum()
    stats = dict(
        avg=avg, std=std, thresh=thr,
        total_usage=df["Water_Usage_Liters"].sum(),
        total_cost=df["Cost_AED"].sum(),
        total_waste=df["Wasted_Liters"].sum(),
        n_abnormal=int(df["Is_Abnormal"].sum()),
        n_rows=len(df), abn_cost=abn_cost,
    )
    return df, avg, std, stats

# ══════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════
if "datasets"       not in st.session_state: st.session_state.datasets       = {}   # {name: {raw, df, stats}}
if "active_ds"      not in st.session_state: st.session_state.active_ds      = None
if "confirm_delete" not in st.session_state: st.session_state.confirm_delete = None

REQUIRED = {"Date","Building","Water_Usage_Liters","Cost_AED"}

def get_active():
    k = st.session_state.active_ds
    if k and k in st.session_state.datasets:
        return st.session_state.datasets[k]
    return None

# ══════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════
with st.sidebar:

    # Logo
    st.markdown("""<div class='sb-logo'>
        <div class='sb-logo-icon'>💧</div>
        <div class='sb-logo-name'>AquaSense UAE</div>
        <div class='sb-logo-sub'>Smart Water Dashboard</div>
    </div>""", unsafe_allow_html=True)

    # Navigation
    st.markdown("<div class='sb-section'>Navigation</div>", unsafe_allow_html=True)
    PAGES = [
        "🏠  Overview",
        "📊  Water Usage Dashboard",
        "📅  Monthly Summary",
        "🏢  Building Comparison",
        "🚨  Leak Detection",
        "🌍  Impact Calculator",
        "🤖  Recommendations",
        "📋  Impact Report",
    ]
    page = st.radio("nav", PAGES, label_visibility="collapsed")

    st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:14px 0;'>", unsafe_allow_html=True)

    # ── Dataset Manager ────────────────────────────────
    st.markdown("<div class='sb-section'>📁 My Datasets</div>", unsafe_allow_html=True)

    upload_new = st.file_uploader(
        "Add dataset", type=["csv","xlsx","xls"],
        label_visibility="collapsed", key="sidebar_uploader"
    )

    if upload_new is not None:
        with st.spinner("Processing…"):
            raw = load_bytes(upload_new.read(), upload_new.name)
        missing = REQUIRED - set(raw.columns)
        if missing:
            st.error(f"Missing: {', '.join(missing)}", icon="⚠️")
        else:
            df_p, avg, std, stats = compute_stats(raw)
            if df_p is not None:
                ds_name = upload_new.name
                # Deduplicate name
                base = ds_name
                i = 2
                while ds_name in st.session_state.datasets:
                    ds_name = f"{base} ({i})"; i += 1
                st.session_state.datasets[ds_name] = {"raw": raw, "df": df_p, "stats": stats, "name": ds_name, "uploaded": datetime.now().strftime("%d %b %Y")}
                st.session_state.active_ds = ds_name
                st.rerun()

    # List datasets
    if st.session_state.datasets:
        for ds_name, ds in list(st.session_state.datasets.items()):
            is_active = ds_name == st.session_state.active_ds
            c_sel, c_del = st.columns([5,1])
            with c_sel:
                if st.button(
                    f"{'● ' if is_active else '○ '}{ds_name[:22]}{'…' if len(ds_name)>22 else ''}",
                    key=f"sel_{ds_name}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary",
                ):
                    st.session_state.active_ds = ds_name
                    st.rerun()
            with c_del:
                if st.button("✕", key=f"del_{ds_name}", help=f"Delete {ds_name}"):
                    st.session_state.confirm_delete = ds_name
                    st.rerun()

        # Confirm delete
        if st.session_state.confirm_delete:
            dn = st.session_state.confirm_delete
            st.warning(f"Delete **{dn}**?", icon="🗑️")
            ca, cb = st.columns(2)
            with ca:
                if st.button("Yes, delete", key="confirm_yes", type="primary"):
                    del st.session_state.datasets[dn]
                    if st.session_state.active_ds == dn:
                        remaining = list(st.session_state.datasets.keys())
                        st.session_state.active_ds = remaining[0] if remaining else None
                    st.session_state.confirm_delete = None
                    st.rerun()
            with cb:
                if st.button("Cancel", key="confirm_no"):
                    st.session_state.confirm_delete = None
                    st.rerun()

        # Clear all
        st.markdown("<div style='margin-top:8px;'>", unsafe_allow_html=True)
        if st.button("🗑️ Clear all datasets", use_container_width=True, key="clear_all"):
            st.session_state.datasets = {}
            st.session_state.active_ds = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("""<div style='padding:14px 8px;text-align:center;color:#4A5568;font-size:0.8rem;font-family:Inter,sans-serif;'>
            No datasets yet.<br>Upload a file above ↑
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ACTIVE DATASET SHORTCUT
# ══════════════════════════════════════════════════════════
active = get_active()
df     = active["df"]    if active else None
stats  = active["stats"] if active else None

def need_data():
    if active is None:
        st.markdown("""<div class='empty-state'>
            <div class='empty-icon'>📂</div>
            <div class='empty-title'>No dataset loaded</div>
            <div class='empty-sub'>Upload a CSV or Excel file using the sidebar panel on the left.</div>
        </div>""", unsafe_allow_html=True)
        return False
    return True

# ══════════════════════════════════════════════════════════
# DOWNLOAD HELPERS
# ══════════════════════════════════════════════════════════
def get_export_csv(df):
    exp = df[["Date","Building","Water_Usage_Liters","Cost_AED","Is_Abnormal","Wasted_Liters"]].copy()
    exp.columns = ["Date","Building","Water_Usage_L","Cost_AED","Is_Abnormal","Wasted_L"]
    return exp.to_csv(index=False).encode("utf-8")

def get_summary_csv(stats, df):
    days  = (df["Date"].max()-df["Date"].min()).days + 1
    wp    = stats["total_waste"]/stats["total_usage"]*100 if stats["total_usage"] else 0
    yw    = (stats["total_waste"]/days)*365
    ys    = yw*0.5
    ya    = (stats["abn_cost"]/days)*365*0.5
    co2   = ys*0.000344
    bld_n = df["Building"].nunique()
    rows  = {
        "Metric": ["Total Usage (L)","Total Cost (AED)","Period (days)","Buildings",
                   "Avg Daily (L)","Anomaly Days","Wasted (L)","Waste %",
                   "Projected Yearly Waste (L)","Saving at 50% (L)","AED Saving/Year","CO₂ Avoided (kg/yr)"],
        "Value":  [f"{stats['total_usage']:,.1f}", f"{stats['total_cost']:,.2f}", str(days), str(bld_n),
                   f"{stats['avg']:,.1f}", str(stats['n_abnormal']), f"{stats['total_waste']:,.1f}", f"{wp:.2f}%",
                   f"{yw:,.1f}", f"{ys:,.1f}", f"{ya:,.2f}", f"{co2:,.4f}"]
    }
    return pd.DataFrame(rows).to_csv(index=False).encode("utf-8")

# ══════════════════════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════════════════════

# ── OVERVIEW ────────────────────────────────────────────
if page.startswith("🏠"):
    st.markdown("""<div class='topbar'>
        <div>
            <div class='topbar-title'>💧 AquaSense UAE</div>
            <div class='topbar-sub'>AI-Powered Water Impact Dashboard for Sustainable Campuses</div>
        </div>
    </div>""", unsafe_allow_html=True)

    if active:
        # Quick stats bar
        s = stats
        wp = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0
        c1,c2,c3,c4,c5 = st.columns(5)
        with c1: st.markdown(scard("💧","Total Water Used",fmt(s["total_usage"])+" L","","scard-blue"), unsafe_allow_html=True)
        with c2: st.markdown(scard("💰","Total Cost (AED)",f"AED {fmt(s['total_cost'])}","","scard-green"), unsafe_allow_html=True)
        with c3: st.markdown(scard("📏","Daily Average",fmt(s["avg"])+" L","Per day","scard-purple"), unsafe_allow_html=True)
        with c4: st.markdown(scard("🚨","Anomaly Days",str(s["n_abnormal"]),f"of {s['n_rows']} records","scard-red"), unsafe_allow_html=True)
        with c5: st.markdown(scard("🌊","Est. Wasted",fmt(s["total_waste"])+" L",f"{wp:.1f}% of total","scard-yellow"), unsafe_allow_html=True)

        vdiv()

        col1, col2 = st.columns([2,1], gap="large")
        with col1:
            # Daily trend mini
            sec("📈","Daily Consumption Overview")
            daily = df.groupby("Date",as_index=False)["Water_Usage_Liters"].sum()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=daily["Date"],y=daily["Water_Usage_Liters"],
                mode="lines",name="Usage",line=dict(color="#00D4FF",width=2),
                fill="tozeroy",fillcolor="rgba(0,212,255,0.05)"))
            fig.add_hline(y=s["thresh"],line_dash="dash",line_color="#FF4757",
                          annotation_text="Threshold",annotation_font=dict(color="#FF4757",size=10))
            T(fig); fig.update_layout(height=300,showlegend=False,
                                      xaxis_title="",yaxis_title="Litres")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            sec("🏢","Buildings Overview")
            bsum = df.groupby("Building").agg(
                Usage=("Water_Usage_Liters","sum"), Abn=("Is_Abnormal","sum")).reset_index()
            bsum = bsum.sort_values("Usage",ascending=False)
            for _, row in bsum.iterrows():
                pct_use = row["Usage"]/s["total_usage"]*100 if s["total_usage"] else 0
                abn_flag = "🔴" if row["Abn"] > 0 else "🟢"
                st.markdown(f"""<div style='display:flex;align-items:center;gap:10px;
                    padding:9px 12px;background:#0F1623;border:1px solid rgba(255,255,255,0.06);
                    border-radius:10px;margin-bottom:6px;'>
                    <span style='font-size:0.85rem;'>{abn_flag}</span>
                    <div style='flex:1;'>
                        <div style='font-size:0.82rem;color:#E2E8F0;font-weight:600;font-family:Inter,sans-serif;'>{row["Building"]}</div>
                        <div style='height:4px;background:rgba(255,255,255,0.06);border-radius:2px;margin-top:5px;'>
                            <div style='height:4px;background:#00D4FF;border-radius:2px;width:{pct_use:.0f}%;'></div>
                        </div>
                    </div>
                    <div style='text-align:right;'>
                        <div style='font-size:0.8rem;color:#00D4FF;font-weight:700;font-family:Inter,sans-serif;'>{pct_use:.0f}%</div>
                        <div style='font-size:0.7rem;color:#4A5568;font-family:Inter,sans-serif;'>{int(row["Abn"])} anomalies</div>
                    </div>
                </div>""", unsafe_allow_html=True)

        vdiv()

        col3,col4 = st.columns(2, gap="large")
        with col3:
            sec("🗓️","Monthly Trend")
            mn = df.groupby("Month_Label")["Water_Usage_Liters"].sum().reset_index()
            fig2 = px.bar(mn,x="Month_Label",y="Water_Usage_Liters",
                          color="Water_Usage_Liters",color_continuous_scale=_SEQ_BLUE)
            T(fig2); fig2.update_layout(height=250,showlegend=False,coloraxis_showscale=False,
                                        xaxis_title="",yaxis_title="Litres",
                                        title="")
            st.plotly_chart(fig2, use_container_width=True)

        with col4:
            sec("🥧","Waste Breakdown")
            pie_d = pd.DataFrame({"Cat":["Normal","Wasted"],
                                   "V":[s["total_usage"]-s["total_waste"],s["total_waste"]]})
            fig3 = px.pie(pie_d,values="V",names="Cat",hole=0.62,
                          color="Cat",color_discrete_map={"Normal":"#00D4FF","Wasted":"#FF4757"})
            fig3.update_traces(textinfo="percent+label",textfont_color="#E2E8F0",
                               marker_line=dict(color="#0F1623",width=2))
            T(fig3); fig3.update_layout(height=250,showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)

    else:
        # Welcome screen
        st.markdown("""<div style='padding:60px 0;'>""", unsafe_allow_html=True)
        c_l, c_r = st.columns([2,1], gap="large")
        with c_l:
            st.markdown("""<div class='page-header' style='padding:36px 38px;'>
                <div class='page-header-title' style='font-size:2rem;'>💧 AquaSense UAE</div>
                <div class='page-header-sub' style='font-size:1rem;margin-top:8px;line-height:1.7;'>
                    AI-powered water management for UAE campuses.<br>
                    Upload your consumption data and instantly detect leaks,<br>
                    quantify waste, and generate actionable recommendations.
                </div>
            </div>""", unsafe_allow_html=True)

            for icon, text in [
                ("📂","Upload CSV or Excel water consumption data"),
                ("🔍","Automated data quality validation"),
                ("📊","Interactive consumption charts and trends"),
                ("🚨","Statistical anomaly detection for leaks"),
                ("🌍","Real AED and CO₂ impact calculations"),
                ("🤖","Building-specific recommendations"),
                ("📋","Exportable full impact report"),
            ]:
                st.markdown(f"""<div style='display:flex;gap:12px;align-items:center;
                    padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.04);'>
                    <span style='font-size:1rem;'>{icon}</span>
                    <span style='font-size:0.875rem;color:#8B9BB4;font-family:Inter,sans-serif;'>{text}</span>
                </div>""", unsafe_allow_html=True)

        with c_r:
            sec("📖","How to start")
            for num, text in [("1","Upload a file using the sidebar"),
                               ("2","Click the file name to activate it"),
                               ("3","Navigate through analysis sections"),
                               ("4","Export your impact report")]:
                st.markdown(f"""<div class='step-row'>
                    <div class='step-num'>{num}</div>
                    <div class='step-text'>{text}</div>
                </div>""", unsafe_allow_html=True)

            sec("📋","Required columns")
            for col, desc in [("Date","Standard date format"),("Building","Name or ID"),
                               ("Water_Usage_Liters","Litres (numeric)"),("Cost_AED","AED (numeric)")]:
                st.markdown(f"""<div style='display:flex;justify-content:space-between;
                    padding:7px 12px;background:#0F1623;border:1px solid rgba(255,255,255,0.05);
                    border-radius:8px;margin-bottom:5px;'>
                    <code style='font-size:0.78rem;'>{col}</code>
                    <span style='font-size:0.76rem;color:#4A5568;font-family:Inter,sans-serif;'>{desc}</span>
                </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ── WATER USAGE DASHBOARD ────────────────────────────────
elif page.startswith("📊"):
    page_header("📊 Water Usage Dashboard","Campus-wide consumption trends and patterns")
    if not need_data(): st.stop()
    s = stats

    wp = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(scard("💧","Total Used",fmt(s["total_usage"])+" L","","scard-blue"), unsafe_allow_html=True)
    with c2: st.markdown(scard("💰","Total Cost",f"AED {fmt(s['total_cost'])}","","scard-green"), unsafe_allow_html=True)
    with c3: st.markdown(scard("📏","Daily Avg",fmt(s["avg"])+" L","Per day","scard-purple"), unsafe_allow_html=True)
    with c4: st.markdown(scard("🚨","Anomaly Days",str(s["n_abnormal"]),"Spikes flagged","scard-red"), unsafe_allow_html=True)
    with c5: st.markdown(scard("🌊","Est. Wasted",fmt(s["total_waste"])+" L",f"{wp:.1f}% of total","scard-yellow"), unsafe_allow_html=True)

    vdiv()

    # Daily trend
    daily = df.groupby("Date",as_index=False)["Water_Usage_Liters"].sum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily["Date"],y=daily["Water_Usage_Liters"],
        mode="lines",name="Daily Usage",line=dict(color="#00D4FF",width=2),
        fill="tozeroy",fillcolor="rgba(0,212,255,0.05)",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Usage: %{y:,.0f} L<extra></extra>"))
    fig.add_hline(y=s["avg"],line_dash="dot",line_color="#00FF9D",
                  annotation_text=f"Avg {s['avg']:,.0f} L",annotation_font=dict(color="#00FF9D",size=10))
    fig.add_hline(y=s["thresh"],line_dash="dash",line_color="#FF4757",
                  annotation_text="Anomaly Threshold",annotation_font=dict(color="#FF4757",size=10))
    T(fig); fig.update_layout(height=320,title="Daily Water Consumption — All Buildings",
                               xaxis_title="",yaxis_title="Litres",showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2, gap="large")
    with col1:
        sec("💸","Daily Cost Trend")
        cd = df.groupby("Date",as_index=False)["Cost_AED"].sum()
        fig2 = px.area(cd,x="Date",y="Cost_AED",color_discrete_sequence=["#00FF9D"])
        fig2.update_traces(fillcolor="rgba(0,255,157,0.05)",line_width=1.5,
                           hovertemplate="<b>%{x|%d %b}</b><br>AED %{y:,.2f}<extra></extra>")
        T(fig2); fig2.update_layout(height=260,xaxis_title="",yaxis_title="AED",showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        sec("📅","Average by Day of Week")
        dow = df.groupby("Day_of_Week")["Water_Usage_Liters"].mean().reindex(
            ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]).reset_index()
        dow.columns = ["Day","Avg"]
        fig3 = px.bar(dow,x="Day",y="Avg",color="Avg",color_continuous_scale=_SEQ_BLUE)
        fig3.update_traces(hovertemplate="<b>%{x}</b><br>%{y:,.0f} L<extra></extra>")
        T(fig3); fig3.update_layout(height=260,showlegend=False,coloraxis_showscale=False,
                                    xaxis_title="",yaxis_title="Avg Litres")
        st.plotly_chart(fig3, use_container_width=True)

    sec("🔵","Usage vs Cost Relationship")
    fig4 = px.scatter(df,x="Water_Usage_Liters",y="Cost_AED",color="Building",
                      size="Water_Usage_Liters",size_max=18,
                      hover_data={"Date":"|%d %b %Y","Building":True,"Water_Usage_Liters":":.0f","Cost_AED":":.2f"},
                      color_discrete_sequence=_COLORS)
    T(fig4); fig4.update_layout(height=340,xaxis_title="Water Usage (L)",yaxis_title="Cost (AED)")
    st.plotly_chart(fig4, use_container_width=True)

    # Export row
    vdiv()
    c_dl1, c_dl2, _ = st.columns([1,1,4])
    with c_dl1: st.download_button("📥 Export Data (CSV)", get_export_csv(df), "aquasense_data.csv","text/csv",use_container_width=True)
    with c_dl2: st.download_button("📊 Export Summary (CSV)", get_summary_csv(stats,df), "aquasense_summary.csv","text/csv",use_container_width=True)

# ── MONTHLY SUMMARY ──────────────────────────────────────
elif page.startswith("📅"):
    page_header("📅 Monthly Water Summary","Month-by-month consumption and cost breakdown")
    if not need_data(): st.stop()

    monthly = df.groupby("Month_Label").agg(
        Usage=("Water_Usage_Liters","sum"), Cost=("Cost_AED","sum"),
        Avg=("Water_Usage_Liters","mean"), Waste=("Wasted_Liters","sum"), Abn=("Is_Abnormal","sum")
    ).reset_index()

    fig = make_subplots(specs=[[{"secondary_y":True}]])
    fig.add_trace(go.Bar(x=monthly["Month_Label"],y=monthly["Usage"],name="Usage (L)",
                         marker_color="#00D4FF",marker_opacity=0.85,
                         hovertemplate="<b>%{x}</b><br>Usage: %{y:,.0f} L<extra></extra>"),secondary_y=False)
    fig.add_trace(go.Scatter(x=monthly["Month_Label"],y=monthly["Cost"],name="Cost (AED)",
                             mode="lines+markers",line=dict(color="#00FF9D",width=2.5),
                             marker=dict(size=8,color="#00FF9D"),
                             hovertemplate="<b>%{x}</b><br>AED %{y:,.2f}<extra></extra>"),secondary_y=True)
    fig.update_layout(height=340,barmode="group",**_DARK_LAYOUT,
                      title="Monthly Water Usage & Cost",legend=dict(orientation="h",y=1.1))
    fig.update_yaxes(title_text="Litres",secondary_y=False,gridcolor="rgba(255,255,255,0.04)",tickfont_color="#4A5568")
    fig.update_yaxes(title_text="AED",secondary_y=True,gridcolor="rgba(255,255,255,0.04)",tickfont_color="#4A5568")
    fig.update_xaxes(tickfont_color="#4A5568")
    st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2, gap="large")
    with col1:
        fig2 = px.bar(monthly,x="Month_Label",y="Waste",color="Waste",
                      color_continuous_scale=_SEQ_RED,title="Estimated Wasted Water per Month (L)")
        fig2.update_traces(hovertemplate="<b>%{x}</b><br>Wasted: %{y:,.0f} L<extra></extra>")
        T(fig2); fig2.update_layout(height=260,coloraxis_showscale=False,xaxis_title="",yaxis_title="Litres")
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        fig3 = px.line(monthly,x="Month_Label",y="Avg",markers=True,
                       color_discrete_sequence=["#A78BFA"],title="Average Daily Usage per Month (L)")
        fig3.update_traces(line_width=2.5,marker_size=9,
                           hovertemplate="<b>%{x}</b><br>Avg: %{y:,.0f} L<extra></extra>")
        T(fig3); fig3.update_layout(height=260,xaxis_title="",yaxis_title="Litres")
        st.plotly_chart(fig3, use_container_width=True)

    sec("📋","Monthly Table")
    md = monthly.copy().round(1)
    md.columns = ["Month","Total (L)","Cost (AED)","Avg Daily (L)","Wasted (L)","Anomaly Days"]
    st.dataframe(md, use_container_width=True, hide_index=True, height=300)

    vdiv()
    c1,_,_,_ = st.columns(4)
    with c1: st.download_button("📥 Export Monthly Data", monthly.to_csv(index=False).encode("utf-8"), "monthly_summary.csv","text/csv",use_container_width=True)

# ── BUILDING COMPARISON ──────────────────────────────────
elif page.startswith("🏢"):
    page_header("🏢 Building Comparison","Which buildings consume and waste the most")
    if not need_data(): st.stop()

    bld = df.groupby("Building").agg(
        Usage=("Water_Usage_Liters","sum"), Cost=("Cost_AED","sum"),
        Avg=("Water_Usage_Liters","mean"), Waste=("Wasted_Liters","sum"),
        Abn=("Is_Abnormal","sum"), N=("Water_Usage_Liters","count")
    ).reset_index().sort_values("Usage",ascending=False)

    col1,col2 = st.columns(2, gap="large")
    with col1:
        fig = px.bar(bld,x="Building",y="Usage",color="Usage",color_continuous_scale=_SEQ_BLUE,
                     title="Total Water Usage by Building (L)",text="Usage")
        fig.update_traces(texttemplate="%{text:,.0f}",textposition="outside",
                          textfont=dict(color="#8B9BB4",size=10))
        T(fig); fig.update_layout(height=300,coloraxis_showscale=False,xaxis_title="",yaxis_title="Litres")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.pie(bld,values="Usage",names="Building",hole=0.58,
                      title="Share of Total Usage",color_discrete_sequence=_COLORS)
        fig2.update_traces(textposition="inside",textinfo="percent+label",
                           textfont=dict(color="#E2E8F0"),
                           marker=dict(line=dict(color="#0F1623",width=2)))
        T(fig2); fig2.update_layout(height=300,showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    sec("💧","Avg Daily Usage vs Estimated Waste")
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=bld["Building"],y=bld["Avg"],name="Avg Daily",marker_color="#00D4FF",marker_opacity=0.85))
    fig3.add_trace(go.Bar(x=bld["Building"],y=bld["Waste"],name="Est. Wasted",marker_color="#FF4757",marker_opacity=0.85))
    T(fig3); fig3.update_layout(barmode="group",height=300,xaxis_title="",yaxis_title="Litres",
                                 legend=dict(orientation="h",y=1.1,font_color="#8B9BB4"))
    st.plotly_chart(fig3, use_container_width=True)

    col3,col4 = st.columns(2, gap="large")
    with col3:
        fig4 = px.bar(bld.sort_values("Waste"),x="Waste",y="Building",
                      orientation="h",color="Waste",color_continuous_scale=_SEQ_RED,title="Wasted Water Ranking (L)")
        T(fig4); fig4.update_layout(height=280,coloraxis_showscale=False,xaxis_title="Litres",yaxis_title="")
        st.plotly_chart(fig4, use_container_width=True)
    with col4:
        fig5 = px.scatter(bld,x="Avg",y="Cost",size="Usage",color="Building",
                          title="Avg Daily Usage vs Total Cost",
                          color_discrete_sequence=_COLORS,hover_data=["Abn"])
        T(fig5); fig5.update_layout(height=280,xaxis_title="Avg Daily (L)",yaxis_title="Total Cost (AED)")
        st.plotly_chart(fig5, use_container_width=True)

    sec("📋","Building Summary Table")
    bd = bld.round(1).copy()
    bd.columns = ["Building","Total (L)","Cost (AED)","Avg Daily (L)","Wasted (L)","Anomaly Days","Records"]
    st.dataframe(bd, use_container_width=True, hide_index=True, height=300)

    vdiv()
    c1,_,_,_ = st.columns(4)
    with c1: st.download_button("📥 Export Building Data", bld.to_csv(index=False).encode("utf-8"), "building_comparison.csv","text/csv",use_container_width=True)

# ── LEAK DETECTION ───────────────────────────────────────
elif page.startswith("🚨"):
    page_header("🚨 Leak Detection","Statistical anomaly detection using the 2σ rule")
    if not need_data(): st.stop()
    s = stats

    ibox(f"""<strong>Detection Logic:</strong> Any day where water usage exceeds 
    <strong>Average + 2 × Std Dev</strong> is flagged as abnormal — likely indicating a 
    <strong>pipe leak, faulty valve, or unexpected consumption spike</strong>.<br><br>
    📏 Avg: <strong>{s['avg']:,.1f} L/day</strong> &nbsp;|&nbsp;
    📊 Std Dev: <strong>{s['std']:,.1f} L</strong> &nbsp;|&nbsp;
    🚨 Threshold: <strong>{s['thresh']:,.1f} L/day</strong>""", "info")

    abn = df[df["Is_Abnormal"]]
    pct = s["n_abnormal"]/s["n_rows"]*100 if s["n_rows"] else 0
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(scard("🚨","Anomaly Days",str(s["n_abnormal"]),f"of {s['n_rows']} days","scard-red"), unsafe_allow_html=True)
    with c2: st.markdown(scard("📊","Anomaly Rate",f"{pct:.1f}%","Of total data","scard-yellow"), unsafe_allow_html=True)
    with c3: st.markdown(scard("💧","Est. Wasted",fmt(s["total_waste"])+" L","Above-threshold","scard-blue"), unsafe_allow_html=True)
    with c4: st.markdown(scard("💰","AED Loss",f"AED {fmt(s['abn_cost'])}","From anomalies","scard-purple"), unsafe_allow_html=True)

    vdiv()

    # Timeline
    daily = df.groupby("Date").agg(U=("Water_Usage_Liters","sum"),A=("Is_Abnormal","any")).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily["Date"],y=daily["U"],mode="lines",name="Usage",
        line=dict(color="#00D4FF",width=1.8),fill="tozeroy",fillcolor="rgba(0,212,255,0.05)",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Usage: %{y:,.0f} L<extra></extra>"))
    ad = daily[daily["A"]]
    if len(ad):
        fig.add_trace(go.Scatter(x=ad["Date"],y=ad["U"],mode="markers",name="⚠️ Anomaly",
            marker=dict(color="#FF4757",size=11,symbol="circle",
                        line=dict(color="rgba(255,71,87,0.3)",width=6)),
            hovertemplate="<b>ANOMALY — %{x|%d %b %Y}</b><br>Usage: %{y:,.0f} L<extra></extra>"))
    fig.add_hline(y=s["thresh"],line_dash="dash",line_color="#FF4757",
                  annotation_text=f"Threshold: {s['thresh']:,.0f} L",annotation_font=dict(color="#FF4757",size=10))
    fig.add_hline(y=s["avg"],line_dash="dot",line_color="#00FF9D",
                  annotation_text=f"Avg: {s['avg']:,.0f} L",annotation_font=dict(color="#00FF9D",size=10))
    T(fig); fig.update_layout(height=320,xaxis_title="",yaxis_title="Litres",showlegend=True,
                               legend=dict(orientation="h",y=1.08,font_color="#8B9BB4"))
    st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2, gap="large")
    with col1:
        sec("🏢","Anomaly Days per Building")
        ab = df.groupby("Building")["Is_Abnormal"].sum().reset_index()
        ab.columns = ["Building","Anomalies"]
        ab = ab[ab["Anomalies"]>0].sort_values("Anomalies",ascending=False)
        if len(ab):
            fig2 = px.bar(ab,x="Building",y="Anomalies",color="Anomalies",
                          color_continuous_scale=_SEQ_RED)
            T(fig2); fig2.update_layout(height=260,coloraxis_showscale=False,xaxis_title="",yaxis_title="Anomaly Days")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            ibox("✅ No anomalies detected per building.", "success")

    with col2:
        sec("📦","Usage Distribution")
        fig3 = go.Figure()
        fig3.add_trace(go.Histogram(x=df["Water_Usage_Liters"],nbinsx=30,
                                    marker_color="#00D4FF",marker_opacity=0.65,name="Records",
                                    hovertemplate="Range: %{x}<br>Count: %{y}<extra></extra>"))
        fig3.add_vline(x=s["avg"],line_dash="dot",line_color="#00FF9D",annotation_text="Avg",
                       annotation_font=dict(color="#00FF9D",size=10))
        fig3.add_vline(x=s["thresh"],line_dash="dash",line_color="#FF4757",annotation_text="Threshold",
                       annotation_font=dict(color="#FF4757",size=10))
        T(fig3); fig3.update_layout(height=260,xaxis_title="Litres",yaxis_title="Frequency",showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    sec("📋","Flagged Records")
    if len(abn):
        ad2 = abn[["Date","Building","Water_Usage_Liters","Cost_AED","Wasted_Liters"]].copy()
        ad2.columns = ["Date","Building","Usage (L)","Cost (AED)","Wasted (L)"]
        ad2 = ad2.round(2).sort_values("Wasted (L)",ascending=False)
        st.dataframe(ad2, use_container_width=True, hide_index=True, height=300)
        vdiv()
        c1,_,_,_ = st.columns(4)
        with c1: st.download_button("📥 Export Anomaly Records", ad2.to_csv(index=False).encode("utf-8"), "anomaly_records.csv","text/csv",use_container_width=True)
    else:
        ibox("✅ No abnormal records found in this dataset.", "success")

# ── IMPACT CALCULATOR ────────────────────────────────────
elif page.startswith("🌍"):
    page_header("🌍 Impact Calculator","Financial and environmental cost of water waste")
    if not need_data(): st.stop()
    s = stats

    days    = (df["Date"].max()-df["Date"].min()).days + 1
    y_waste = (s["total_waste"]/days)*365
    y_save  = y_waste*0.5
    y_aed   = (s["abn_cost"]/days)*365*0.5
    co2     = y_save*0.000344
    kwh     = y_save*0.004
    bottles = y_save*2
    trees   = y_save*0.05/1000
    wp      = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0

    sec("📊","Current Waste — This Dataset")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(scard("💧","Wasted (Period)",fmt(s["total_waste"])+" L","From anomaly days","scard-red"), unsafe_allow_html=True)
    with c2: st.markdown(scard("📊","Waste Percentage",f"{wp:.1f}%","Of total usage","scard-yellow"), unsafe_allow_html=True)
    with c3: st.markdown(scard("💰","AED Lost",f"AED {fmt(s['abn_cost'])}","Anomaly days cost","scard-blue"), unsafe_allow_html=True)
    with c4: st.markdown(scard("📅","Data Period",f"{days} days",f"{df['Date'].min().date()}","scard-purple"), unsafe_allow_html=True)

    vdiv()
    sec("🌱","Projected Yearly Impact — at 50% Waste Reduction")
    ibox("""Projections based on reducing anomalous usage by <strong>50%</strong> through 
    leak repairs and operational improvements — a <strong>realistic, achievable target</strong>.""", "success")

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(scard("💧","Water Saved/Year",fmt(y_save)+" L","50% of yearly waste","scard-green"), unsafe_allow_html=True)
    with c2: st.markdown(scard("💰","AED Saved/Year",f"AED {fmt(y_aed)}","Projected financial","scard-blue"), unsafe_allow_html=True)
    with c3: st.markdown(scard("🌿","CO₂ Avoided",f"{co2:,.1f} kg","Less desalination","scard-purple"), unsafe_allow_html=True)
    with c4: st.markdown(scard("⚡","Energy Saved",f"{kwh:,.1f} kWh","Desal energy cut","scard-yellow"), unsafe_allow_html=True)

    c5,c6,_,_ = st.columns(4)
    with c5: st.markdown(scard("🍶","Bottles Avoided",fmt(bottles),"500ml equiv.","scard-red"), unsafe_allow_html=True)
    with c6: st.markdown(scard("🌳","Tree CO₂ Equiv.",f"{trees:,.0f}","Offset equivalent","scard-green"), unsafe_allow_html=True)

    vdiv()
    col1,col2 = st.columns(2, gap="large")
    with col1:
        pie = pd.DataFrame({"Cat":["Normal","Wasted"],"V":[s["total_usage"]-s["total_waste"],s["total_waste"]]})
        fig = px.pie(pie,values="V",names="Cat",hole=0.62,
                     color="Cat",color_discrete_map={"Normal":"#00D4FF","Wasted":"#FF4757"})
        fig.update_traces(textinfo="percent+label",textfont_color="#E2E8F0",
                          marker_line=dict(color="#0F1623",width=2))
        T(fig); fig.update_layout(height=280,showlegend=False,title="Waste vs Normal Usage")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = go.Figure(go.Waterfall(
            orientation="v",measure=["relative","relative","relative","total"],
            x=["Yearly Waste","50% Reduction","Remaining","Net Saving"],
            y=[y_waste,-y_save,y_save,0],
            connector={"line":{"color":"rgba(255,255,255,0.1)"}},
            increasing={"marker":{"color":"rgba(255,71,87,0.7)","line":{"color":"#FF4757","width":1}}},
            decreasing={"marker":{"color":"rgba(0,255,157,0.7)","line":{"color":"#00FF9D","width":1}}},
            totals={"marker":{"color":"rgba(0,212,255,0.7)","line":{"color":"#00D4FF","width":1}}},
            text=["","","",""],
        ))
        T(fig2); fig2.update_layout(height=280,title="Yearly Saving Waterfall (L)",yaxis_title="Litres")
        st.plotly_chart(fig2, use_container_width=True)

    vdiv()
    sec("🎛️","Custom Reduction Scenario")
    pct = st.slider("Waste reduction target", 10, 90, 50, 5, format="%d%%")
    cs = y_waste*(pct/100); ca = y_aed*(pct/50); cc = cs*0.000344
    c1,c2,c3,_ = st.columns(4)
    with c1: st.markdown(scard("💧",f"Saved at {pct}%",fmt(cs)+" L/yr","","scard-blue"), unsafe_allow_html=True)
    with c2: st.markdown(scard("💰","AED Saved",f"AED {fmt(ca)}/yr","","scard-green"), unsafe_allow_html=True)
    with c3: st.markdown(scard("🌿","CO₂ Avoided",f"{cc:,.2f} kg/yr","","scard-purple"), unsafe_allow_html=True)

# ── RECOMMENDATIONS ──────────────────────────────────────
elif page.startswith("🤖"):
    page_header("🤖 AI Recommendations","Data-driven actions tailored to your campus patterns")
    if not need_data(): st.stop()
    s = stats
    wp = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0

    ibox(f"""⚠️ Campus is wasting an estimated <strong>{wp:.1f}%</strong> of its water through 
    <strong>{s['n_abnormal']}</strong> anomaly events. Recommendations below are derived from 
    your data patterns.""", "danger")

    # Building-level alerts
    ba  = df.groupby("Building").agg(A=("Is_Abnormal","sum"),W=("Wasted_Liters","sum")).reset_index()
    top = ba[ba["A"]>0].sort_values("A",ascending=False)

    if len(top):
        sec("🏢","Building Alerts")
        for _, row in top.head(5).iterrows():
            severity = "danger" if row["A"] >= 5 else "warn"
            ibox(f"""🚨 <strong>{row['Building']}</strong> — {int(row['A'])} anomaly day(s) detected · 
            Estimated <strong>{row['W']:,.0f} L</strong> wasted above average. Immediate inspection recommended.""", severity)

    vdiv()
    sec("💡","Recommendations")
    RECS = [
        ("🔧","Fix Leaks Immediately",
         f"Your data flagged {s['n_abnormal']} abnormal usage days — likely leaks, running "
         "toilets, or faulty valves. A single dripping tap wastes 10,000+ L/year. "
         "Plumbing inspection delivers the highest ROI of any intervention.","30–50% waste reduction"),
        ("📱","Deploy Smart Water Meters",
         "IoT-enabled meters provide real-time alerts when usage exceeds thresholds — "
         "automating exactly what this dashboard detects, running 24/7 without manual uploads.","Instant leak detection"),
        ("🚿","Upgrade to Low-Flow Fixtures",
         "Low-flow taps and toilets cut consumption 30–50% with no change in user "
         "experience. Prioritise the buildings with the highest anomaly counts first.","30–45% per fixture"),
        ("🌿","Greywater Recycling",
         "Reuse sink and shower water for flushing and irrigation. UAE campuses with "
         "greywater systems report up to 40% reduction in potable water demand.","Up to 40% saving"),
        ("👥","Awareness Programme",
         "Monthly water challenges at UAE universities achieve 15–25% reductions "
         "within 3 months. Low-cost, high-impact with the right communications.","15–25% reduction"),
        ("🗓️","Quarterly Plumbing Audits",
         "Preventive maintenance is 10× cheaper than emergency repairs. Scheduled "
         "audits catch the slow leaks that are invisible without data like this.","60–80% fewer anomalies"),
        ("☀️","Solar Water Heating",
         "Solar heaters eliminate energy costs from water heating. Combined with "
         "insulated pipes, this removes heat-loss waste and supports Net Zero 2050.","20% energy + water saving"),
        ("🌱","Drought-Resistant Landscaping",
         "UAE-native plants with drip irrigation dramatically reduce outdoor usage. "
         "Landscape irrigation accounts for up to 50% of campus water in summer months.","Up to 50% irrigation saving"),
    ]
    for icon, title, body, saving in RECS:
        st.markdown(f"""<div class='rec-card'>
            <div class='rec-icon-box'>{icon}</div>
            <div>
                <div class='rec-title'>{title}</div>
                <div class='rec-body'>{body}</div>
                <div class='rec-tag'>💚 {saving}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    vdiv()
    sec("📊","Priority Matrix — Impact vs Ease")
    pri = pd.DataFrame({
        "Action":  ["Fix Leaks","Smart Meters","Low-Flow Fixtures","Greywater","Awareness Campaign"],
        "Impact":  [95, 85, 75, 70, 55],
        "Ease":    [80, 50, 70, 35, 90],
        "Cost":    [5,  80, 40, 150, 2],
    })
    fig = px.scatter(pri, x="Ease", y="Impact", size="Cost", text="Action", color="Impact",
                     color_continuous_scale=_SEQ_BLUE, size_max=36,
                     labels={"Ease":"← Harder    Ease of Implementation    Easier →","Impact":"Impact Score ↑"})
    fig.update_traces(textposition="top center",textfont=dict(color="#E2E8F0",size=11))
    fig.add_hline(y=75, line_dash="dot", line_color="rgba(255,255,255,0.1)")
    fig.add_vline(x=60, line_dash="dot", line_color="rgba(255,255,255,0.1)")
    T(fig); fig.update_layout(height=360,coloraxis_showscale=False,
                               annotations=[
                                   dict(x=85,y=98,text="Do first",showarrow=False,font=dict(color="#00FF9D",size=10)),
                                   dict(x=25,y=98,text="Plan carefully",showarrow=False,font=dict(color="#FFD166",size=10)),
                                   dict(x=85,y=52,text="Quick wins",showarrow=False,font=dict(color="#8B9BB4",size=10)),
                                   dict(x=25,y=52,text="Reconsider",showarrow=False,font=dict(color="#FF4757",size=10)),
                               ])
    st.plotly_chart(fig, use_container_width=True)

# ── IMPACT REPORT ────────────────────────────────────────
elif page.startswith("📋"):
    page_header("📋 Final Impact Report","Complete summary of findings, projections, and actions")
    if not need_data(): st.stop()
    s = stats

    days    = (df["Date"].max()-df["Date"].min()).days + 1
    y_waste = (s["total_waste"]/days)*365
    y_save  = y_waste*0.5
    y_aed   = (s["abn_cost"]/days)*365*0.5
    co2     = y_save*0.000344
    wp      = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0
    bld_n   = df["Building"].nunique()

    # Report hero
    st.markdown(f"""<div class='report-card'>
        <div style='font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;color:#F0F6FF;margin-bottom:4px;'>
            💧 Campus Water Impact Report
        </div>
        <div style='color:rgba(255,255,255,0.4);font-size:0.82rem;margin-bottom:26px;font-family:Inter,sans-serif;'>
            Generated {datetime.now().strftime("%d %B %Y, %H:%M")} &nbsp;·&nbsp;
            Period: {df['Date'].min().date()} → {df['Date'].max().date()} &nbsp;·&nbsp;
            {bld_n} buildings &nbsp;·&nbsp; {days} days
        </div>
        <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:16px;'>
            <div style='text-align:center;background:rgba(0,0,0,0.2);border-radius:12px;padding:16px;'>
                <div class='rval'>{fmt(s["total_usage"])} L</div>
                <div class='rlbl'>Total Water Consumed</div>
            </div>
            <div style='text-align:center;background:rgba(0,0,0,0.2);border-radius:12px;padding:16px;'>
                <div class='rval'>AED {fmt(s["total_cost"])}</div>
                <div class='rlbl'>Total Water Cost</div>
            </div>
            <div style='text-align:center;background:rgba(0,0,0,0.2);border-radius:12px;padding:16px;'>
                <div class='rval' style='color:#FF4757;'>{s["n_abnormal"]}</div>
                <div class='rlbl'>Anomaly Days Detected</div>
            </div>
            <div style='text-align:center;background:rgba(0,0,0,0.2);border-radius:12px;padding:16px;'>
                <div class='rval' style='color:#FFD166;'>{wp:.1f}%</div>
                <div class='rlbl'>Estimated Water Wasted</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    sec("🌱","Projected Yearly Savings — 50% Waste Reduction")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(scard("💧","Water Saved/Year",fmt(y_save)+" L","","scard-green"), unsafe_allow_html=True)
    with c2: st.markdown(scard("💰","AED Saved/Year",f"AED {fmt(y_aed)}","","scard-blue"), unsafe_allow_html=True)
    with c3: st.markdown(scard("🌿","CO₂ Avoided",f"{co2:,.1f} kg/yr","","scard-purple"), unsafe_allow_html=True)
    with c4: st.markdown(scard("🏢","Buildings Studied",str(bld_n),"","scard-yellow"), unsafe_allow_html=True)

    vdiv()
    col1,col2 = st.columns(2, gap="large")
    with col1:
        pie = pd.DataFrame({"Cat":["Normal","Wasted"],"V":[s["total_usage"]-s["total_waste"],s["total_waste"]]})
        fig = px.pie(pie,values="V",names="Cat",hole=0.58,
                     color="Cat",color_discrete_map={"Normal":"#00D4FF","Wasted":"#FF4757"})
        fig.update_traces(textinfo="percent+label",textfont_color="#E2E8F0",
                          marker_line=dict(color="#0F1623",width=2))
        T(fig); fig.update_layout(height=270,showlegend=False,title="Normal vs Wasted Water")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        bs = df.groupby("Building")["Water_Usage_Liters"].sum().reset_index()
        fig2 = px.pie(bs,values="Water_Usage_Liters",names="Building",hole=0.58,
                      color_discrete_sequence=_COLORS)
        fig2.update_traces(textinfo="percent+label",textfont_color="#E2E8F0",
                           marker_line=dict(color="#0F1623",width=2))
        T(fig2); fig2.update_layout(height=270,showlegend=False,title="Usage Share by Building")
        st.plotly_chart(fig2, use_container_width=True)

    sec("📅","Monthly Trend")
    mn = df.groupby("Month_Label")["Water_Usage_Liters"].sum().reset_index()
    fig3 = px.bar(mn,x="Month_Label",y="Water_Usage_Liters",color="Water_Usage_Liters",
                  color_continuous_scale=_SEQ_BLUE)
    T(fig3); fig3.update_layout(height=260,coloraxis_showscale=False,xaxis_title="",yaxis_title="Litres",title="")
    st.plotly_chart(fig3, use_container_width=True)

    vdiv()
    sec("📝","Key Findings")
    for f in [
        f"📍 Campus consumed **{s['total_usage']:,.0f} L** over {days} days — averaging **AED {s['total_cost']/days:,.2f}/day**.",
        f"🚨 **{s['n_abnormal']} anomaly events** detected (2σ threshold: {s['thresh']:,.0f} L/day).",
        f"🌊 Estimated **{s['total_waste']:,.0f} L wasted** — {wp:.1f}% of total consumption.",
        f"💰 AED loss from anomalies: **AED {s['abn_cost']:,.2f}** over the analysis period.",
        f"🌱 At 50% waste reduction: **{y_save:,.0f} L/year** and **AED {y_aed:,.2f}/year** recovered.",
        f"🌿 This prevents **{co2:,.2f} kg CO₂/year** from reduced desalination energy.",
        f"🏢 **{bld_n} buildings** analysed — highest-waste buildings should be prioritised first.",
    ]:
        st.markdown(f)

    vdiv()
    sec("🎯","Top 3 Priority Actions")
    for num, icon, title, body in [
        ("1","🔧","Fix Leaks Immediately",f"Inspect all {s['n_abnormal']} anomaly days. Highest ROI action available."),
        ("2","📱","Deploy Smart Water Meters","Real-time 24/7 anomaly detection — no manual uploads needed."),
        ("3","🚿","Low-Flow Fixture Upgrade","Upgrade top-usage buildings. UAE campus ROI: typically 12–18 months."),
    ]:
        st.markdown(f"""<div class='rec-card'>
            <div style='width:42px;height:42px;border-radius:11px;flex-shrink:0;
                        background:rgba(0,212,255,0.1);border:1px solid rgba(0,212,255,0.2);
                        color:#00D4FF;font-family:Syne,sans-serif;font-weight:800;font-size:1.1rem;
                        display:flex;align-items:center;justify-content:center;'>{num}</div>
            <div>
                <div class='rec-title'>{icon} {title}</div>
                <div class='rec-body'>{body}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    vdiv()
    sec("⬇️","Export Full Report")
    c1,c2,c3,_ = st.columns([1,1,1,2])
    with c1: st.download_button("📥 Full Dataset (CSV)", get_export_csv(df), "aquasense_data.csv","text/csv",use_container_width=True)
    with c2: st.download_button("📊 Summary Report (CSV)", get_summary_csv(stats,df), "aquasense_summary.csv","text/csv",use_container_width=True)
    with c3:
        bld_exp = df.groupby("Building").agg(
            Total_L=("Water_Usage_Liters","sum"),Cost_AED=("Cost_AED","sum"),
            Avg_Daily=("Water_Usage_Liters","mean"),Wasted_L=("Wasted_Liters","sum"),
            Anomaly_Days=("Is_Abnormal","sum")
        ).reset_index()
        st.download_button("🏢 Building Report (CSV)", bld_exp.to_csv(index=False).encode("utf-8"), "building_report.csv","text/csv",use_container_width=True)

# ── Footer ─────────────────────────────────────────────────
st.markdown("""<div class='app-footer'>
    💧 AquaSense UAE &nbsp;·&nbsp; AI-Powered Water Impact Dashboard &nbsp;·&nbsp;
    Streamlit · Plotly · Pandas · NumPy &nbsp;·&nbsp; UAE Net Zero 2050 · SDG 6
</div>""", unsafe_allow_html=True)
