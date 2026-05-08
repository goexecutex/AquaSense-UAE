"""
AquaSense UAE: AI-Powered Water Impact Dashboard for Sustainable Campuses
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
    page_title="AquaSense UAE | Smart Water Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS — all colours explicit, no theme variable inheritance ────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap');

[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
.main .block-container {
    background: #F0F8FC !important;
    max-width: 1300px !important;
    padding-top: 1.4rem !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg,#003D52 0%,#005670 60%,#0A7EA4 100%) !important;
}
[data-testid="stSidebar"] * { color: #DFF0F8 !important; }
[data-testid="stSidebar"] .stRadio > label { display: none; }

h1,h2,h3,h4 { font-family:'Syne',sans-serif !important; color:#003D52 !important; }

.hero {
    background: linear-gradient(135deg,#003D52 0%,#0A7EA4 55%,#00C5A1 100%);
    border-radius:20px; padding:42px 46px 36px; margin-bottom:24px;
    position:relative; overflow:hidden;
}
.hero::before {
    content:''; position:absolute; top:-70px; right:-70px;
    width:290px; height:290px; border-radius:50%; background:rgba(255,255,255,0.05);
}
.hero-title {
    font-family:'Syne',sans-serif; font-size:2.4rem; font-weight:800;
    color:#FFFFFF; margin:0 0 8px; line-height:1.15; position:relative; z-index:1;
}
.hero-sub { font-size:1rem; color:rgba(255,255,255,0.82); margin:0 0 18px; position:relative; z-index:1; }
.badge-row { display:flex; gap:10px; flex-wrap:wrap; position:relative; z-index:1; }
.badge {
    background:rgba(255,255,255,0.16); border:1px solid rgba(255,255,255,0.3);
    border-radius:30px; padding:5px 14px; font-size:0.77rem;
    color:#FFFFFF; font-family:'DM Sans',sans-serif; font-weight:600;
}

.stitle {
    font-family:'Syne',sans-serif; font-size:1.35rem; font-weight:700;
    color:#003D52; margin:26px 0 14px; display:flex; align-items:center; gap:10px;
}
.stitle-dot { display:inline-block; width:10px; height:10px; border-radius:50%; background:#00C5A1; flex-shrink:0; }

.mcard {
    background:#FFFFFF; border-radius:16px; padding:20px 20px 16px;
    border:1px solid #D0E8F0; box-shadow:0 2px 12px rgba(10,126,164,0.08);
    transition:transform .18s,box-shadow .18s;
}
.mcard:hover { transform:translateY(-3px); box-shadow:0 8px 24px rgba(10,126,164,0.15); }
.mcard-icon  { font-size:1.5rem; margin-bottom:7px; }
.mcard-label {
    font-size:0.71rem; color:#5A7A85; text-transform:uppercase;
    letter-spacing:.9px; margin-bottom:3px; font-weight:600; font-family:'DM Sans',sans-serif;
}
.mcard-value { font-family:'Syne',sans-serif; font-size:1.58rem; font-weight:700; color:#003D52; line-height:1; }
.mcard-delta { font-size:0.76rem; margin-top:5px; color:#5A7A85; font-family:'DM Sans',sans-serif; }
.ml-blue  { border-left:4px solid #0A7EA4; }
.ml-green { border-left:4px solid #00C5A1; }
.ml-red   { border-left:4px solid #E84855; }
.ml-warn  { border-left:4px solid #F5A623; }
.ml-deep  { border-left:4px solid #003D52; }

/* EXPLICIT colours — never inherit from dark theme */
.box { border-radius:12px; padding:14px 18px; margin:12px 0; font-size:0.9rem; font-family:'DM Sans',sans-serif; line-height:1.6; }
.box b, .box strong { font-weight:700; }
.box-info    { background:#E3F4FD; border-left:4px solid #0A7EA4; color:#0C2D3A; }
.box-success { background:#E4F9F3; border-left:4px solid #00C5A1; color:#074D3A; }
.box-warn    { background:#FFF6E2; border-left:4px solid #F5A623; color:#5C3D00; }
.box-danger  { background:#FDECEA; border-left:4px solid #E84855; color:#6B1010; }

/* Step rows — EXPLICIT text colour */
.step-row {
    display:flex; align-items:center; gap:14px;
    padding:10px 14px; background:#FFFFFF; border-radius:12px;
    margin-bottom:8px; border:1px solid #D0E8F0;
}
.step-num {
    width:32px; height:32px; border-radius:50%; flex-shrink:0;
    background:linear-gradient(135deg,#0A7EA4,#00C5A1); color:#FFFFFF;
    font-family:'Syne',sans-serif; font-weight:800; font-size:0.88rem;
    display:flex; align-items:center; justify-content:center;
}
.step-label { font-size:0.88rem; color:#1A2E35; font-weight:500; font-family:'DM Sans',sans-serif; }

.feat-row { display:flex; align-items:flex-start; gap:12px; padding:9px 0; border-bottom:1px solid #D0E8F0; }
.feat-text { font-size:0.88rem; color:#1A2E35; font-family:'DM Sans',sans-serif; line-height:1.45; }

.acard { background:#FFFFFF; border-radius:14px; padding:16px 18px; border:1px solid #D0E8F0; margin-bottom:12px; }
.acard-title { font-family:'Syne',sans-serif; font-size:1.0rem; font-weight:700; color:#003D52; margin:5px 0 2px; }
.acard-sub   { font-size:0.8rem; color:#5A7A85; font-family:'DM Sans',sans-serif; }

.rec { background:#FFFFFF; border-radius:14px; padding:18px 20px; border:1px solid #D0E8F0; margin-bottom:13px; display:flex; gap:16px; align-items:flex-start; }
.rec-icon { width:44px; height:44px; border-radius:12px; flex-shrink:0; background:linear-gradient(135deg,#0A7EA4,#00C5A1); display:flex; align-items:center; justify-content:center; font-size:1.25rem; }
.rec-title { font-family:'Syne',sans-serif; font-size:0.95rem; font-weight:700; color:#003D52; margin-bottom:4px; }
.rec-body  { font-size:0.84rem; color:#3A5A65; line-height:1.55; font-family:'DM Sans',sans-serif; }
.rec-tag   { display:inline-block; background:#E4F9F3; color:#075C45; border-radius:20px; padding:3px 11px; font-size:0.73rem; font-weight:700; margin-top:6px; font-family:'DM Sans',sans-serif; }

.report-hero { background:linear-gradient(135deg,#003D52,#005670,#0A7EA4); border-radius:20px; padding:34px 38px; margin-bottom:18px; }
.report-val  { font-family:'Syne',sans-serif; font-size:1.9rem; font-weight:800; color:#00C5A1; }
.report-lbl  { font-size:0.78rem; color:rgba(255,255,255,0.7); margin-top:3px; font-family:'DM Sans',sans-serif; }

.divider { height:2px; border:none; margin:24px 0; background:linear-gradient(90deg,#00C5A1,rgba(0,197,161,0)); }

.stProgress > div > div > div { background:linear-gradient(90deg,#0A7EA4,#00C5A1) !important; }
[data-testid="stFileUploader"] section { border:2px dashed #0A7EA4 !important; border-radius:14px !important; background:#F0F8FC !important; }
[data-testid="stDataFrame"] { border-radius:12px; overflow:hidden; }
.stDownloadButton button { background:linear-gradient(135deg,#0A7EA4,#00C5A1) !important; color:#FFFFFF !important; border:none !important; border-radius:10px !important; font-weight:600 !important; }

.footer { text-align:center; padding:20px; color:#5A7A85; font-size:0.77rem; border-top:1px solid #D0E8F0; margin-top:36px; font-family:'DM Sans',sans-serif; }
</style>
""", unsafe_allow_html=True)

