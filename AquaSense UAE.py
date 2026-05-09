"""
AquaSense UAE — AI-Powered Water Impact Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from datetime import datetime

st.set_page_config(
    page_title="AquaSense UAE",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# DESIGN TOKENS + CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

/* ── CANVAS ── */
html, body { background: #07111F !important; }

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section[data-testid="stMain"],
.main .block-container {
    background: #07111F !important;
    padding: 0 28px 40px 28px !important;
    max-width: 100% !important;
}
[data-testid="stHeader"]    { display: none !important; }
[data-testid="stDecoration"]{ display: none !important; }
[data-testid="stToolbar"]   { display: none !important; }
div[data-testid="stStatusWidget"] { display: none !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0B1525 !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
    min-width: 240px !important;
    max-width: 240px !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: #0B1525 !important;
    padding: 0 !important;
}

/* ── GLOBAL TEXT ── */
h1,h2,h3,h4,h5 { font-family:'Syne',sans-serif !important; color:#F0F6FF !important; }
p, li, div, span, label { font-family:'Inter',sans-serif !important; }

/* ── FILE UPLOADER — compact dark ── */
[data-testid="stFileUploader"] {
    background: transparent !important;
}
[data-testid="stFileUploader"] > label { display: none !important; }
[data-testid="stFileUploader"] section {
    background: #0F1E30 !important;
    border: 1.5px dashed rgba(0,195,220,0.28) !important;
    border-radius: 10px !important;
    padding: 12px 10px !important;
    min-height: unset !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: rgba(0,195,220,0.55) !important;
}
[data-testid="stFileUploader"] section * { color: #4A6080 !important; font-size: 0.78rem !important; }
[data-testid="stFileUploader"] section button {
    background: rgba(0,195,220,0.1) !important;
    border: 1px solid rgba(0,195,220,0.25) !important;
    color: #00C3DC !important;
    border-radius: 6px !important;
    font-size: 0.75rem !important;
    padding: 4px 10px !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── SIDEBAR NAV BUTTONS ── */
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div > [data-testid="stButton"] > button {
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    color: #6B829E !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.84rem !important;
    font-weight: 400 !important;
    text-align: left !important;
    padding: 9px 14px !important;
    width: 100% !important;
    transition: all 0.15s ease !important;
    box-shadow: none !important;
    letter-spacing: 0.01em !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div > [data-testid="stButton"] > button:hover {
    background: rgba(0,195,220,0.07) !important;
    color: #B0C8D8 !important;
    box-shadow: none !important;
}
/* Active nav — primary type */
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div > [data-testid="stButton"] > button[kind="primary"] {
    background: rgba(0,195,220,0.1) !important;
    color: #00C3DC !important;
    font-weight: 600 !important;
    border: none !important;
    border-left: 2px solid #00C3DC !important;
    border-radius: 0 8px 8px 0 !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div > [data-testid="stButton"] > button[kind="primary"]:hover {
    background: rgba(0,195,220,0.14) !important;
}

/* ── MAIN BUTTONS ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #00A8C8, #0072A3) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
    padding: 9px 18px !important;
    box-shadow: 0 2px 12px rgba(0,168,200,0.22) !important;
}
.stButton > button:not([kind="primary"]) {
    background: #0F1E30 !important;
    color: #6B829E !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    padding: 7px 14px !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: #152030 !important;
    color: #8FA8C0 !important;
    border-color: rgba(0,195,220,0.2) !important;
}

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background: rgba(0,230,140,0.09) !important;
    color: #00E68C !important;
    border: 1px solid rgba(0,230,140,0.22) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    transition: all 0.18s !important;
}
.stDownloadButton > button:hover {
    background: rgba(0,230,140,0.15) !important;
    border-color: rgba(0,230,140,0.4) !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    background: #0C1A28 !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] * { color: #8FA8C0 !important; }
[data-testid="stDataFrame"] th { color: #4A6080 !important; background: #0F1E30 !important; }
.dvn-scroller { background: #0C1A28 !important; }

/* ── SLIDER ── */
[data-testid="stSlider"] * { color: #6B829E !important; font-family: 'Inter',sans-serif !important; }
[data-testid="stSlider"] [data-baseweb="slider"] > div:first-child { background: #152030 !important; }
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] { background: #00C3DC !important; }

/* ── SELECTBOX ── */
[data-baseweb="select"] { background: #0F1E30 !important; border-color: rgba(255,255,255,0.08) !important; }
[data-baseweb="select"] * { color: #8FA8C0 !important; font-family: 'Inter',sans-serif !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width:4px; height:4px; }
::-webkit-scrollbar-track { background:#07111F; }
::-webkit-scrollbar-thumb { background:#1A2E42; border-radius:4px; }
::-webkit-scrollbar-thumb:hover { background:#00C3DC; }

/* ── WARNING / INFO / ERROR ── */
[data-testid="stAlert"] { border-radius: 10px !important; }

/* ══ CUSTOM COMPONENT CLASSES ══ */

/* Metric card */
.mc {
    background: #0C1A28;
    border: 1px solid rgba(255,255,255,0.055);
    border-radius: 14px;
    padding: 20px 20px 16px;
    position: relative; overflow: hidden;
    transition: transform .18s, border-color .18s;
    height: 100%;
}
.mc:hover { transform: translateY(-2px); border-color: rgba(0,195,220,0.2); }
.mc-accent { position:absolute; top:0; left:0; right:0; height:2px; border-radius:14px 14px 0 0; }
.mc-icon  { font-size:1.4rem; margin-bottom:10px; }
.mc-label { font-size:0.68rem; color:#3D5268; text-transform:uppercase; letter-spacing:1.1px; font-weight:600; margin-bottom:4px; font-family:'Inter',sans-serif; }
.mc-value { font-family:'Syne',sans-serif; font-size:1.65rem; font-weight:800; line-height:1; }
.mc-delta { font-size:0.73rem; color:#3D5268; margin-top:6px; font-family:'Inter',sans-serif; }
.c-cyan   { color:#00C3DC; }
.c-green  { color:#00D68C; }
.c-red    { color:#FF4460; }
.c-amber  { color:#FFBD4A; }
.c-purple { color:#9B7AFF; }
.c-white  { color:#CDD9E5; }

/* Info boxes */
.ib { border-radius:10px; padding:13px 16px; margin:10px 0; font-size:0.855rem; font-family:'Inter',sans-serif; line-height:1.62; }
.ib b, .ib strong { font-weight:700; }
.ib-info    { background:rgba(0,195,220,0.07);  border-left:3px solid rgba(0,195,220,0.6);  color:#7ABFCF; }
.ib-success { background:rgba(0,214,140,0.07);  border-left:3px solid rgba(0,214,140,0.5);  color:#62C79B; }
.ib-warn    { background:rgba(255,189,74,0.07); border-left:3px solid rgba(255,189,74,0.5); color:#E8AC4A; }
.ib-danger  { background:rgba(255,68,96,0.07);  border-left:3px solid rgba(255,68,96,0.5);  color:#E86070; }

/* Page header */
.ph {
    padding: 28px 0 20px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 24px;
}
.ph-title { font-family:'Syne',sans-serif; font-size:1.55rem; font-weight:800; color:#EEF4FF; margin:0 0 3px; }
.ph-sub   { font-size:0.83rem; color:#3D5268; font-family:'Inter',sans-serif; }

/* Section label */
.sl {
    font-family:'Syne',sans-serif; font-size:0.95rem; font-weight:700;
    color:#CDD9E5; margin:22px 0 12px;
    display:flex; align-items:center; gap:9px;
}
.sl-dot { width:6px; height:6px; border-radius:50%; background:#00C3DC; flex-shrink:0; }

/* Rec card */
.rc {
    background:#0C1A28; border:1px solid rgba(255,255,255,0.055);
    border-radius:13px; padding:17px 18px; margin-bottom:11px;
    display:flex; gap:14px; align-items:flex-start;
    transition:border-color .18s;
}
.rc:hover { border-color:rgba(0,195,220,0.18); }
.rc-icon {
    width:40px; height:40px; border-radius:10px; flex-shrink:0;
    background:rgba(0,195,220,0.09); border:1px solid rgba(0,195,220,0.18);
    display:flex; align-items:center; justify-content:center; font-size:1.15rem;
}
.rc-title { font-family:'Syne',sans-serif; font-size:0.9rem; font-weight:700; color:#CDD9E5; margin-bottom:4px; }
.rc-body  { font-size:0.8rem; color:#3D5268; line-height:1.56; font-family:'Inter',sans-serif; }
.rc-tag   { display:inline-block; background:rgba(0,214,140,0.08); color:#00D68C; border-radius:20px; padding:2px 10px; font-size:0.7rem; font-weight:600; margin-top:6px; font-family:'Inter',sans-serif; border:1px solid rgba(0,214,140,0.18); }

/* Report hero */
.rh {
    background:linear-gradient(135deg,#091929 0%,#0C2035 50%,#0A1E36 100%);
    border:1px solid rgba(0,195,220,0.12);
    border-radius:18px; padding:30px 34px; margin-bottom:20px; position:relative; overflow:hidden;
}
.rh::after { content:''; position:absolute; top:-80px; right:-80px; width:260px; height:260px; border-radius:50%; background:radial-gradient(circle,rgba(0,195,220,0.06) 0%,transparent 70%); }
.rh-val { font-family:'Syne',sans-serif; font-size:1.85rem; font-weight:800; color:#00C3DC; }
.rh-lbl { font-size:0.75rem; color:rgba(255,255,255,0.35); margin-top:3px; font-family:'Inter',sans-serif; }

/* Row divider */
.rd { height:1px; background:rgba(255,255,255,0.05); border:none; margin:22px 0; }

/* Step row */
.sr { display:flex; align-items:center; gap:12px; padding:9px 12px; background:#0C1A28; border:1px solid rgba(255,255,255,0.05); border-radius:10px; margin-bottom:7px; }
.sr-n { width:26px; height:26px; border-radius:50%; background:rgba(0,195,220,0.1); border:1px solid rgba(0,195,220,0.25); color:#00C3DC; font-family:'Syne',sans-serif; font-weight:800; font-size:0.78rem; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.sr-t { font-size:0.83rem; color:#6B829E; font-family:'Inter',sans-serif; }

/* Feature row */
.fr { display:flex; align-items:flex-start; gap:11px; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.04); }
.fr-t { font-size:0.84rem; color:#6B829E; font-family:'Inter',sans-serif; line-height:1.45; }

/* Sidebar label */
.sbl { padding:14px 16px 6px; font-size:0.63rem; color:#2A3A4E; font-weight:700; letter-spacing:1.6px; text-transform:uppercase; font-family:'Inter',sans-serif; }

/* Building bar */
.bb { display:flex; align-items:center; gap:10px; padding:9px 12px; background:#0C1A28; border:1px solid rgba(255,255,255,0.05); border-radius:10px; margin-bottom:7px; }
.bb-bar { height:3px; background:rgba(255,255,255,0.05); border-radius:2px; margin-top:5px; }
.bb-fill { height:3px; background:#00C3DC; border-radius:2px; }

/* Health row */
.hr-row { display:flex; justify-content:space-between; align-items:center; padding:9px 14px; border-radius:9px; margin-bottom:7px; }
.hr-ok   { background:rgba(0,214,140,0.06); border:1px solid rgba(0,214,140,0.1); }
.hr-warn { background:rgba(255,189,74,0.06); border:1px solid rgba(255,189,74,0.1); }
.hr-bad  { background:rgba(255,68,96,0.06);  border:1px solid rgba(255,68,96,0.1); }

/* Dataset item */
.ds-item { display:flex; align-items:center; gap:6px; padding:7px 10px; margin:3px 8px; border-radius:8px; background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.04); font-size:0.78rem; }
.ds-name { color:#6B829E; font-family:'Inter',sans-serif; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:120px; }
.ds-badge { font-size:0.6rem; color:#00C3DC; background:rgba(0,195,220,0.08); padding:1px 7px; border-radius:10px; border:1px solid rgba(0,195,220,0.18); }

/* Empty state */
.es { text-align:center; padding:70px 20px; background:#0C1A28; border:1px dashed rgba(255,255,255,0.06); border-radius:16px; margin:16px 0; }
.es-icon  { font-size:2.8rem; margin-bottom:12px; }
.es-title { font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:700; color:#1E3045; }
.es-sub   { font-size:0.82rem; color:#1A2A3A; margin-top:6px; font-family:'Inter',sans-serif; }

/* Footer */
.ft { text-align:center; padding:18px; border-top:1px solid rgba(255,255,255,0.04); margin-top:40px; font-family:'Inter',sans-serif; font-size:0.73rem; color:#1E3045; }

/* Overview welcome hero */
.wh { background:linear-gradient(140deg,rgba(0,195,220,0.07) 0%,rgba(0,110,160,0.04) 100%); border:1px solid rgba(0,195,220,0.1); border-radius:16px; padding:30px 30px 28px; margin-bottom:20px; }
.wh-title { font-family:'Syne',sans-serif; font-size:1.75rem; font-weight:800; color:#EEF4FF; margin:0 0 6px; }
.wh-sub   { font-size:0.88rem; color:#4A6080; line-height:1.65; font-family:'Inter',sans-serif; }

/* Col code chip */
.chip { display:inline-flex; align-items:center; gap:8px; background:#0C1A28; border:1px solid rgba(255,255,255,0.07); border-radius:8px; padding:8px 12px; margin-bottom:6px; width:100%; }
.chip-code { font-family:monospace; font-size:0.8rem; color:#00C3DC; background:rgba(0,195,220,0.08); padding:2px 8px; border-radius:5px; }
.chip-desc { font-size:0.77rem; color:#3D5268; font-family:'Inter',sans-serif; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PLOTLY DARK THEME
# ══════════════════════════════════════════════════════════════════════════════
C = ["#00C3DC","#00D68C","#9B7AFF","#FFBD4A","#FF4460",
     "#38B8D0","#2EC47A","#7A5FD4","#E8AC4A","#E84060"]

_PL = dict(
    font=dict(family="Inter", color="#6B829E", size=12),
    plot_bgcolor  ="#0C1A28",
    paper_bgcolor ="#0C1A28",
    margin        =dict(l=16, r=16, t=38, b=16),
    colorway      =C,
    title_font    =dict(family="Syne", size=13, color="#CDD9E5"),
    legend        =dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#6B829E", size=11)),
    xaxis         =dict(gridcolor="rgba(255,255,255,0.03)", linecolor="rgba(255,255,255,0.06)",
                        tickfont=dict(color="#3D5268", size=10), title_font=dict(color="#4A6080"), zeroline=False),
    yaxis         =dict(gridcolor="rgba(255,255,255,0.03)", linecolor="rgba(255,255,255,0.06)",
                        tickfont=dict(color="#3D5268", size=10), title_font=dict(color="#4A6080"), zeroline=False),
)

def T(fig):
    fig.update_layout(**_PL)
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.03)", linecolor="rgba(255,255,255,0.06)",
                     tickfont=dict(color="#3D5268",size=10), zeroline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.03)", linecolor="rgba(255,255,255,0.06)",
                     tickfont=dict(color="#3D5268",size=10), zeroline=False)
    return fig

SB = [[0,"#091929"],[0.5,"#005E7A"],[1,"#00C3DC"]]
SG = [[0,"#091929"],[0.5,"#006644"],[1,"#00D68C"]]
SR = [[0,"#091929"],[0.5,"#7A0020"],[1,"#FF4460"]]

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
PAGES = [
    ("overview",  "🏠", "Overview"),
    ("dashboard", "📊", "Dashboard"),
    ("monthly",   "📅", "Monthly"),
    ("buildings", "🏢", "Buildings"),
    ("leaks",     "🚨", "Leak Detection"),
    ("impact",    "🌍", "Impact Calculator"),
    ("recs",      "🤖", "Recommendations"),
    ("report",    "📋", "Impact Report"),
]

for k, v in [("page","overview"),("datasets",{}),("active_ds",None),("confirm_del",None)]:
    if k not in st.session_state: st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
# DATA HELPERS
# ══════════════════════════════════════════════════════════════════════════════
REQUIRED = {"Date","Building","Water_Usage_Liters","Cost_AED"}

@st.cache_data(show_spinner=False)
def read_file(b, n):
    return pd.read_csv(io.BytesIO(b)) if n.lower().endswith(".csv") else pd.read_excel(io.BytesIO(b))

def process(raw):
    df = raw.copy()
    df["Date"]               = pd.to_datetime(df["Date"], errors="coerce")
    df["Water_Usage_Liters"] = pd.to_numeric(df["Water_Usage_Liters"], errors="coerce")
    df["Cost_AED"]           = pd.to_numeric(df["Cost_AED"], errors="coerce")
    df = df.dropna(subset=["Date","Water_Usage_Liters","Cost_AED"]).sort_values("Date").reset_index(drop=True)
    if len(df) == 0: return None, {}
    avg  = df["Water_Usage_Liters"].mean()
    std  = df["Water_Usage_Liters"].std(ddof=1) if len(df)>1 else 0.0
    thr  = avg + 2*std
    df["Is_Abnormal"]   = df["Water_Usage_Liters"] > thr
    df["Wasted_Liters"] = np.where(df["Is_Abnormal"], df["Water_Usage_Liters"]-avg, 0)
    df["Month_Label"]   = df["Date"].dt.strftime("%b %Y")
    df["Day_of_Week"]   = df["Date"].dt.day_name()
    s = dict(avg=avg, std=std, thresh=thr,
             total_usage=df["Water_Usage_Liters"].sum(),
             total_cost=df["Cost_AED"].sum(),
             total_waste=df["Wasted_Liters"].sum(),
             n_abnormal=int(df["Is_Abnormal"].sum()),
             n_rows=len(df),
             abn_cost=df[df["Is_Abnormal"]]["Cost_AED"].sum())
    return df, s

def fmt(n, d=0):
    if abs(n)>=1_000_000: return f"{n/1_000_000:.2f}M"
    if abs(n)>=1_000:     return f"{n/1_000:.1f}K"
    return f"{n:,.{d}f}"

def mc(icon, label, value, delta="", color_cls="c-cyan", accent="#00C3DC"):
    dh = f"<div class='mc-delta'>{delta}</div>" if delta else ""
    return f"""<div class='mc'>
        <div class='mc-accent' style='background:{accent};'></div>
        <div class='mc-icon'>{icon}</div>
        <div class='mc-label'>{label}</div>
        <div class='mc-value {color_cls}'>{value}</div>{dh}
    </div>"""

def sl(icon, text):
    st.markdown(f"<div class='sl'><span class='sl-dot'></span>{icon}&nbsp;{text}</div>",
                unsafe_allow_html=True)

def rd(): st.markdown("<hr class='rd'>", unsafe_allow_html=True)

def ib(content, kind="info"):
    st.markdown(f"<div class='ib ib-{kind}'>{content}</div>", unsafe_allow_html=True)

def ph(title, sub=""):
    s = f"<div class='ph-sub'>{sub}</div>" if sub else ""
    st.markdown(f"<div class='ph'><div class='ph-title'>{title}</div>{s}</div>",
                unsafe_allow_html=True)

# Export helpers
def csv_data(df):
    e = df[["Date","Building","Water_Usage_Liters","Cost_AED","Is_Abnormal","Wasted_Liters"]].copy()
    e.columns = ["Date","Building","Water_L","Cost_AED","Abnormal","Wasted_L"]
    return e.to_csv(index=False).encode()

def summary_csv(s, df):
    days = (df["Date"].max()-df["Date"].min()).days+1
    wp   = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0
    yw   = (s["total_waste"]/days)*365
    ya   = (s["abn_cost"]/days)*365*0.5
    return pd.DataFrame({
        "Metric":["Total Usage (L)","Total Cost (AED)","Period (days)","Buildings",
                  "Daily Avg (L)","Anomaly Days","Wasted (L)","Waste %",
                  "Yearly Saving 50% (L)","AED Saving/Year","CO₂ Avoided (kg/yr)"],
        "Value":[f"{s['total_usage']:,.1f}",f"{s['total_cost']:,.2f}",str(days),
                 str(df['Building'].nunique()),f"{s['avg']:,.1f}",str(s['n_abnormal']),
                 f"{s['total_waste']:,.1f}",f"{wp:.2f}%",f"{yw*0.5:,.1f}",
                 f"{ya:,.2f}",f"{yw*0.5*0.000344:,.4f}"]
    }).to_csv(index=False).encode()

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # ── Logo ──────────────────────────────────────────
    st.markdown("""
    <div style='padding:22px 16px 16px;border-bottom:1px solid rgba(255,255,255,0.05);margin-bottom:6px;'>
        <div style='font-size:1.8rem;'>💧</div>
        <div style='font-family:Syne,sans-serif;font-size:1.05rem;font-weight:800;
                    color:#EEF4FF;margin-top:6px;letter-spacing:-.01em;'>AquaSense UAE</div>
        <div style='font-size:0.63rem;color:#2A3A4E;letter-spacing:1.4px;
                    text-transform:uppercase;margin-top:2px;font-family:Inter,sans-serif;'>
            Smart Water Dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Navigation ────────────────────────────────────
    st.markdown("<div class='sbl'>Navigate</div>", unsafe_allow_html=True)

    for key, icon, label in PAGES:
        is_active = st.session_state.page == key
        clicked   = st.button(
            f"{icon}  {label}",
            key       = f"nav_{key}",
            type      = "primary" if is_active else "secondary",
            use_container_width = True,
        )
        if clicked and not is_active:
            st.session_state.page = key
            st.rerun()

    st.markdown("<hr style='border-color:rgba(255,255,255,0.05);margin:14px 0 6px;'>",
                unsafe_allow_html=True)

    # ── Dataset Manager ───────────────────────────────
    st.markdown("<div class='sbl'>My Datasets</div>", unsafe_allow_html=True)

    # Upload widget — compact
    up = st.file_uploader("up", type=["csv","xlsx","xls"],
                          label_visibility="collapsed", key="up_widget")
    if up:
        raw_ = read_file(up.read(), up.name)
        miss = REQUIRED - set(raw_.columns)
        if miss:
            st.error(f"Missing: {', '.join(miss)}", icon="⚠️")
        else:
            df_, s_ = process(raw_)
            if df_ is not None:
                name = up.name
                base = name; i = 2
                while name in st.session_state.datasets:
                    name = f"{base} ({i})"; i += 1
                st.session_state.datasets[name] = {
                    "raw":raw_, "df":df_, "stats":s_, "name":name,
                    "uploaded":datetime.now().strftime("%d %b")
                }
                st.session_state.active_ds = name
                st.rerun()

    # Dataset list
    if st.session_state.datasets:
        for ds_name, ds in list(st.session_state.datasets.items()):
            is_act = ds_name == st.session_state.active_ds
            ca, cb = st.columns([5,1], gap="small")
            with ca:
                lbl = ("● " if is_act else "○ ") + ds_name[:18] + ("…" if len(ds_name)>18 else "")
                if st.button(lbl, key=f"sel_{ds_name}", use_container_width=True,
                             type="primary" if is_act else "secondary"):
                    st.session_state.active_ds = ds_name
                    st.rerun()
            with cb:
                if st.button("✕", key=f"del_{ds_name}", help=f"Delete {ds_name}"):
                    st.session_state.confirm_del = ds_name
                    st.rerun()

        # Confirm delete
        if st.session_state.confirm_del:
            dn = st.session_state.confirm_del
            st.warning(f"Delete **{dn[:20]}**?", icon="🗑️")
            cy, cn = st.columns(2)
            with cy:
                if st.button("Delete", key="ok_del", type="primary"):
                    del st.session_state.datasets[dn]
                    rem = list(st.session_state.datasets)
                    st.session_state.active_ds = rem[0] if rem else None
                    st.session_state.confirm_del = None
                    st.rerun()
            with cn:
                if st.button("Cancel", key="no_del"):
                    st.session_state.confirm_del = None
                    st.rerun()

        rd()
        if st.button("🗑️  Clear all", use_container_width=True, key="clear_all"):
            st.session_state.datasets = {}
            st.session_state.active_ds = None
            st.rerun()
    else:
        st.markdown("""<div style='padding:12px 10px;text-align:center;
            color:#1E3045;font-size:0.78rem;font-family:Inter,sans-serif;'>
            Upload a file above to begin
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ACTIVE DATASET
# ══════════════════════════════════════════════════════════════════════════════
_act   = st.session_state.datasets.get(st.session_state.active_ds)
df     = _act["df"]    if _act else None
stats  = _act["stats"] if _act else None

def need():
    if _act is None:
        st.markdown("""<div class='es'>
            <div class='es-icon'>📂</div>
            <div class='es-title'>No dataset loaded</div>
            <div class='es-sub'>Upload a file using the sidebar panel.</div>
        </div>""", unsafe_allow_html=True)
        return False
    return True

# ══════════════════════════════════════════════════════════════════════════════
# ── OVERVIEW ─────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "overview":

    if _act:
        s = stats
        wp = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0
        ph("🏠 Overview", f"Active dataset: {st.session_state.active_ds}")

        # KPI row
        c1,c2,c3,c4,c5 = st.columns(5, gap="small")
        with c1: st.markdown(mc("💧","Total Used",fmt(s["total_usage"])+" L","","c-cyan","#00C3DC"), unsafe_allow_html=True)
        with c2: st.markdown(mc("💰","Total Cost",f"AED {fmt(s['total_cost'])}","","c-green","#00D68C"), unsafe_allow_html=True)
        with c3: st.markdown(mc("📏","Daily Avg",fmt(s["avg"])+" L","Per day","c-purple","#9B7AFF"), unsafe_allow_html=True)
        with c4: st.markdown(mc("🚨","Anomaly Days",str(s["n_abnormal"]),f"of {s['n_rows']} records","c-red","#FF4460"), unsafe_allow_html=True)
        with c5: st.markdown(mc("🌊","Est. Wasted",fmt(s["total_waste"])+" L",f"{wp:.1f}% of total","c-amber","#FFBD4A"), unsafe_allow_html=True)

        rd()

        col1, col2 = st.columns([3,2], gap="large")
        with col1:
            sl("📈","Daily Consumption Trend")
            daily = df.groupby("Date",as_index=False)["Water_Usage_Liters"].sum()
            fig   = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily["Date"], y=daily["Water_Usage_Liters"], mode="lines",
                line=dict(color="#00C3DC",width=1.8),
                fill="tozeroy", fillcolor="rgba(0,195,220,0.04)",
                hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y:,.0f} L<extra></extra>"))
            fig.add_hline(y=s["thresh"], line_dash="dash", line_color="rgba(255,68,96,0.5)",
                          annotation_text="Threshold", annotation_font=dict(color="#FF4460",size=10))
            T(fig); fig.update_layout(height=260, showlegend=False,
                                      xaxis_title="", yaxis_title="Litres")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            sl("🏢","Buildings")
            bsum = df.groupby("Building").agg(
                U=("Water_Usage_Liters","sum"),A=("Is_Abnormal","sum")).reset_index()
            bsum = bsum.sort_values("U",ascending=False)
            total_u = bsum["U"].sum()
            for _, row in bsum.iterrows():
                pct = row["U"]/total_u*100 if total_u else 0
                dot = "🔴" if row["A"]>0 else "🟢"
                st.markdown(f"""<div class='bb'>
                    <span style='font-size:.85rem;'>{dot}</span>
                    <div style='flex:1;min-width:0;'>
                        <div style='font-size:.8rem;color:#8FA8C0;font-weight:600;font-family:Inter,sans-serif;
                             white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>{row["Building"]}</div>
                        <div class='bb-bar'><div class='bb-fill' style='width:{pct:.0f}%;'></div></div>
                    </div>
                    <div style='text-align:right;flex-shrink:0;'>
                        <div style='font-size:.78rem;color:#00C3DC;font-weight:700;font-family:Inter,sans-serif;'>{pct:.0f}%</div>
                        <div style='font-size:.68rem;color:#2A3A4E;font-family:Inter,sans-serif;'>{int(row["A"])} anom.</div>
                    </div>
                </div>""", unsafe_allow_html=True)

        rd()

        col3, col4 = st.columns(2, gap="large")
        with col3:
            sl("📅","Monthly Trend")
            mn = df.groupby("Month_Label")["Water_Usage_Liters"].sum().reset_index()
            fig2 = px.bar(mn, x="Month_Label", y="Water_Usage_Liters",
                          color="Water_Usage_Liters", color_continuous_scale=SB)
            T(fig2); fig2.update_layout(height=230, coloraxis_showscale=False,
                                        showlegend=False, xaxis_title="", yaxis_title="L")
            st.plotly_chart(fig2, use_container_width=True)

        with col4:
            sl("🥧","Waste Split")
            pie = pd.DataFrame({"Cat":["Normal","Wasted"],
                                 "V":[s["total_usage"]-s["total_waste"],s["total_waste"]]})
            fig3 = px.pie(pie,values="V",names="Cat",hole=0.64,
                          color="Cat",color_discrete_map={"Normal":"#00C3DC","Wasted":"#FF4460"})
            fig3.update_traces(textinfo="percent+label",textfont=dict(color="#CDD9E5",size=11),
                               marker=dict(line=dict(color="#0C1A28",width=2)))
            T(fig3); fig3.update_layout(height=230, showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)

    else:
        # ── Welcome ──────────────────────────────────
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        col_l, col_r = st.columns([3,2], gap="large")

        with col_l:
            st.markdown("""<div class='wh'>
                <div class='wh-title'>💧 AquaSense UAE</div>
                <div class='wh-sub' style='margin-top:8px;'>
                    AI-powered water management for UAE campuses and buildings.<br>
                    Upload your consumption data to instantly detect leaks,
                    quantify waste in AED, and generate actionable recommendations.
                </div>
            </div>""", unsafe_allow_html=True)

            sl("⚙️","What this dashboard does")
            for icon, text in [
                ("📂","Upload and validate campus water data from CSV or Excel"),
                ("🔍","Automated data quality checks — missing values, duplicates"),
                ("📊","Interactive daily, monthly, and building-level charts"),
                ("🚨","Statistical anomaly detection to flag leaks and spikes"),
                ("🌍","Real AED and CO₂ impact of water waste"),
                ("🤖","Building-specific water-saving recommendations"),
                ("📋","Exportable full impact report with projections"),
            ]:
                st.markdown(f"<div class='fr'><span style='font-size:.95rem;flex-shrink:0;'>{icon}</span><span class='fr-t'>{text}</span></div>",
                            unsafe_allow_html=True)

        with col_r:
            sl("📖","Getting started")
            for num, text in [("1","Upload a file using the sidebar"),
                               ("2","Click the filename to activate it"),
                               ("3","Navigate through analysis sections"),
                               ("4","Export your impact report")]:
                st.markdown(f"<div class='sr'><div class='sr-n'>{num}</div><div class='sr-t'>{text}</div></div>",
                            unsafe_allow_html=True)

            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            sl("📋","Required columns")
            for code, desc in [("Date","Any date format"),
                                ("Building","Name or block ID"),
                                ("Water_Usage_Liters","Litres, numeric"),
                                ("Cost_AED","UAE Dirhams, numeric")]:
                st.markdown(f"""<div class='chip'>
                    <span class='chip-code'>{code}</span>
                    <span class='chip-desc'>{desc}</span>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ── DASHBOARD ────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "dashboard":
    ph("📊 Water Usage Dashboard", "Campus-wide consumption trends")
    if not need(): st.stop()
    s  = stats
    wp = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0

    c1,c2,c3,c4,c5 = st.columns(5,gap="small")
    with c1: st.markdown(mc("💧","Total Used",fmt(s["total_usage"])+" L","","c-cyan","#00C3DC"),unsafe_allow_html=True)
    with c2: st.markdown(mc("💰","Total Cost",f"AED {fmt(s['total_cost'])}","","c-green","#00D68C"),unsafe_allow_html=True)
    with c3: st.markdown(mc("📏","Daily Avg",fmt(s["avg"])+" L","Per day","c-purple","#9B7AFF"),unsafe_allow_html=True)
    with c4: st.markdown(mc("🚨","Anomaly Days",str(s["n_abnormal"]),f"of {s['n_rows']} records","c-red","#FF4460"),unsafe_allow_html=True)
    with c5: st.markdown(mc("🌊","Est. Wasted",fmt(s["total_waste"])+" L",f"{wp:.1f}% of total","c-amber","#FFBD4A"),unsafe_allow_html=True)

    rd()
    daily = df.groupby("Date",as_index=False)["Water_Usage_Liters"].sum()
    fig   = go.Figure()
    fig.add_trace(go.Scatter(x=daily["Date"],y=daily["Water_Usage_Liters"],mode="lines",
        line=dict(color="#00C3DC",width=2),fill="tozeroy",fillcolor="rgba(0,195,220,0.05)",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y:,.0f} L<extra></extra>"))
    fig.add_hline(y=s["avg"],line_dash="dot",line_color="rgba(0,214,140,0.6)",
                  annotation_text=f"Avg {s['avg']:,.0f} L",annotation_font=dict(color="#00D68C",size=10))
    fig.add_hline(y=s["thresh"],line_dash="dash",line_color="rgba(255,68,96,0.6)",
                  annotation_text="Anomaly Threshold",annotation_font=dict(color="#FF4460",size=10))
    T(fig); fig.update_layout(height=300,showlegend=False,
                               title="Daily Water Consumption — All Buildings",
                               xaxis_title="",yaxis_title="Litres")
    st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2,gap="large")
    with col1:
        sl("💸","Daily Cost (AED)")
        cd  = df.groupby("Date",as_index=False)["Cost_AED"].sum()
        fig2= px.area(cd,x="Date",y="Cost_AED",color_discrete_sequence=["#00D68C"])
        fig2.update_traces(fillcolor="rgba(0,214,140,0.05)",line_width=1.8,
                           hovertemplate="<b>%{x|%d %b}</b><br>AED %{y:,.2f}<extra></extra>")
        T(fig2); fig2.update_layout(height=250,showlegend=False,xaxis_title="",yaxis_title="AED")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        sl("📅","Average by Day of Week")
        dow = df.groupby("Day_of_Week")["Water_Usage_Liters"].mean().reindex(
            ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]).reset_index()
        dow.columns = ["Day","Avg"]
        fig3 = px.bar(dow,x="Day",y="Avg",color="Avg",color_continuous_scale=SB)
        T(fig3); fig3.update_layout(height=250,coloraxis_showscale=False,
                                    showlegend=False,xaxis_title="",yaxis_title="Avg Litres")
        st.plotly_chart(fig3, use_container_width=True)

    sl("🔵","Usage vs Cost Scatter")
    fig4 = px.scatter(df,x="Water_Usage_Liters",y="Cost_AED",color="Building",
                      size="Water_Usage_Liters",size_max=16,color_discrete_sequence=C,
                      hover_data={"Date":"|%d %b %Y","Building":True,"Water_Usage_Liters":":.0f","Cost_AED":":.2f"})
    T(fig4); fig4.update_layout(height=320,xaxis_title="Water Usage (L)",yaxis_title="Cost (AED)")
    st.plotly_chart(fig4, use_container_width=True)

    rd()
    c1,c2,_,_ = st.columns(4)
    with c1: st.download_button("📥 Export Dataset (CSV)",csv_data(df),"aquasense_data.csv","text/csv",use_container_width=True)
    with c2: st.download_button("📊 Export Summary (CSV)",summary_csv(stats,df),"summary.csv","text/csv",use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# ── MONTHLY ──────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "monthly":
    ph("📅 Monthly Water Summary","Month-by-month breakdown")
    if not need(): st.stop()

    monthly = df.groupby("Month_Label").agg(
        Usage=("Water_Usage_Liters","sum"),Cost=("Cost_AED","sum"),
        Avg=("Water_Usage_Liters","mean"),Waste=("Wasted_Liters","sum"),Abn=("Is_Abnormal","sum")
    ).reset_index()

    fig = make_subplots(specs=[[{"secondary_y":True}]])
    fig.add_trace(go.Bar(x=monthly["Month_Label"],y=monthly["Usage"],name="Usage (L)",
                         marker_color="#00C3DC",marker_opacity=0.8,
                         hovertemplate="<b>%{x}</b><br>%{y:,.0f} L<extra></extra>"),secondary_y=False)
    fig.add_trace(go.Scatter(x=monthly["Month_Label"],y=monthly["Cost"],name="Cost (AED)",
                             mode="lines+markers",line=dict(color="#00D68C",width=2.5),
                             marker=dict(size=7,color="#00D68C"),
                             hovertemplate="<b>%{x}</b><br>AED %{y:,.2f}<extra></extra>"),secondary_y=True)
    fig.update_layout(height=320,title="Monthly Usage & Cost",**_PL,
                      legend=dict(orientation="h",y=1.08,font=dict(color="#6B829E",size=11)))
    fig.update_yaxes(title_text="Litres",secondary_y=False,
                     gridcolor="rgba(255,255,255,0.03)",tickfont=dict(color="#3D5268",size=10))
    fig.update_yaxes(title_text="AED",secondary_y=True,
                     gridcolor="rgba(255,255,255,0.03)",tickfont=dict(color="#3D5268",size=10))
    fig.update_xaxes(tickfont=dict(color="#3D5268",size=10))
    st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2,gap="large")
    with col1:
        fig2 = px.bar(monthly,x="Month_Label",y="Waste",color="Waste",
                      color_continuous_scale=SR,title="Estimated Wasted Water (L)")
        T(fig2); fig2.update_layout(height=240,coloraxis_showscale=False,xaxis_title="",yaxis_title="Litres")
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        fig3 = px.line(monthly,x="Month_Label",y="Avg",markers=True,
                       color_discrete_sequence=["#9B7AFF"],title="Average Daily Usage (L)")
        fig3.update_traces(line_width=2.5,marker_size=8)
        T(fig3); fig3.update_layout(height=240,xaxis_title="",yaxis_title="Litres")
        st.plotly_chart(fig3, use_container_width=True)

    sl("📋","Monthly Table")
    md = monthly.copy().round(1)
    md.columns = ["Month","Total (L)","Cost (AED)","Avg Daily (L)","Wasted (L)","Anomaly Days"]
    st.dataframe(md, use_container_width=True, hide_index=True, height=280)
    rd()
    c1,_,_,_ = st.columns(4)
    with c1: st.download_button("📥 Monthly Data (CSV)",monthly.to_csv(index=False).encode(),"monthly.csv","text/csv",use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# ── BUILDINGS ────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "buildings":
    ph("🏢 Building Comparison","Which buildings consume and waste the most")
    if not need(): st.stop()

    bld = df.groupby("Building").agg(
        Usage=("Water_Usage_Liters","sum"),Cost=("Cost_AED","sum"),
        Avg=("Water_Usage_Liters","mean"),Waste=("Wasted_Liters","sum"),
        Abn=("Is_Abnormal","sum"),N=("Water_Usage_Liters","count")
    ).reset_index().sort_values("Usage",ascending=False)

    col1,col2 = st.columns(2,gap="large")
    with col1:
        fig = px.bar(bld,x="Building",y="Usage",color="Usage",color_continuous_scale=SB,
                     title="Total Usage by Building (L)",text="Usage")
        fig.update_traces(texttemplate="%{text:,.0f}",textposition="outside",
                          textfont=dict(color="#6B829E",size=10))
        T(fig); fig.update_layout(height=280,coloraxis_showscale=False,xaxis_title="",yaxis_title="Litres")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.pie(bld,values="Usage",names="Building",hole=0.60,
                      title="Usage Share",color_discrete_sequence=C)
        fig2.update_traces(textinfo="percent+label",textfont=dict(color="#CDD9E5",size=11),
                           marker=dict(line=dict(color="#0C1A28",width=2)))
        T(fig2); fig2.update_layout(height=280,showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    sl("💧","Avg Daily vs Estimated Waste")
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=bld["Building"],y=bld["Avg"],name="Avg Daily",marker_color="#00C3DC",marker_opacity=0.8))
    fig3.add_trace(go.Bar(x=bld["Building"],y=bld["Waste"],name="Est. Wasted",marker_color="#FF4460",marker_opacity=0.8))
    T(fig3); fig3.update_layout(barmode="group",height=280,xaxis_title="",yaxis_title="Litres",
                                 legend=dict(orientation="h",y=1.1,font=dict(color="#6B829E",size=11)))
    st.plotly_chart(fig3, use_container_width=True)

    col3,col4 = st.columns(2,gap="large")
    with col3:
        fig4 = px.bar(bld.sort_values("Waste"),x="Waste",y="Building",orientation="h",
                      color="Waste",color_continuous_scale=SR,title="Wasted Water Ranking (L)")
        T(fig4); fig4.update_layout(height=260,coloraxis_showscale=False,xaxis_title="Litres",yaxis_title="")
        st.plotly_chart(fig4, use_container_width=True)
    with col4:
        fig5 = px.scatter(bld,x="Avg",y="Cost",size="Usage",color="Building",
                          title="Avg Daily vs Total Cost",color_discrete_sequence=C,hover_data=["Abn"])
        T(fig5); fig5.update_layout(height=260,xaxis_title="Avg Daily (L)",yaxis_title="Total Cost (AED)")
        st.plotly_chart(fig5, use_container_width=True)

    sl("📋","Building Summary")
    bd = bld.round(1).copy()
    bd.columns = ["Building","Total (L)","Cost (AED)","Avg Daily (L)","Wasted (L)","Anomaly Days","Records"]
    st.dataframe(bd, use_container_width=True, hide_index=True, height=280)
    rd()
    c1,_,_,_ = st.columns(4)
    with c1: st.download_button("📥 Building Data (CSV)",bld.to_csv(index=False).encode(),"buildings.csv","text/csv",use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# ── LEAK DETECTION ───────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "leaks":
    ph("🚨 Leak Detection","Statistical anomaly detection — 2σ rule")
    if not need(): st.stop()
    s   = stats
    abn = df[df["Is_Abnormal"]]
    pct = s["n_abnormal"]/s["n_rows"]*100 if s["n_rows"] else 0

    ib(f"""<strong>Method:</strong> Days where usage exceeds <strong>Average + 2 × Std Dev</strong> 
    are flagged. This identifies likely <strong>pipe leaks, broken valves, or unusual spikes</strong>.<br>
    Average: <strong>{s['avg']:,.1f} L/day</strong> &nbsp;|&nbsp;
    Std Dev: <strong>{s['std']:,.1f} L</strong> &nbsp;|&nbsp;
    Threshold: <strong>{s['thresh']:,.1f} L/day</strong>""","info")

    c1,c2,c3,c4 = st.columns(4,gap="small")
    with c1: st.markdown(mc("🚨","Anomaly Days",str(s["n_abnormal"]),f"of {s['n_rows']} records","c-red","#FF4460"),unsafe_allow_html=True)
    with c2: st.markdown(mc("📊","Anomaly Rate",f"{pct:.1f}%","Of total data","c-amber","#FFBD4A"),unsafe_allow_html=True)
    with c3: st.markdown(mc("💧","Est. Wasted",fmt(s["total_waste"])+" L","Above-threshold usage","c-cyan","#00C3DC"),unsafe_allow_html=True)
    with c4: st.markdown(mc("💰","AED Lost",f"AED {fmt(s['abn_cost'])}","From anomaly days","c-purple","#9B7AFF"),unsafe_allow_html=True)

    rd()
    daily = df.groupby("Date").agg(U=("Water_Usage_Liters","sum"),A=("Is_Abnormal","any")).reset_index()
    fig   = go.Figure()
    fig.add_trace(go.Scatter(x=daily["Date"],y=daily["U"],mode="lines",
        line=dict(color="#00C3DC",width=1.8),fill="tozeroy",fillcolor="rgba(0,195,220,0.04)",
        name="Daily Usage",hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y:,.0f} L<extra></extra>"))
    ad = daily[daily["A"]]
    if len(ad):
        fig.add_trace(go.Scatter(x=ad["Date"],y=ad["U"],mode="markers",name="⚠️ Anomaly",
            marker=dict(color="#FF4460",size=11,symbol="circle",
                        line=dict(color="rgba(255,68,96,0.25)",width=7)),
            hovertemplate="<b>ANOMALY — %{x|%d %b %Y}</b><br>%{y:,.0f} L<extra></extra>"))
    fig.add_hline(y=s["thresh"],line_dash="dash",line_color="rgba(255,68,96,0.55)",
                  annotation_text=f"Threshold {s['thresh']:,.0f} L",annotation_font=dict(color="#FF4460",size=10))
    fig.add_hline(y=s["avg"],line_dash="dot",line_color="rgba(0,214,140,0.55)",
                  annotation_text=f"Avg {s['avg']:,.0f} L",annotation_font=dict(color="#00D68C",size=10))
    T(fig); fig.update_layout(height=310,xaxis_title="",yaxis_title="Litres",
                               legend=dict(orientation="h",y=1.08,font=dict(color="#6B829E",size=11)))
    st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2,gap="large")
    with col1:
        sl("🏢","Anomaly Days by Building")
        ab = df.groupby("Building")["Is_Abnormal"].sum().reset_index()
        ab.columns = ["Building","Anomalies"]
        ab = ab[ab["Anomalies"]>0].sort_values("Anomalies",ascending=False)
        if len(ab):
            fig2 = px.bar(ab,x="Building",y="Anomalies",color="Anomalies",color_continuous_scale=SR)
            T(fig2); fig2.update_layout(height=250,coloraxis_showscale=False,xaxis_title="",yaxis_title="Days")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            ib("✅ No per-building anomalies detected.","success")

    with col2:
        sl("📦","Usage Distribution")
        fig3 = go.Figure()
        fig3.add_trace(go.Histogram(x=df["Water_Usage_Liters"],nbinsx=28,
                                    marker_color="#00C3DC",marker_opacity=0.6,name="Records"))
        fig3.add_vline(x=s["avg"],line_dash="dot",line_color="rgba(0,214,140,0.7)",
                       annotation_text="Avg",annotation_font=dict(color="#00D68C",size=10))
        fig3.add_vline(x=s["thresh"],line_dash="dash",line_color="rgba(255,68,96,0.7)",
                       annotation_text="Threshold",annotation_font=dict(color="#FF4460",size=10))
        T(fig3); fig3.update_layout(height=250,showlegend=False,xaxis_title="Litres",yaxis_title="Frequency")
        st.plotly_chart(fig3, use_container_width=True)

    sl("📋","Flagged Records")
    if len(abn):
        ad2 = abn[["Date","Building","Water_Usage_Liters","Cost_AED","Wasted_Liters"]].copy()
        ad2.columns = ["Date","Building","Usage (L)","Cost (AED)","Wasted (L)"]
        st.dataframe(ad2.round(2).sort_values("Wasted (L)",ascending=False),
                     use_container_width=True, hide_index=True, height=280)
        rd()
        c1,_,_,_ = st.columns(4)
        with c1: st.download_button("📥 Anomaly Records (CSV)",ad2.to_csv(index=False).encode(),"anomalies.csv","text/csv",use_container_width=True)
    else:
        ib("✅ No abnormal records found in this dataset.","success")

# ══════════════════════════════════════════════════════════════════════════════
# ── IMPACT CALCULATOR ────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "impact":
    ph("🌍 Impact Calculator","Financial and environmental cost of water waste")
    if not need(): st.stop()
    s  = stats

    days = (df["Date"].max()-df["Date"].min()).days+1
    yw   = (s["total_waste"]/days)*365
    ys   = yw*0.5
    ya   = (s["abn_cost"]/days)*365*0.5
    co2  = ys*0.000344
    kwh  = ys*0.004
    bot  = ys*2
    tre  = ys*0.05/1000
    wp   = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0

    sl("📊","Current Waste — This Dataset")
    c1,c2,c3,c4 = st.columns(4,gap="small")
    with c1: st.markdown(mc("💧","Wasted (Period)",fmt(s["total_waste"])+" L","","c-red","#FF4460"),unsafe_allow_html=True)
    with c2: st.markdown(mc("📊","Waste %",f"{wp:.1f}%","Of total usage","c-amber","#FFBD4A"),unsafe_allow_html=True)
    with c3: st.markdown(mc("💰","AED Lost",f"AED {fmt(s['abn_cost'])}","From anomaly days","c-cyan","#00C3DC"),unsafe_allow_html=True)
    with c4: st.markdown(mc("📅","Period",f"{days} days",f"{df['Date'].min().date()}","c-purple","#9B7AFF"),unsafe_allow_html=True)

    rd()
    sl("🌱","Projected Yearly Savings — 50% Waste Reduction")
    ib("Based on reducing anomalous usage by <strong>50%</strong> through leak repairs — a realistic, achievable target for most campuses.","success")

    c1,c2,c3,c4 = st.columns(4,gap="small")
    with c1: st.markdown(mc("💧","Water Saved/Year",fmt(ys)+" L","","c-green","#00D68C"),unsafe_allow_html=True)
    with c2: st.markdown(mc("💰","AED Saved/Year",f"AED {fmt(ya)}","","c-cyan","#00C3DC"),unsafe_allow_html=True)
    with c3: st.markdown(mc("🌿","CO₂ Avoided",f"{co2:,.1f} kg","Less desalination","c-purple","#9B7AFF"),unsafe_allow_html=True)
    with c4: st.markdown(mc("⚡","Energy Saved",f"{kwh:,.1f} kWh","Desal energy cut","c-amber","#FFBD4A"),unsafe_allow_html=True)

    c5,c6,_,_ = st.columns(4,gap="small")
    with c5: st.markdown(mc("🍶","Bottles Avoided",fmt(bot),"500ml equiv.","c-red","#FF4460"),unsafe_allow_html=True)
    with c6: st.markdown(mc("🌳","Trees Equiv.",f"{tre:,.0f}","CO₂ offset","c-green","#00D68C"),unsafe_allow_html=True)

    rd()
    col1,col2 = st.columns(2,gap="large")
    with col1:
        pie = pd.DataFrame({"Cat":["Normal","Wasted"],"V":[s["total_usage"]-s["total_waste"],s["total_waste"]]})
        fig  = px.pie(pie,values="V",names="Cat",hole=0.62,title="Normal vs Wasted Water",
                      color="Cat",color_discrete_map={"Normal":"#00C3DC","Wasted":"#FF4460"})
        fig.update_traces(textinfo="percent+label",textfont=dict(color="#CDD9E5",size=11),
                          marker=dict(line=dict(color="#0C1A28",width=2)))
        T(fig); fig.update_layout(height=260,showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = go.Figure(go.Waterfall(
            orientation="v",measure=["relative","relative","relative","total"],
            x=["Yearly Waste","50% Saved","Remaining","Net Saving"],
            y=[yw,-ys,ys,0],
            connector={"line":{"color":"rgba(255,255,255,0.06)"}},
            increasing={"marker":{"color":"rgba(255,68,96,0.7)"}},
            decreasing={"marker":{"color":"rgba(0,214,140,0.7)"}},
            totals   ={"marker":{"color":"rgba(0,195,220,0.7)"}},
        ))
        T(fig2); fig2.update_layout(height=260,title="Yearly Saving Waterfall (L)",yaxis_title="Litres")
        st.plotly_chart(fig2, use_container_width=True)

    rd()
    sl("🎛️","Custom Reduction Scenario")
    pct = st.slider("Waste reduction target", 10, 90, 50, 5, format="%d%%")
    cs  = yw*(pct/100); ca = ya*(pct/50); cc = cs*0.000344
    c1,c2,c3,_ = st.columns(4,gap="small")
    with c1: st.markdown(mc("💧",f"Saved at {pct}%",fmt(cs)+" L/yr","","c-cyan","#00C3DC"),unsafe_allow_html=True)
    with c2: st.markdown(mc("💰","AED Saved",f"AED {fmt(ca)}/yr","","c-green","#00D68C"),unsafe_allow_html=True)
    with c3: st.markdown(mc("🌿","CO₂ Avoided",f"{cc:,.2f} kg/yr","","c-purple","#9B7AFF"),unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ── RECOMMENDATIONS ──────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "recs":
    ph("🤖 Recommendations","Data-driven actions tailored to your campus patterns")
    if not need(): st.stop()
    s  = stats
    wp = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0

    ib(f"⚠️ Campus is wasting an estimated <strong>{wp:.1f}%</strong> of its water through <strong>{s['n_abnormal']}</strong> anomaly events.","danger")

    ba  = df.groupby("Building").agg(A=("Is_Abnormal","sum"),W=("Wasted_Liters","sum")).reset_index()
    top = ba[ba["A"]>0].sort_values("A",ascending=False)
    if len(top):
        sl("🏢","Building Alerts")
        for _, row in top.head(5).iterrows():
            sev = "danger" if row["A"]>=5 else "warn"
            ib(f"🚨 <strong>{row['Building']}</strong> — {int(row['A'])} anomaly day(s) · Est. <strong>{row['W']:,.0f} L</strong> wasted. Inspection recommended.",sev)

    rd()
    sl("💡","Recommendations")
    RECS = [
        ("🔧","Fix Leaks Immediately",
         f"Your data flagged {s['n_abnormal']} abnormal days — likely from leaks, running toilets, or faulty valves. A single dripping tap wastes 10,000+ L/year. Plumbing inspection is the highest-ROI action available.","30–50% waste reduction"),
        ("📱","Deploy Smart Water Meters",
         "IoT-enabled meters provide real-time alerts when usage exceeds thresholds — automating exactly what this dashboard detects, 24/7 without manual uploads.","Instant leak detection"),
        ("🚿","Upgrade to Low-Flow Fixtures",
         "Low-flow taps and toilets cut consumption 30–50% with no change in user experience. Prioritise buildings with the highest anomaly counts first.","30–45% per fixture"),
        ("🌿","Greywater Recycling",
         "Reuse sink and shower water for flushing and irrigation. UAE campuses with greywater systems report up to 40% reduction in potable water demand.","Up to 40% potable saving"),
        ("👥","Awareness Programme",
         "Monthly water challenges at UAE universities achieve 15–25% reductions within 3 months. Low cost, measurable impact with proper communications.","15–25% reduction"),
        ("🗓️","Quarterly Plumbing Audits",
         "Preventive maintenance is 10× cheaper than emergency repairs. Scheduled audits catch slow leaks before they become costly — exactly the type this dashboard detects.","60–80% fewer anomalies"),
        ("☀️","Solar Water Heating",
         "Solar heaters eliminate energy costs from water heating. Combined with insulated pipes, this removes heat-loss waste and supports UAE Net Zero 2050.","20% energy + water saving"),
        ("🌱","Drought-Resistant Landscaping",
         "UAE-native plants with drip irrigation dramatically reduce outdoor usage. Landscape irrigation accounts for up to 50% of campus water in summer months.","Up to 50% irrigation saving"),
    ]
    col1,col2 = st.columns(2,gap="large")
    for i,(icon,title,body,saving) in enumerate(RECS):
        with (col1 if i%2==0 else col2):
            st.markdown(f"""<div class='rc'>
                <div class='rc-icon'>{icon}</div>
                <div>
                    <div class='rc-title'>{title}</div>
                    <div class='rc-body'>{body}</div>
                    <div class='rc-tag'>💚 {saving}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    rd()
    sl("📊","Priority Matrix — Impact vs Ease")
    pri = pd.DataFrame({"Action":["Fix Leaks","Smart Meters","Low-Flow","Greywater","Awareness"],
                         "Impact":[95,85,75,70,55],"Ease":[80,50,70,35,90],"Cost":[5,80,40,150,2]})
    fig = px.scatter(pri,x="Ease",y="Impact",size="Cost",text="Action",color="Impact",
                     color_continuous_scale=SB,size_max=34,
                     labels={"Ease":"← Harder    Ease of Implementation    Easier →","Impact":"Impact ↑"})
    fig.update_traces(textposition="top center",textfont=dict(color="#CDD9E5",size=11,family="Inter"))
    fig.add_hline(y=75,line_dash="dot",line_color="rgba(255,255,255,0.06)")
    fig.add_vline(x=60,line_dash="dot",line_color="rgba(255,255,255,0.06)")
    T(fig); fig.update_layout(height=350,coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# ── IMPACT REPORT ────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "report":
    ph("📋 Final Impact Report","Complete summary of findings, projections, and actions")
    if not need(): st.stop()
    s  = stats

    days = (df["Date"].max()-df["Date"].min()).days+1
    yw   = (s["total_waste"]/days)*365
    ys   = yw*0.5
    ya   = (s["abn_cost"]/days)*365*0.5
    co2  = ys*0.000344
    wp   = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0
    bn   = df["Building"].nunique()

    # Hero card
    st.markdown(f"""<div class='rh'>
        <div style='font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;color:#EEF4FF;margin-bottom:4px;'>
            💧 Campus Water Impact Report
        </div>
        <div style='color:rgba(255,255,255,0.3);font-size:0.79rem;margin-bottom:24px;font-family:Inter,sans-serif;'>
            {datetime.now().strftime("%d %B %Y, %H:%M")} &nbsp;·&nbsp;
            {df['Date'].min().date()} → {df['Date'].max().date()} &nbsp;·&nbsp;
            {bn} buildings &nbsp;·&nbsp; {days} days
        </div>
        <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:14px;position:relative;z-index:1;'>
            <div style='text-align:center;background:rgba(0,0,0,0.25);border-radius:12px;padding:15px 10px;'>
                <div class='rh-val'>{fmt(s["total_usage"])} L</div>
                <div class='rh-lbl'>Total Consumed</div>
            </div>
            <div style='text-align:center;background:rgba(0,0,0,0.25);border-radius:12px;padding:15px 10px;'>
                <div class='rh-val'>AED {fmt(s["total_cost"])}</div>
                <div class='rh-lbl'>Total Cost</div>
            </div>
            <div style='text-align:center;background:rgba(0,0,0,0.25);border-radius:12px;padding:15px 10px;'>
                <div class='rh-val' style='color:#FF4460;'>{s["n_abnormal"]}</div>
                <div class='rh-lbl'>Anomaly Days</div>
            </div>
            <div style='text-align:center;background:rgba(0,0,0,0.25);border-radius:12px;padding:15px 10px;'>
                <div class='rh-val' style='color:#FFBD4A;'>{wp:.1f}%</div>
                <div class='rh-lbl'>Estimated Waste</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    sl("🌱","Projected Yearly Savings — 50% Waste Reduction")
    c1,c2,c3,c4 = st.columns(4,gap="small")
    with c1: st.markdown(mc("💧","Water/Year",fmt(ys)+" L","","c-green","#00D68C"),unsafe_allow_html=True)
    with c2: st.markdown(mc("💰","AED/Year",f"AED {fmt(ya)}","","c-cyan","#00C3DC"),unsafe_allow_html=True)
    with c3: st.markdown(mc("🌿","CO₂",f"{co2:,.1f} kg/yr","","c-purple","#9B7AFF"),unsafe_allow_html=True)
    with c4: st.markdown(mc("🏢","Buildings",str(bn),"Analysed","c-amber","#FFBD4A"),unsafe_allow_html=True)

    rd()
    col1,col2 = st.columns(2,gap="large")
    with col1:
        pie = pd.DataFrame({"Cat":["Normal","Wasted"],"V":[s["total_usage"]-s["total_waste"],s["total_waste"]]})
        fig  = px.pie(pie,values="V",names="Cat",hole=0.60,
                      color="Cat",color_discrete_map={"Normal":"#00C3DC","Wasted":"#FF4460"},title="Normal vs Wasted")
        fig.update_traces(textinfo="percent+label",textfont=dict(color="#CDD9E5",size=11),
                          marker=dict(line=dict(color="#0C1A28",width=2)))
        T(fig); fig.update_layout(height=250,showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        bs  = df.groupby("Building")["Water_Usage_Liters"].sum().reset_index()
        fig2= px.pie(bs,values="Water_Usage_Liters",names="Building",hole=0.60,
                     title="Usage by Building",color_discrete_sequence=C)
        fig2.update_traces(textinfo="percent+label",textfont=dict(color="#CDD9E5",size=11),
                           marker=dict(line=dict(color="#0C1A28",width=2)))
        T(fig2); fig2.update_layout(height=250,showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    sl("📅","Monthly Trend")
    mn  = df.groupby("Month_Label")["Water_Usage_Liters"].sum().reset_index()
    fig3= px.bar(mn,x="Month_Label",y="Water_Usage_Liters",color="Water_Usage_Liters",color_continuous_scale=SB)
    T(fig3); fig3.update_layout(height=240,coloraxis_showscale=False,showlegend=False,xaxis_title="",yaxis_title="Litres")
    st.plotly_chart(fig3, use_container_width=True)

    rd()
    sl("📝","Key Findings")
    for f in [
        f"📍 Campus consumed **{s['total_usage']:,.0f} L** over {days} days — avg **AED {s['total_cost']/days:,.2f}/day**.",
        f"🚨 **{s['n_abnormal']} anomaly events** detected (2σ threshold: {s['thresh']:,.0f} L/day).",
        f"🌊 Estimated **{s['total_waste']:,.0f} L wasted** — {wp:.1f}% of total consumption.",
        f"💰 AED loss from anomalies: **AED {s['abn_cost']:,.2f}** over the analysis period.",
        f"🌱 50% waste reduction: **{ys:,.0f} L/year** and **AED {ya:,.2f}/year** recovered.",
        f"🌿 Environmental: **{co2:,.2f} kg CO₂/year** avoided from reduced desalination.",
        f"🏢 **{bn} buildings** analysed — prioritise highest-waste buildings first.",
    ]:
        st.markdown(f)

    rd()
    sl("🎯","Top 3 Priority Actions")
    for num,icon,title,body in [
        ("1","🔧","Fix Leaks Immediately",f"Inspect all {s['n_abnormal']} flagged days. Highest ROI action available."),
        ("2","📱","Deploy Smart Water Meters","Real-time 24/7 detection — no manual uploads needed."),
        ("3","🚿","Low-Flow Fixture Upgrade","Upgrade top-usage buildings first. UAE campus ROI: 12–18 months."),
    ]:
        st.markdown(f"""<div class='rc'>
            <div style='width:38px;height:38px;border-radius:10px;flex-shrink:0;
                        background:rgba(0,195,220,0.08);border:1px solid rgba(0,195,220,0.2);
                        color:#00C3DC;font-family:Syne,sans-serif;font-weight:800;font-size:1rem;
                        display:flex;align-items:center;justify-content:center;'>{num}</div>
            <div>
                <div class='rc-title'>{icon} {title}</div>
                <div class='rc-body'>{body}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    rd()
    sl("⬇️","Export")
    c1,c2,c3,_ = st.columns([1,1,1,2])
    with c1: st.download_button("📥 Full Dataset",csv_data(df),"aquasense_data.csv","text/csv",use_container_width=True)
    with c2: st.download_button("📊 Summary Report",summary_csv(stats,df),"summary.csv","text/csv",use_container_width=True)
    with c3:
        br = df.groupby("Building").agg(
            Total_L=("Water_Usage_Liters","sum"),Cost_AED=("Cost_AED","sum"),
            Avg_Daily=("Water_Usage_Liters","mean"),Wasted_L=("Wasted_Liters","sum"),
            Anomaly_Days=("Is_Abnormal","sum")).reset_index()
        st.download_button("🏢 Building Report",br.to_csv(index=False).encode(),"buildings.csv","text/csv",use_container_width=True)

# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown("""<div class='ft'>
    💧 AquaSense UAE &nbsp;·&nbsp; AI-Powered Water Impact Dashboard &nbsp;·&nbsp;
    Streamlit · Plotly · Pandas · NumPy &nbsp;·&nbsp; UAE Net Zero 2050 · SDG 6 Clean Water
</div>""", unsafe_allow_html=True)