# ─── Plotly theme ─────────────────────────────────────────────────────────────
COLORS = ["#0A7EA4","#00C5A1","#003D52","#F5A623","#E84855",
          "#6EC6E6","#4BC8A8","#2D6E8A","#FFD166","#EF8354"]
_L = dict(
    font_family="DM Sans", plot_bgcolor="white", paper_bgcolor="white",
    margin=dict(l=20,r=20,t=44,b=20), colorway=COLORS,
    title_font=dict(family="Syne",size=15,color="#003D52"),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)
def theme(fig):
    fig.update_layout(**_L)
    fig.update_xaxes(showgrid=True,gridcolor="#E8F3F8",linecolor="#D0E8F0",tickfont_color="#5A7A85")
    fig.update_yaxes(showgrid=True,gridcolor="#E8F3F8",linecolor="#D0E8F0",tickfont_color="#5A7A85")
    return fig

# ─── Helpers ──────────────────────────────────────────────────────────────────
def fmt(n, d=0):
    if n >= 1_000_000: return f"{n/1_000_000:.2f}M"
    if n >= 1_000:     return f"{n/1_000:.1f}K"
    return f"{n:,.{d}f}"

def mcard(icon, label, value, delta="", cls="ml-blue"):
    dh = f"<div class='mcard-delta'>{delta}</div>" if delta else ""
    return f"<div class='mcard {cls}'><div class='mcard-icon'>{icon}</div><div class='mcard-label'>{label}</div><div class='mcard-value'>{value}</div>{dh}</div>"

def stitle(icon, text):
    st.markdown(f"<div class='stitle'>{icon}&nbsp;<span class='stitle-dot'></span>&nbsp;{text}</div>", unsafe_allow_html=True)

def hr():
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

def box(content, kind="info"):
    st.markdown(f"<div class='box box-{kind}'>{content}</div>", unsafe_allow_html=True)

# ─── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_file(b, name):
    return pd.read_csv(io.BytesIO(b)) if name.endswith(".csv") else pd.read_excel(io.BytesIO(b))

def process(raw):
    df = raw.copy()
    df["Date"]               = pd.to_datetime(df["Date"], errors="coerce")
    df["Water_Usage_Liters"] = pd.to_numeric(df["Water_Usage_Liters"], errors="coerce")
    df["Cost_AED"]           = pd.to_numeric(df["Cost_AED"], errors="coerce")
    df = df.dropna(subset=["Date","Water_Usage_Liters","Cost_AED"]).sort_values("Date").reset_index(drop=True)
    avg = df["Water_Usage_Liters"].mean()
    std = df["Water_Usage_Liters"].std()
    thr = avg + 2 * std
    df["Is_Abnormal"]   = df["Water_Usage_Liters"] > thr
    df["Wasted_Liters"] = np.where(df["Is_Abnormal"], df["Water_Usage_Liters"] - avg, 0)
    df["Month_Label"]   = df["Date"].dt.strftime("%b %Y")
    df["Day_of_Week"]   = df["Date"].dt.day_name()
    return df, avg, std, thr

# ─── Session state ────────────────────────────────────────────────────────────
for k, v in [("df_raw",None),("df",None),("stats",{})]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:22px 0 12px;'>
        <div style='font-size:2.7rem;'>💧</div>
        <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#DFF0F8;line-height:1.25;'>AquaSense UAE</div>
        <div style='font-size:0.67rem;color:rgba(223,240,248,0.55);margin-top:5px;letter-spacing:1.3px;'>SMART WATER DASHBOARD</div>
    </div>
    <hr style='border-color:rgba(255,255,255,0.14);margin:6px 0 16px;'>
    """, unsafe_allow_html=True)
    PAGES = [
        "🏠  Home",
        "📂  Upload Water Data",
        "🔍  Data Quality Check",
        "📊  Water Usage Dashboard",
        "📅  Monthly Water Summary",
        "🏢  Building-wise Comparison",
        "🚨  Abnormal Usage / Leak Detection",
        "🌍  Impact Calculator",
        "🤖  AI Recommendations",
        "📋  Final Impact Report",
    ]
    page = st.radio("nav", PAGES, label_visibility="collapsed")

# ─── Guard ────────────────────────────────────────────────────────────────────
def need_data():
    if st.session_state.df is None:
        st.markdown("""<div style='text-align:center;padding:70px 20px;'>
            <div style='font-size:3.5rem;margin-bottom:14px;'>📂</div>
            <div style='font-family:Syne,sans-serif;font-size:1.25rem;font-weight:700;color:#003D52;'>No Data Uploaded Yet</div>
            <div style='font-size:0.9rem;color:#5A7A85;margin-top:8px;'>
                Go to <strong style='color:#0A7EA4;'>Upload Water Data</strong> first.
            </div></div>""", unsafe_allow_html=True)
        return False
    return True

# ═════════════════════════════════════════════════════════════════════════════
# HOME
# ═════════════════════════════════════════════════════════════════════════════
if page.startswith("🏠"):
    st.markdown("""
    <div class='hero'>
        <div class='hero-title'>💧 AquaSense UAE</div>
        <div class='hero-sub'>AI-Powered Water Impact Dashboard for Sustainable Campuses</div>
        <div class='badge-row'>
            <span class='badge'>🏆 RAK EISC 2026 — 3rd Place</span>
            <span class='badge'>🎖️ RAK Dept. of Knowledge Award</span>
            <span class='badge'>💰 AED 1,000 Cash Prize</span>
            <span class='badge'>🌱 UAE Net Zero 2050 Aligned</span>
        </div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        stitle("📌", "About This Project")
        box("""<strong>AquaSense UAE</strong> is a smart water management system for UAE 
        universities and buildings. It analyses daily water consumption data, flags potential 
        leaks using statistical anomaly detection, estimates the true cost of water waste in AED, 
        and generates practical recommendations — supporting the UAE's water security and 
        Net Zero 2050 goals.""", "info")

        box("""🌍 <strong>Why Water Matters in the UAE</strong><br>
        Over <strong>90% of UAE freshwater comes from energy-intensive desalination</strong>. 
        The UAE ranks among the highest per-capita water consumers globally. Every litre 
        saved reduces CO₂ emissions, energy costs, and national water insecurity.""", "success")

        stitle("⚙️", "What This Dashboard Does")
        for icon, text in [
            ("📂","Upload and validate campus water data from CSV or Excel"),
            ("🔍","Automated data quality checks — missing values, duplicates, column validation"),
            ("📊","Interactive daily, monthly, and building-level consumption charts"),
            ("🚨","Statistical anomaly detection to flag leaks and abnormal spikes"),
            ("🌍","Real financial (AED) and environmental (CO₂) impact of water waste"),
            ("🤖","AI-style recommendations tailored to your specific usage patterns"),
            ("📋","Exportable impact report with projected yearly savings"),
        ]:
            st.markdown(f"""<div class='feat-row'>
                <span style='font-size:1.05rem;flex-shrink:0;'>{icon}</span>
                <span class='feat-text'>{text}</span>
            </div>""", unsafe_allow_html=True)

    with col2:
        stitle("🏆", "Awards & Recognition")
        for icon, title, sub, color in [
            ("🥉","3rd Place","RAK EISC 2026 Competition","#F5A623"),
            ("🎖️","Special Recognition","RAK Department of Knowledge","#0A7EA4"),
            ("💰","AED 1,000","Cash Prize Awarded","#00C5A1"),
            ("🌱","SDG 6 Aligned","Clean Water & Sanitation","#003D52"),
        ]:
            st.markdown(f"""<div class='acard' style='border-left:4px solid {color};'>
                <div style='font-size:1.5rem;'>{icon}</div>
                <div class='acard-title'>{title}</div>
                <div class='acard-sub'>{sub}</div>
            </div>""", unsafe_allow_html=True)

        stitle("📖", "How to Use")
        for num, text in [
            ("1","Go to Upload Water Data"),
            ("2","Upload your CSV or Excel file"),
            ("3","Navigate through each analysis section"),
            ("4","Download the Final Impact Report"),
        ]:
            st.markdown(f"""<div class='step-row'>
                <div class='step-num'>{num}</div>
                <div class='step-label'>{text}</div>
            </div>""", unsafe_allow_html=True)

    hr()
    stitle("📋", "Required Data Columns")
    c1,c2,c3,c4 = st.columns(4)
    for col, (icon, name, desc) in zip([c1,c2,c3,c4], [
        ("📅","Date","Any standard date format"),
        ("🏢","Building","Building name or block ID"),
        ("💧","Water_Usage_Liters","Daily consumption in litres"),
        ("💰","Cost_AED","Cost in UAE Dirhams"),
    ]):
        with col:
            st.markdown(mcard(icon, name, name, desc, "ml-blue"), unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# UPLOAD
# ═════════════════════════════════════════════════════════════════════════════
elif page.startswith("📂"):
    st.markdown("""<div class='hero' style='padding:34px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>📂 Upload Water Data</div>
        <div class='hero-sub'>Upload your campus water consumption file to begin analysis</div>
    </div>""", unsafe_allow_html=True)

    col_up, col_info = st.columns([2,1], gap="large")
    with col_up:
        stitle("⬆️", "Upload Your File")
        uploaded = st.file_uploader("Drag & drop or browse — CSV or Excel accepted", type=["csv","xlsx","xls"])
        if uploaded:
            with st.spinner("Reading file…"):
                raw = load_file(uploaded.read(), uploaded.name)
            st.session_state.df_raw = raw
            REQUIRED = {"Date","Building","Water_Usage_Liters","Cost_AED"}
            missing  = REQUIRED - set(raw.columns)
            if missing:
                box(f"⚠️ Missing columns: <strong>{', '.join(missing)}</strong>", "danger")
            else:
                df_p, avg, std, thr = process(raw)
                abn_cost = df_p[df_p["Is_Abnormal"]]["Cost_AED"].sum()
                st.session_state.df    = df_p
                st.session_state.stats = dict(
                    avg=avg, std=std, thresh=thr,
                    total_usage=df_p["Water_Usage_Liters"].sum(),
                    total_cost=df_p["Cost_AED"].sum(),
                    total_waste=df_p["Wasted_Liters"].sum(),
                    n_abnormal=int(df_p["Is_Abnormal"].sum()),
                    n_rows=len(df_p), abn_cost=abn_cost,
                )
                box("✅ <strong>File processed successfully!</strong> Navigate to any section.", "success")
            st.markdown("#### Data Preview")
            st.dataframe(raw.head(10), use_container_width=True, height=260)
            c1,c2,c3 = st.columns(3)
            with c1: st.markdown(mcard("📄","Total Rows",f"{len(raw):,}","","ml-blue"), unsafe_allow_html=True)
            with c2: st.markdown(mcard("📐","Columns",str(len(raw.columns)),"","ml-green"), unsafe_allow_html=True)
            with c3: st.markdown(mcard("💾","File Size",f"{uploaded.size/1024:.1f} KB","","ml-deep"), unsafe_allow_html=True)
        else:
            st.markdown("""<div style='text-align:center;padding:58px 20px;'>
                <div style='font-size:3.5rem;margin-bottom:12px;'>📤</div>
                <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:600;color:#003D52;'>No file uploaded yet</div>
                <div style='font-size:0.87rem;color:#5A7A85;margin-top:7px;'>Upload a CSV or Excel file to start</div>
            </div>""", unsafe_allow_html=True)

    with col_info:
        stitle("📋", "Requirements")
        box("""<strong>Required Columns</strong><br><br>
        ✅ <code>Date</code><br>✅ <code>Building</code><br>
        ✅ <code>Water_Usage_Liters</code><br>✅ <code>Cost_AED</code><br><br>
        <strong>Accepted Formats</strong><br><br>
        📄 <code>.csv</code><br>📊 <code>.xlsx</code> / <code>.xls</code>""", "info")
        stitle("💡", "Sample Row")
        st.dataframe(pd.DataFrame([
            {"Date":"2024-01-15","Building":"Block A","Water_Usage_Liters":3200,"Cost_AED":16.5},
            {"Date":"2024-01-16","Building":"Block B","Water_Usage_Liters":4100,"Cost_AED":21.2},
        ]), use_container_width=True, hide_index=True)

# ═════════════════════════════════════════════════════════════════════════════
# DATA QUALITY CHECK
# ═════════════════════════════════════════════════════════════════════════════
elif page.startswith("🔍"):
    st.markdown("""<div class='hero' style='padding:34px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>🔍 Data Quality Check</div>
        <div class='hero-sub'>Validate your dataset before running analysis</div>
    </div>""", unsafe_allow_html=True)

    if not need_data(): st.stop()
    df  = st.session_state.df
    raw = st.session_state.df_raw
    nulls = int(raw.isnull().sum().sum())
    dups  = int(raw.duplicated().sum())
    days  = (df["Date"].max()-df["Date"].min()).days

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(mcard("📄","Total Records",f"{len(raw):,}","","ml-blue"), unsafe_allow_html=True)
    with c2: st.markdown(mcard("🚫","Missing Values",str(nulls),"Clean ✅" if nulls==0 else "⚠️ Fix needed","ml-green" if nulls==0 else "ml-red"), unsafe_allow_html=True)
    with c3: st.markdown(mcard("🔁","Duplicates",str(dups),"None ✅" if dups==0 else "Found ⚠️","ml-green" if dups==0 else "ml-warn"), unsafe_allow_html=True)
    with c4: st.markdown(mcard("📅","Date Span",f"{days} days",f"{df['Date'].min().date()} → {df['Date'].max().date()}","ml-deep"), unsafe_allow_html=True)

    hr()
    col1,col2 = st.columns(2)
    with col1:
        stitle("📋","Column Health")
        for col in ["Date","Building","Water_Usage_Liters","Cost_AED"]:
            if col in raw.columns:
                n  = int(raw[col].isnull().sum())
                ok = n == 0
                st.markdown(f"""<div style='display:flex;justify-content:space-between;align-items:center;
                    padding:10px 14px;background:{"#E4F9F3" if ok else "#FFF6E2"};
                    border-radius:10px;margin-bottom:8px;'>
                    <span style='font-weight:600;color:#003D52;font-family:DM Sans,sans-serif;'>{col}</span>
                    <span style='color:{"#074D3A" if ok else "#5C3D00"};font-weight:600;font-family:DM Sans,sans-serif;'>
                        {"✅ OK" if ok else f"⚠️ {n} missing"}</span>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style='display:flex;justify-content:space-between;align-items:center;
                    padding:10px 14px;background:#FDECEA;border-radius:10px;margin-bottom:8px;'>
                    <span style='font-weight:600;color:#003D52;font-family:DM Sans,sans-serif;'>{col}</span>
                    <span style='color:#6B1010;font-weight:600;font-family:DM Sans,sans-serif;'>❌ Missing</span>
                </div>""", unsafe_allow_html=True)
    with col2:
        stitle("📈","Statistical Summary")
        st.dataframe(df[["Water_Usage_Liters","Cost_AED"]].describe().round(2), use_container_width=True)

    hr()
    stitle("🏢","Records per Building")
    bc = df.groupby("Building").size().reset_index(name="Records")
    fig = px.bar(bc,x="Building",y="Records",color="Records",color_continuous_scale=["#6EC6E6","#003D52"],title="Data Records per Building")
    st.plotly_chart(theme(fig), use_container_width=True)
    st.dataframe(df[["Date","Building","Water_Usage_Liters","Cost_AED","Is_Abnormal"]], use_container_width=True, height=280)

# ═════════════════════════════════════════════════════════════════════════════
# WATER USAGE DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
elif page.startswith("📊"):
    st.markdown("""<div class='hero' style='padding:34px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>📊 Water Usage Dashboard</div>
        <div class='hero-sub'>Campus-wide consumption trends and patterns</div>
    </div>""", unsafe_allow_html=True)

    if not need_data(): st.stop()
    df = st.session_state.df
    s  = st.session_state.stats
    wp = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(mcard("💧","Total Water Used",fmt(s["total_usage"])+" L","","ml-blue"), unsafe_allow_html=True)
    with c2: st.markdown(mcard("💰","Total Cost",f"AED {fmt(s['total_cost'])}","","ml-green"), unsafe_allow_html=True)
    with c3: st.markdown(mcard("📏","Daily Average",fmt(s["avg"])+" L","Per day","ml-deep"), unsafe_allow_html=True)
    with c4: st.markdown(mcard("🚨","Anomaly Days",str(s["n_abnormal"]),"Usage spikes","ml-red"), unsafe_allow_html=True)
    with c5: st.markdown(mcard("🌊","Est. Wasted",fmt(s["total_waste"])+" L",f"{wp:.1f}% of total","ml-warn"), unsafe_allow_html=True)

    hr()
    stitle("📈","Daily Usage Trend")
    daily = df.groupby("Date",as_index=False)["Water_Usage_Liters"].sum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily["Date"],y=daily["Water_Usage_Liters"],mode="lines",name="Daily Usage",
        line=dict(color="#0A7EA4",width=2.5),fill="tozeroy",fillcolor="rgba(10,126,164,0.07)"))
    fig.add_hline(y=s["avg"],line_dash="dot",line_color="#00C5A1",annotation_text=f"Avg: {s['avg']:.0f} L",annotation_font_color="#007A60")
    fig.add_hline(y=s["thresh"],line_dash="dash",line_color="#E84855",annotation_text="Anomaly Threshold",annotation_font_color="#E84855")
    theme(fig); fig.update_layout(title="Daily Water Consumption — All Buildings",xaxis_title="Date",yaxis_title="Litres")
    st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2)
    with col1:
        cd = df.groupby("Date",as_index=False)["Cost_AED"].sum()
        fig2 = px.area(cd,x="Date",y="Cost_AED",color_discrete_sequence=["#00C5A1"],title="Daily Cost in AED")
        fig2.update_traces(fillcolor="rgba(0,197,161,0.1)")
        st.plotly_chart(theme(fig2), use_container_width=True)
    with col2:
        dow = df.groupby("Day_of_Week")["Water_Usage_Liters"].mean().reindex(
            ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]).reset_index()
        dow.columns = ["Day","Avg"]
        fig3 = px.bar(dow,x="Day",y="Avg",color="Avg",color_continuous_scale=["#6EC6E6","#003D52"],title="Avg Usage by Day of Week")
        st.plotly_chart(theme(fig3), use_container_width=True)

    stitle("🔵","Usage vs Cost")
    fig4 = px.scatter(df,x="Water_Usage_Liters",y="Cost_AED",color="Building",size="Water_Usage_Liters",
                      hover_data=["Date","Building"],title="Water Usage (L) vs Cost (AED) — by Building",
                      color_discrete_sequence=COLORS)
    st.plotly_chart(theme(fig4), use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# MONTHLY SUMMARY
# ═════════════════════════════════════════════════════════════════════════════
elif page.startswith("📅"):
    st.markdown("""<div class='hero' style='padding:34px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>📅 Monthly Water Summary</div>
        <div class='hero-sub'>Month-by-month consumption and cost breakdown</div>
    </div>""", unsafe_allow_html=True)

    if not need_data(): st.stop()
    df = st.session_state.df
    monthly = df.groupby("Month_Label").agg(
        Usage=("Water_Usage_Liters","sum"),Cost=("Cost_AED","sum"),
        Avg=("Water_Usage_Liters","mean"),Waste=("Wasted_Liters","sum"),Abn=("Is_Abnormal","sum")
    ).reset_index()

    fig = make_subplots(specs=[[{"secondary_y":True}]])
    fig.add_trace(go.Bar(x=monthly["Month_Label"],y=monthly["Usage"],name="Usage (L)",marker_color="#0A7EA4"),secondary_y=False)
    fig.add_trace(go.Scatter(x=monthly["Month_Label"],y=monthly["Cost"],name="Cost (AED)",mode="lines+markers",line=dict(color="#00C5A1",width=3),marker_size=8),secondary_y=True)
    fig.update_layout(title="Monthly Water Usage & Cost",**_L)
    fig.update_yaxes(title_text="Litres",secondary_y=False)
    fig.update_yaxes(title_text="AED",secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2)
    with col1:
        fig2 = px.bar(monthly,x="Month_Label",y="Waste",color="Waste",color_continuous_scale=["#FFFACD","#E84855"],title="Estimated Wasted Water per Month (L)")
        st.plotly_chart(theme(fig2), use_container_width=True)
    with col2:
        fig3 = px.line(monthly,x="Month_Label",y="Avg",markers=True,color_discrete_sequence=["#F5A623"],title="Average Daily Usage per Month")
        fig3.update_traces(line_width=3,marker_size=9)
        st.plotly_chart(theme(fig3), use_container_width=True)

    stitle("📋","Monthly Table")
    md = monthly.copy().round(1)
    md.columns = ["Month","Total (L)","Cost (AED)","Avg Daily (L)","Wasted (L)","Anomaly Days"]
    st.dataframe(md, use_container_width=True, hide_index=True)

# ═════════════════════════════════════════════════════════════════════════════
# BUILDING COMPARISON
# ═════════════════════════════════════════════════════════════════════════════
elif page.startswith("🏢"):
    st.markdown("""<div class='hero' style='padding:34px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>🏢 Building-wise Comparison</div>
        <div class='hero-sub'>Which buildings consume the most — and waste the most</div>
    </div>""", unsafe_allow_html=True)

    if not need_data(): st.stop()
    df = st.session_state.df
    bld = df.groupby("Building").agg(
        Usage=("Water_Usage_Liters","sum"),Cost=("Cost_AED","sum"),
        Avg=("Water_Usage_Liters","mean"),Waste=("Wasted_Liters","sum"),
        Abn=("Is_Abnormal","sum"),N=("Water_Usage_Liters","count")
    ).reset_index().sort_values("Usage",ascending=False)

    col1,col2 = st.columns(2)
    with col1:
        fig = px.bar(bld,x="Building",y="Usage",color="Usage",color_continuous_scale=["#6EC6E6","#003D52"],
                     title="Total Water Usage by Building (L)",text="Usage")
        fig.update_traces(texttemplate="%{text:,.0f}",textposition="outside",textfont_size=10)
        st.plotly_chart(theme(fig), use_container_width=True)
    with col2:
        fig2 = px.pie(bld,values="Usage",names="Building",color_discrete_sequence=COLORS,hole=0.44,title="Share of Total Usage")
        fig2.update_traces(textposition="inside",textinfo="percent+label")
        st.plotly_chart(theme(fig2), use_container_width=True)

    stitle("💧","Avg Daily Usage vs Estimated Waste")
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=bld["Building"],y=bld["Avg"],name="Avg Daily",marker_color="#0A7EA4"))
    fig3.add_trace(go.Bar(x=bld["Building"],y=bld["Waste"],name="Est. Wasted",marker_color="#E84855"))
    fig3.update_layout(barmode="group",title="Avg Daily Usage vs Estimated Waste per Building",**_L)
    st.plotly_chart(fig3, use_container_width=True)

    col3,col4 = st.columns(2)
    with col3:
        fig4 = px.bar(bld.sort_values("Waste"),x="Waste",y="Building",orientation="h",
                      color="Waste",color_continuous_scale=["#FFF3CC","#E84855"],title="Wasted Water Ranking (L)")
        st.plotly_chart(theme(fig4), use_container_width=True)
    with col4:
        fig5 = px.scatter(bld,x="Avg",y="Cost",size="Usage",color="Building",
                          title="Avg Daily Usage vs Total Cost",color_discrete_sequence=COLORS,hover_data=["Abn"])
        st.plotly_chart(theme(fig5), use_container_width=True)

    stitle("📋","Building Summary Table")
    bd = bld.round(1).copy()
    bd.columns = ["Building","Total (L)","Cost (AED)","Avg Daily (L)","Wasted (L)","Anomaly Days","Records"]
    st.dataframe(bd, use_container_width=True, hide_index=True)

# ═════════════════════════════════════════════════════════════════════════════
# ABNORMAL DETECTION
# ═════════════════════════════════════════════════════════════════════════════
elif page.startswith("🚨"):
    st.markdown("""<div class='hero' style='padding:34px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>🚨 Abnormal Usage / Leak Detection</div>
        <div class='hero-sub'>Statistical anomaly detection to flag potential leaks and waste</div>
    </div>""", unsafe_allow_html=True)

    if not need_data(): st.stop()
    df = st.session_state.df
    s  = st.session_state.stats

    box(f"""<strong>Detection Method — 2 Standard Deviation Rule:</strong> Any day where usage 
    exceeds the campus average + 2× standard deviation is flagged as abnormal — indicating a 
    potential <strong>leak, faulty valve, or unusual consumption event</strong>.<br><br>
    📏 Average: <strong>{s['avg']:,.1f} L/day</strong> &nbsp;|&nbsp;
    📊 Std Dev: <strong>{s['std']:,.1f} L</strong> &nbsp;|&nbsp;
    🚨 Threshold: <strong>{s['thresh']:,.1f} L/day</strong>""", "info")

    abn = df[df["Is_Abnormal"]]
    pct = s["n_abnormal"]/s["n_rows"]*100 if s["n_rows"] else 0
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(mcard("🚨","Anomaly Days",str(s["n_abnormal"]),f"of {s['n_rows']} records","ml-red"), unsafe_allow_html=True)
    with c2: st.markdown(mcard("📊","Anomaly Rate",f"{pct:.1f}%","Of total data","ml-warn"), unsafe_allow_html=True)
    with c3: st.markdown(mcard("💧","Est. Wasted",fmt(s["total_waste"])+" L","Above-average waste","ml-blue"), unsafe_allow_html=True)
    with c4: st.markdown(mcard("💰","AED Loss",f"AED {fmt(s['abn_cost'])}","From anomaly days","ml-deep"), unsafe_allow_html=True)

    hr()
    stitle("📈","Usage Timeline with Anomaly Markers")
    daily = df.groupby("Date").agg(U=("Water_Usage_Liters","sum"),A=("Is_Abnormal","any")).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily["Date"],y=daily["U"],mode="lines",name="Daily Usage",
        line=dict(color="#0A7EA4",width=2.5),fill="tozeroy",fillcolor="rgba(10,126,164,0.07)"))
    ad = daily[daily["A"]]
    fig.add_trace(go.Scatter(x=ad["Date"],y=ad["U"],mode="markers",name="⚠️ Anomaly",
        marker=dict(color="#E84855",size=13,symbol="circle",line=dict(color="white",width=2))))
    fig.add_hline(y=s["thresh"],line_dash="dash",line_color="#E84855",annotation_text=f"Threshold: {s['thresh']:,.0f} L",annotation_font_color="#E84855")
    fig.add_hline(y=s["avg"],line_dash="dot",line_color="#00C5A1",annotation_text=f"Average: {s['avg']:,.0f} L",annotation_font_color="#007A60")
    theme(fig); fig.update_layout(title="Daily Usage — Anomalies Highlighted",xaxis_title="Date",yaxis_title="Litres")
    st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2)
    with col1:
        stitle("🏢","Anomaly Days by Building")
        ab = df.groupby("Building")["Is_Abnormal"].sum().reset_index()
        ab.columns = ["Building","Anomalies"]
        ab = ab[ab["Anomalies"]>0].sort_values("Anomalies",ascending=False)
        if len(ab):
            fig2 = px.bar(ab,x="Building",y="Anomalies",color="Anomalies",color_continuous_scale=["#FFD166","#E84855"],title="Anomaly Days per Building")
            st.plotly_chart(theme(fig2), use_container_width=True)
        else:
            box("✅ No anomalies detected per building.","success")
    with col2:
        stitle("📦","Usage Distribution")
        fig3 = go.Figure()
        fig3.add_trace(go.Histogram(x=df["Water_Usage_Liters"],nbinsx=30,marker_color="#0A7EA4",opacity=0.75,name="Records"))
        fig3.add_vline(x=s["avg"],line_dash="dot",line_color="#00C5A1",annotation_text="Average")
        fig3.add_vline(x=s["thresh"],line_dash="dash",line_color="#E84855",annotation_text="Threshold")
        theme(fig3); fig3.update_layout(title="Usage Distribution with Threshold",xaxis_title="Litres",yaxis_title="Frequency")
        st.plotly_chart(fig3, use_container_width=True)

    stitle("📋","Flagged Records")
    if len(abn):
        ad2 = abn[["Date","Building","Water_Usage_Liters","Cost_AED","Wasted_Liters"]].copy()
        ad2.columns = ["Date","Building","Usage (L)","Cost (AED)","Wasted (L)"]
        st.dataframe(ad2.round(2).sort_values("Wasted (L)",ascending=False), use_container_width=True, hide_index=True)
    else:
        box("✅ No abnormal records in this dataset.","success")

# ═════════════════════════════════════════════════════════════════════════════
# IMPACT CALCULATOR
# ═════════════════════════════════════════════════════════════════════════════
elif page.startswith("🌍"):
    st.markdown("""<div class='hero' style='padding:34px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>🌍 Impact Calculator</div>
        <div class='hero-sub'>Financial and environmental cost of water waste</div>
    </div>""", unsafe_allow_html=True)

    if not need_data(): st.stop()
    df = st.session_state.df
    s  = st.session_state.stats

    days    = (df["Date"].max()-df["Date"].min()).days + 1
    y_waste = (s["total_waste"]/days)*365
    y_save  = y_waste*0.5
    y_aed   = (s["abn_cost"]/days)*365*0.5
    co2     = y_save*0.000344
    kwh     = y_save*0.004
    bottles = y_save*2
    trees   = y_save*0.05/1000
    wp      = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0

    stitle("📊","Current Waste")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(mcard("💧","Wasted (Period)",fmt(s["total_waste"])+" L","From anomaly days","ml-red"), unsafe_allow_html=True)
    with c2: st.markdown(mcard("📊","Waste %",f"{wp:.1f}%","Of total usage","ml-warn"), unsafe_allow_html=True)
    with c3: st.markdown(mcard("💰","AED Loss",f"AED {fmt(s['abn_cost'])}","Anomaly cost","ml-blue"), unsafe_allow_html=True)
    with c4: st.markdown(mcard("📅","Period",f"{days} days",f"{df['Date'].min().date()}","ml-deep"), unsafe_allow_html=True)

    hr()
    stitle("🌱","Projected Yearly Savings at 50% Waste Reduction")
    box("""These projections show what could be saved annually if abnormal usage is reduced by 
    <strong>50%</strong> through leak repairs and improved practices — a realistic, achievable 
    target for most campuses.""", "success")

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(mcard("💧","Water Saved/Year",fmt(y_save)+" L","50% of yearly waste","ml-green"), unsafe_allow_html=True)
    with c2: st.markdown(mcard("💰","AED Saved/Year",f"AED {fmt(y_aed)}","Financial saving","ml-blue"), unsafe_allow_html=True)
    with c3: st.markdown(mcard("🌿","CO₂ Avoided",f"{co2:,.1f} kg","Less desalination","ml-deep"), unsafe_allow_html=True)
    with c4: st.markdown(mcard("⚡","Energy Saved",f"{kwh:,.1f} kWh","Desal energy cut","ml-warn"), unsafe_allow_html=True)

    c5,c6,_,_ = st.columns(4)
    with c5: st.markdown(mcard("🍶","Bottles Equiv.",fmt(bottles),"500ml bottles","ml-red"), unsafe_allow_html=True)
    with c6: st.markdown(mcard("🌳","Trees Equiv.",f"{trees:,.0f}","CO₂ offset equiv.","ml-green"), unsafe_allow_html=True)

    hr()
    col1,col2 = st.columns(2)
    with col1:
        pie = pd.DataFrame({"Category":["Normal Usage","Estimated Waste"],"Litres":[s["total_usage"]-s["total_waste"],s["total_waste"]]})
        fig = px.pie(pie,values="Litres",names="Category",hole=0.5,color_discrete_sequence=["#0A7EA4","#E84855"],title="Normal vs Wasted Water")
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(theme(fig), use_container_width=True)
    with col2:
        fig2 = go.Figure(go.Waterfall(
            orientation="v",measure=["relative","relative","relative","total"],
            x=["Total Waste","50% Reduction","Remaining","Net Saving"],y=[y_waste,-y_save,y_save,0],
            connector={"line":{"color":"#D0E8F0"}},
            increasing={"marker":{"color":"#E84855"}},decreasing={"marker":{"color":"#00C5A1"}},totals={"marker":{"color":"#0A7EA4"}},
        ))
        theme(fig2); fig2.update_layout(title="Yearly Waste & Saving Waterfall (L)")
        st.plotly_chart(fig2, use_container_width=True)

    hr()
    stitle("🎛️","Custom Reduction Scenario")
    pct = st.slider("Select waste reduction target (%)", 10, 90, 50, 5)
    cs = y_waste*(pct/100); ca = y_aed*(pct/50); cc = cs*0.000344
    c1,c2,c3 = st.columns(3)
    with c1: st.markdown(mcard("💧",f"Saved at {pct}%",fmt(cs)+" L/yr","","ml-blue"), unsafe_allow_html=True)
    with c2: st.markdown(mcard("💰","AED Saved",f"AED {fmt(ca)}/yr","","ml-green"), unsafe_allow_html=True)
    with c3: st.markdown(mcard("🌿","CO₂ Avoided",f"{cc:,.2f} kg/yr","","ml-deep"), unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# AI RECOMMENDATIONS
# ═════════════════════════════════════════════════════════════════════════════
elif page.startswith("🤖"):
    st.markdown("""<div class='hero' style='padding:34px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>🤖 AI Recommendations</div>
        <div class='hero-sub'>Data-driven actions tailored to your campus patterns</div>
    </div>""", unsafe_allow_html=True)

    if not need_data(): st.stop()
    df = st.session_state.df
    s  = st.session_state.stats
    wp = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0

    box(f"""⚠️ Your campus is wasting an estimated <strong>{wp:.1f}%</strong> of its water 
    through <strong>{s['n_abnormal']}</strong> anomaly events. The recommendations below are 
    generated from your specific data patterns.""", "danger")

    ba  = df.groupby("Building").agg(A=("Is_Abnormal","sum"),W=("Wasted_Liters","sum")).reset_index()
    top = ba[ba["A"]>0].sort_values("A",ascending=False)["Building"].tolist()
    if top:
        stitle("🏢","Building Alerts")
        for bld in top[:5]:
            r = ba[ba["Building"]==bld].iloc[0]
            box(f"""🚨 <strong>{bld}</strong> — {int(r['A'])} anomaly day(s) · 
            Estimated <strong>{r['W']:,.0f} L</strong> wasted. Inspection recommended.""", "danger")

    hr()
    stitle("💡","Recommendations")
    RECS = [
        ("🔧","Fix Leaks Immediately",
         f"Your data shows {s['n_abnormal']} abnormal usage days — likely caused by leaking pipes, "
         "running toilets, or faulty valves. A dripping tap wastes 10,000+ L/year. Plumbing inspection is the highest-ROI action available.",
         "30–50% waste reduction"),
        ("📱","Install Smart Water Meters",
         "IoT-enabled meters provide real-time alerts when usage exceeds thresholds — automating "
         "exactly what this dashboard detects, running continuously without manual uploads.",
         "Instant leak detection"),
        ("🚿","Upgrade to Low-Flow Fixtures",
         "Replacing standard taps and toilets with low-flow equivalents reduces consumption by "
         "30–50% with no change in user experience. Prioritise the highest-usage buildings first.",
         "30–45% per fixture"),
        ("🌿","Greywater Recycling",
         "Reuse sink and shower water for flushing and irrigation. UAE campuses with greywater "
         "systems report up to 40% reduction in potable water demand.",
         "Up to 40% potable saving"),
        ("👥","Awareness Programme",
         "Monthly water challenges at UAE universities have achieved 15–25% reductions within "
         "3 months. Behavioural nudges cost almost nothing to implement.",
         "15–25% usage reduction"),
        ("🗓️","Quarterly Plumbing Audits",
         "Preventive maintenance is 10× cheaper than emergency repairs. Scheduled audits catch "
         "slow leaks before they become costly — exactly the type this dashboard detects.",
         "60–80% fewer anomaly days"),
        ("☀️","Solar Water Heating",
         "Switching to solar heaters cuts energy costs and supports UAE Net Zero 2050. "
         "Insulated pipes eliminate heat-loss waste.",
         "20% energy + water saving"),
        ("🌱","Drought-Resistant Landscaping",
         "UAE-native plants with drip irrigation dramatically reduce outdoor water use. "
         "Landscape irrigation accounts for up to 50% of campus water in summer.",
         "Up to 50% irrigation saving"),
    ]
    for icon, title, body, saving in RECS:
        st.markdown(f"""<div class='rec'>
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
        "Action":["Fix Leaks","Smart Meters","Low-Flow Fixtures","Greywater","Awareness"],
        "Impact":[95,85,75,70,55],"Ease":[80,50,70,35,90],"Cost_K_AED":[5,80,40,150,2],
    })
    fig = px.scatter(pri,x="Ease",y="Impact",size="Cost_K_AED",text="Action",color="Impact",
                     color_continuous_scale=["#6EC6E6","#003D52"],title="Impact vs Ease of Implementation",
                     labels={"Ease":"Ease →","Impact":"Impact ↑"})
    fig.update_traces(textposition="top center")
    st.plotly_chart(theme(fig), use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# FINAL REPORT
# ═════════════════════════════════════════════════════════════════════════════
elif page.startswith("📋"):
    st.markdown("""<div class='hero' style='padding:34px 40px;'>
        <div class='hero-title' style='font-size:2rem;'>📋 Final Impact Report</div>
        <div class='hero-sub'>Full summary of findings, projections, and recommended actions</div>
    </div>""", unsafe_allow_html=True)

    if not need_data(): st.stop()
    df = st.session_state.df
    s  = st.session_state.stats

    days    = (df["Date"].max()-df["Date"].min()).days + 1
    y_waste = (s["total_waste"]/days)*365
    y_save  = y_waste*0.5
    y_aed   = (s["abn_cost"]/days)*365*0.5
    co2     = y_save*0.000344
    wp      = s["total_waste"]/s["total_usage"]*100 if s["total_usage"] else 0
    bld_n   = df["Building"].nunique()

    st.markdown(f"""<div class='report-hero'>
        <div style='font-family:Syne,sans-serif;font-size:1.35rem;font-weight:800;color:#FFFFFF;margin-bottom:6px;'>
            💧 AquaSense UAE — Campus Water Impact Report
        </div>
        <div style='color:rgba(255,255,255,0.7);font-size:0.84rem;margin-bottom:24px;'>
            Generated: {datetime.now().strftime("%d %B %Y, %H:%M")} &nbsp;|&nbsp;
            Period: {df['Date'].min().date()} → {df['Date'].max().date()} &nbsp;|&nbsp;
            Buildings analysed: {bld_n}
        </div>
        <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:14px;'>
            <div style='text-align:center;'><div class='report-val'>{fmt(s['total_usage'])} L</div><div class='report-lbl'>Total Water Consumed</div></div>
            <div style='text-align:center;'><div class='report-val'>AED {fmt(s['total_cost'])}</div><div class='report-lbl'>Total Cost</div></div>
            <div style='text-align:center;'><div class='report-val'>{s['n_abnormal']}</div><div class='report-lbl'>Anomaly Days</div></div>
            <div style='text-align:center;'><div class='report-val'>{wp:.1f}%</div><div class='report-lbl'>Estimated Waste</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

    stitle("🌱","Projected Yearly Savings — 50% Waste Reduction")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(mcard("💧","Water Saved/Year",fmt(y_save)+" L","","ml-green"), unsafe_allow_html=True)
    with c2: st.markdown(mcard("💰","AED Saved/Year",f"AED {fmt(y_aed)}","","ml-blue"), unsafe_allow_html=True)
    with c3: st.markdown(mcard("🌿","CO₂ Avoided",f"{co2:,.1f} kg/yr","","ml-deep"), unsafe_allow_html=True)
    with c4: st.markdown(mcard("🏢","Buildings",str(bld_n),"Analysed","ml-warn"), unsafe_allow_html=True)

    hr()
    col1,col2 = st.columns(2)
    with col1:
        pie = pd.DataFrame({"Cat":["Normal","Wasted"],"V":[s["total_usage"]-s["total_waste"],s["total_waste"]]})
        fig = px.pie(pie,values="V",names="Cat",hole=0.5,color_discrete_sequence=["#0A7EA4","#E84855"],title="Normal vs Wasted Water")
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(theme(fig), use_container_width=True)
    with col2:
        bs = df.groupby("Building")["Water_Usage_Liters"].sum().reset_index()
        fig2 = px.pie(bs,values="Water_Usage_Liters",names="Building",color_discrete_sequence=COLORS,hole=0.5,title="Usage by Building")
        fig2.update_traces(textinfo="percent+label")
        st.plotly_chart(theme(fig2), use_container_width=True)

    stitle("📅","Monthly Usage Trend")
    mn = df.groupby("Month_Label")["Water_Usage_Liters"].sum().reset_index()
    fig3 = px.bar(mn,x="Month_Label",y="Water_Usage_Liters",color="Water_Usage_Liters",
                  color_continuous_scale=["#6EC6E6","#003D52"],title="Monthly Water Usage (L)")
    st.plotly_chart(theme(fig3), use_container_width=True)

    hr()
    stitle("📝","Key Findings")
    for f in [
        f"📍 Campus consumed **{s['total_usage']:,.0f} L** over {days} days (avg **AED {s['total_cost']/days:,.2f}/day**).",
        f"🚨 **{s['n_abnormal']} anomaly events** detected using the 2σ threshold ({s['thresh']:,.0f} L/day).",
        f"🌊 Estimated **{s['total_waste']:,.0f} L wasted** — {wp:.1f}% of total consumption.",
        f"💰 AED loss from anomalies: **AED {s['abn_cost']:,.2f}** over the analysis period.",
        f"🌱 At 50% waste reduction: **{y_save:,.0f} L/year** saved and **AED {y_aed:,.2f}/year** recovered.",
        f"🌿 Environmental benefit: **{co2:,.2f} kg CO₂/year** avoided from reduced desalination energy.",
        f"🏢 **{bld_n} buildings** analysed — highest-waste buildings should be prioritised first.",
    ]:
        st.markdown(f)

    hr()
    stitle("🎯","Top 3 Priority Actions")
    for num, icon, title, body in [
        ("1","🔧","Fix Leaks Immediately",f"Inspect all {s['n_abnormal']} flagged anomaly days. Leak repairs deliver the highest ROI."),
        ("2","📱","Deploy Smart Water Meters","Automate real-time anomaly detection — eliminate manual data uploads entirely."),
        ("3","🚿","Low-Flow Fixture Upgrade","Upgrade top-usage buildings first. Typical UAE campus ROI: 12–18 months."),
    ]:
        st.markdown(f"""<div class='rec'>
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
    stitle("⬇️","Export")
    exp = df[["Date","Building","Water_Usage_Liters","Cost_AED","Is_Abnormal","Wasted_Liters"]].copy()
    exp.columns = ["Date","Building","Water_Usage_L","Cost_AED","Is_Abnormal","Wasted_L"]
    summ = pd.DataFrame({
        "Metric":["Total Usage (L)","Total Cost (AED)","Period (days)","Buildings",
                  "Avg Daily (L)","Anomaly Days","Wasted (L)","Waste %",
                  "Yearly Waste (L)","Yearly Saving 50% (L)","AED Saving/Year","CO2 Avoided (kg/yr)"],
        "Value":[f"{s['total_usage']:,.1f}",f"{s['total_cost']:,.2f}",str(days),str(bld_n),
                 f"{s['avg']:,.1f}",str(s['n_abnormal']),f"{s['total_waste']:,.1f}",f"{wp:.2f}%",
                 f"{y_waste:,.1f}",f"{y_save:,.1f}",f"{y_aed:,.2f}",f"{co2:,.4f}"]
    })
    ca,cb,_ = st.columns([1,1,2])
    with ca:
        st.download_button("📥 Full Dataset (CSV)", exp.to_csv(index=False).encode("utf-8"),
                           "aquasense_data.csv","text/csv",use_container_width=True)
    with cb:
        st.download_button("📊 Summary Report (CSV)", summ.to_csv(index=False).encode("utf-8"),
                           "aquasense_summary.csv","text/csv",use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""<div class='footer'>
    💧 <strong>AquaSense UAE</strong> — AI-Powered Water Impact Dashboard for Sustainable Campuses<br>
    <span style='color:#B0C8D0;font-size:0.72rem;'>
        Streamlit · Plotly · Pandas · NumPy &nbsp;|&nbsp; UAE Net Zero 2050 · SDG 6 Clean Water &amp; Sanitation
    </span>
</div>""", unsafe_allow_html=True)
