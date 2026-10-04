"""
MediScan AI — Redesigned
Premium UI · English labels · Image-based verifier
"""
import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime

from database import (
    MEDICINES, search_medicine,
    get_all_medicine_names,
)
from ocr_utils import (
    extract_text_from_image, extract_medicine_names, format_prescription,
)
from verifier import verify_by_image_match, get_verification_checklist
from symptom_checker import suggest_medicines
from complaints import (
    init_complaints, file_complaint, add_comment,
    upvote_complaint, resolve_complaint,
    get_all_complaints, get_complaint_stats,
)


st.set_page_config(
    page_title="MediScan AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)
init_complaints()


# ============================================================
# CSS — MIDNIGHT TEAL PREMIUM THEME
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&display=swap');

    * { font-family: 'Inter', -apple-system, sans-serif; }
    #MainMenu, footer, header {visibility: hidden;}
    .block-container { padding: 1.5rem 2rem 3rem 2rem; max-width: 100%; }

    /* ============ BACKGROUND ============ */
    .stApp {
        background: #f4f6fb;
        background-image:
            radial-gradient(at 0% 0%, rgba(13, 148, 136, 0.06) 0px, transparent 40%),
            radial-gradient(at 100% 0%, rgba(59, 130, 246, 0.05) 0px, transparent 40%);
    }

    /* ============ SIDEBAR ============ */
    [data-testid="stSidebar"] {
        background: #0a1929;
        min-width: 280px !important;
        max-width: 280px !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    [data-testid="stSidebar"] * { color: #94a3b8 !important; }
    [data-testid="stSidebar"] .stRadio > label { display: none; }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 6px; }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
        background: transparent;
        padding: 11px 16px;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.25s ease;
        font-weight: 500;
        font-size: 0.88rem;
        width: 100%;
        border: 1px solid transparent;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
        background: rgba(13, 148, 136, 0.08) !important;
        border-color: rgba(13, 148, 136, 0.2);
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(135deg, rgba(13, 148, 136, 0.9), rgba(6, 182, 212, 0.9)) !important;
        box-shadow: 0 4px 16px rgba(13, 148, 136, 0.4);
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) * {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] .stRadio input[type="radio"] { display: none; }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label > div:first-child {
        display: none;
    }

    /* ============ BRAND ============ */
    .brand {
        display: flex; align-items: center; gap: 0.85rem;
        padding: 0.5rem 0.2rem 1.5rem 0.2rem;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 1.2rem;
    }
    .brand-logo {
        width: 46px; height: 46px;
        background: linear-gradient(135deg, #0d9488, #06b6d4);
        border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.5rem;
        box-shadow: 0 8px 24px rgba(13, 148, 136, 0.4);
    }
    .brand-name {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700; font-size: 1.15rem; color: #ffffff !important;
        letter-spacing: -0.3px;
    }
    .brand-sub {
        font-size: 0.65rem; color: #14b8a6 !important;
        font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px;
        margin-top: 1px;
    }

    /* ============ PAGE HEADER ============ */
    .page-head { margin-bottom: 2rem; }
    .page-eyebrow {
        font-size: 0.72rem; color: #0d9488; font-weight: 700;
        letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0.4rem;
    }
    .page-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem; font-weight: 700; color: #0f172a;
        letter-spacing: -0.8px; margin: 0; line-height: 1.1;
    }
    .page-desc {
        font-size: 0.92rem; color: #64748b; margin-top: 0.5rem;
    }

    /* ============ HERO ============ */
    .hero {
        background: linear-gradient(135deg, #0d9488 0%, #06b6d4 100%);
        padding: 2rem 2.2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px -20px rgba(13, 148, 136, 0.5);
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: ""; position: absolute; top: -50%; right: -10%;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(255,255,255,0.15), transparent 70%);
        border-radius: 50%;
    }
    .hero-content { position: relative; z-index: 2; }
    .hero h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.9rem; font-weight: 700;
        margin: 0 0 0.5rem 0; letter-spacing: -0.6px;
    }
    .hero p { font-size: 1rem; opacity: 0.95; margin: 0; }

    /* ============ KPI CARDS ============ */
    .kpi {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.3rem 1.4rem;
        transition: all 0.25s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    .kpi::before {
        content: ""; position: absolute; top: 0; left: 0;
        width: 4px; height: 100%; background: #0d9488;
    }
    .kpi.blue::before { background: #3b82f6; }
    .kpi.orange::before { background: #f59e0b; }
    .kpi.purple::before { background: #8b5cf6; }
    .kpi:hover {
        border-color: #cbd5e1;
        transform: translateY(-2px);
        box-shadow: 0 12px 28px -10px rgba(0,0,0,0.12);
    }
    .kpi-icon {
        width: 44px; height: 44px; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.3rem; margin-bottom: 1rem;
    }
    .kpi-icon.teal { background: #ccfbf1; }
    .kpi-icon.blue { background: #dbeafe; }
    .kpi-icon.orange { background: #ffedd5; }
    .kpi-icon.purple { background: #ede9fe; }
    .kpi-label {
        font-size: 0.75rem; color: #64748b; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.8px;
        margin-bottom: 0.4rem;
    }
    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem; font-weight: 700; color: #0f172a;
        line-height: 1; letter-spacing: -0.5px;
    }
    .kpi-sub {
        font-size: 0.72rem; color: #94a3b8; margin-top: 0.4rem;
    }

    /* ============ CARDS ============ */
    .card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.4rem 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.2s;
    }
    .card:hover {
        box-shadow: 0 10px 24px -12px rgba(0,0,0,0.1);
        border-color: #cbd5e1;
    }
    .card-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.05rem; font-weight: 600; color: #0f172a;
        margin-bottom: 0.7rem;
    }
    .card-desc {
        font-size: 0.88rem; color: #64748b; line-height: 1.5;
    }

    /* ============ QUICK ACTION ============ */
    .action-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.25s ease;
        height: 100%;
    }
    .action-card:hover {
        border-color: #14b8a6;
        transform: translateY(-3px);
        box-shadow: 0 16px 32px -16px rgba(13, 148, 136, 0.3);
    }
    .action-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem; font-weight: 700; color: #0f172a;
        margin: 0.7rem 0 0.5rem 0;
    }
    .action-desc {
        font-size: 0.85rem; color: #64748b; line-height: 1.5;
    }

    /* ============ BADGES ============ */
    .badge {
        display: inline-block; padding: 4px 12px;
        border-radius: 20px; font-size: 0.72rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.5px;
    }
    .badge-genuine { background: #d1fae5; color: #065f46; }
    .badge-suspicious { background: #fee2e2; color: #991b1b; }
    .badge-pending { background: #fef3c7; color: #92400e; }
    .badge-resolved { background: #d1fae5; color: #065f46; }

    /* ============ INFO ROW ============ */
    .info-row {
        display: flex; padding: 0.7rem 0;
        border-bottom: 1px solid #f1f5f9; font-size: 0.88rem;
    }
    .info-row:last-child { border-bottom: none; }
    .info-label {
        font-weight: 600; color: #64748b;
        min-width: 150px; flex-shrink: 0;
    }
    .info-value { color: #0f172a; flex: 1; font-weight: 500; }

    /* ============ CHECKLIST ============ */
    .checklist-item {
        display: flex; gap: 1rem; padding: 1rem 0;
        border-bottom: 1px solid #f1f5f9;
    }
    .checklist-item:last-child { border-bottom: none; }
    .checklist-num {
        width: 32px; height: 32px; border-radius: 10px;
        background: #ccfbf1; color: #0d9488;
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; font-size: 0.85rem; flex-shrink: 0;
    }
    .checklist-title {
        font-weight: 700; color: #0f172a;
        font-size: 0.92rem; margin-bottom: 0.2rem;
    }
    .checklist-desc {
        font-size: 0.82rem; color: #64748b; line-height: 1.5;
    }

    /* ============ BUTTONS ============ */
    .stButton > button {
        border-radius: 10px; font-weight: 600; font-size: 0.88rem;
        padding: 0.55rem 1.2rem; transition: all 0.2s ease;
        border: 1px solid #e2e8f0; background: white; color: #334155;
    }
    .stButton > button:hover {
        border-color: #14b8a6; color: #0d9488;
        transform: translateY(-1px);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0d9488, #06b6d4);
        border: none; color: white;
        box-shadow: 0 6px 16px -6px rgba(13, 148, 136, 0.6);
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 10px 24px -8px rgba(13, 148, 136, 0.7);
        color: white; transform: translateY(-1px);
    }

    /* ============ INPUTS ============ */
    .stTextInput input, .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 10px !important;
        border-color: #e2e8f0 !important;
        font-size: 0.9rem !important;
        padding: 0.6rem 0.9rem !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #14b8a6 !important;
        box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.1) !important;
    }
    .stTextInput label, .stSelectbox label, .stTextArea label {
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        color: #475569 !important;
    }

    /* ============ FILE UPLOADER ============ */
    [data-testid="stFileUploader"] {
        border-radius: 16px; border: 2px dashed #99f6e4;
        background: #f0fdfa; padding: 1.2rem;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #14b8a6; background: #ccfbf1;
    }

    /* ============ EXPANDER ============ */
    .streamlit-expanderHeader {
        font-weight: 600; font-size: 0.9rem;
        color: #334155; background: #f8fafc !important;
        border-radius: 10px !important;
    }

    /* ============ METRIC SIDEBAR ============ */
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04);
        padding: 0.7rem 0.9rem; border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 0.5rem;
    }
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] * {
        color: #94a3b8 !important; font-size: 0.72rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stMetricValue"] * {
        color: #ffffff !important; font-size: 1.3rem !important;
        font-weight: 700 !important;
    }

    /* ============ EMPTY ============ */
    .empty-state { text-align: center; padding: 3rem 1rem; color: #94a3b8; }
    .empty-icon { font-size: 3rem; margin-bottom: 0.7rem; opacity: 0.4; }

    /* ============ TABS ============ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px; background: white; padding: 5px;
        border-radius: 12px; border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 38px; border-radius: 8px; padding: 0 18px;
        font-weight: 600; font-size: 0.85rem; color: #64748b;
        background: transparent;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0d9488, #06b6d4) !important;
        color: white !important;
    }

    @media (max-width: 768px) {
        .block-container { padding: 1rem !important; }
        .page-title { font-size: 1.5rem; }
        .hero h1 { font-size: 1.4rem; }
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-logo">💊</div>
        <div>
            <div class="brand-name">MediScan AI</div>
            <div class="brand-sub">Medicine Safety</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "🏠  Dashboard",
            "💊  Verify Medicine",
            "📸  Read Prescription",
            "🩺  Symptom Checker",
            "📢  Complaints",
            "🛠️  Department Panel",
        ],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Live Stats")

    stats = get_complaint_stats()
    st.metric("Total Complaints", stats["total"])
    st.metric("Pending", stats["pending"])
    st.metric("Resolved", stats["resolved"])

    st.markdown("<br>")
    st.caption("⚠️ Educational purposes only.")


# ============================================================
# DASHBOARD
# ============================================================
if page == "🏠  Dashboard":
    st.markdown("""
    <div class="hero">
        <div class="hero-content">
            <h1>💊 Welcome to MediScan AI</h1>
            <p>Verify medicines, read prescriptions, and stay safe — all in one place</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI Cards
    stats = get_complaint_stats()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-icon teal">💊</div>
            <div class="kpi-label">Medicines Verified</div>
            <div class="kpi-value">{len(MEDICINES)}</div>
            <div class="kpi-sub">In database</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi blue">
            <div class="kpi-icon blue">📢</div>
            <div class="kpi-label">Total Complaints</div>
            <div class="kpi-value">{stats['total']}</div>
            <div class="kpi-sub">Filed by users</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi orange">
            <div class="kpi-icon orange">⏳</div>
            <div class="kpi-label">Pending</div>
            <div class="kpi-value">{stats['pending']}</div>
            <div class="kpi-sub">Awaiting action</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi purple">
            <div class="kpi-icon purple">✅</div>
            <div class="kpi-label">Resolved</div>
            <div class="kpi-value">{stats['resolved']}</div>
            <div class="kpi-sub">Cases closed</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="page-eyebrow">QUICK ACTIONS</div>
    <h2 style="font-family:'Space Grotesk'; font-size:1.5rem; font-weight:700; color:#0f172a; margin:0 0 1.2rem 0;">
        What would you like to do?
    </h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("""
        <div class="action-card">
            <div style="font-size:2rem;">💊</div>
            <div class="action-title">Verify a Medicine</div>
            <div class="action-desc">
                Upload a photo of the medicine package. Our system will check if it's genuine or fake.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="action-card">
            <div style="font-size:2rem;">📸</div>
            <div class="action-title">Read Prescription</div>
            <div class="action-desc">
                Upload your prescription photo. Get a clean, readable list of medicines.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="action-card">
            <div style="font-size:2rem;">🩺</div>
            <div class="action-title">Symptom Checker</div>
            <div class="action-desc">
                Describe your symptoms. Get safe OTC medicine suggestions instantly.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="action-card">
            <div style="font-size:2rem;">📢</div>
            <div class="action-title">File a Complaint</div>
            <div class="action-desc">
                Found a fake medicine? Report it directly to the government department.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="page-eyebrow">RECENT ACTIVITY</div>
    <h2 style="font-family:'Space Grotesk'; font-size:1.3rem; font-weight:700; color:#0f172a; margin:0 0 1rem 0;">
        Latest Complaints
    </h2>
    """, unsafe_allow_html=True)

    complaints = get_all_complaints()[:3]
    if complaints:
        for c in complaints:
            badge_class = "badge-resolved" if c["status"] == "Resolved" else "badge-pending"
            st.markdown(f"""
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
                    <div>
                        <div style="font-family:'Space Grotesk'; font-weight:700; color:#0d9488; font-size:0.9rem;">
                            🆔 {c['id']}
                        </div>
                        <div style="font-size:0.95rem; color:#0f172a; font-weight:600; margin-top:0.3rem;">
                            💊 {c['medicine']} — 🏪 {c['pharmacy']}
                        </div>
                        <div style="font-size:0.78rem; color:#94a3b8; margin-top:0.4rem;">
                            📍 {c['city']} · 📅 {c['date']} · 👍 {c['upvotes']} upvotes
                        </div>
                    </div>
                    <span class="badge {badge_class}">{c['status']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 No complaints yet. Your activity will appear here.")


# ============================================================
# VERIFY MEDICINE (Image-only)
# ============================================================
elif page == "💊  Verify Medicine":
    st.markdown("""
    <div class="page-head">
        <div class="page-eyebrow">MEDICINE VERIFICATION</div>
        <h1 class="page-title">Verify Your Medicine</h1>
        <div class="page-desc">Upload a photo of the medicine package — we'll check if it's genuine or fake</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📤 Upload Medicine Photo</div>', unsafe_allow_html=True)
        st.caption("Take a clear photo of the front of the medicine package")

        uploaded = st.file_uploader(
            "Upload image",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed",
            key="verify_upload"
        )

        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption="Uploaded Medicine", use_container_width=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">💊</div>
                <p>Upload a photo of the medicine package</p>
                <p style="font-size:0.8rem; color:#cbd5e1; margin-top:0.5rem;">
                    Make sure text on the package is clearly visible
                </p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🔍 Verification Result</div>', unsafe_allow_html=True)

        if not uploaded:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">🔍</div>
                <p>Result will appear here</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("🔎 Analyzing medicine package..."):
                uploaded.seek(0)
                raw_text = extract_text_from_image(uploaded)
                detected = extract_medicine_names(raw_text)

            if not detected:
                st.warning("⚠️ Could not detect any medicine from the image.")
                st.caption("Try a clearer photo with the medicine name visible.")
            else:
                result = verify_by_image_match(detected)

                for r in result["results"]:
                    badge_class = "badge-genuine" if r["status"] == "GENUINE" else "badge-suspicious"
                    icon = "✅" if r["status"] == "GENUINE" else "⚠️"

                    st.markdown(f"""
                    <div style="padding:1rem; background:#f8fafc; border-radius:12px; margin-bottom:1rem; border-left:4px solid {'#10b981' if r['status']=='GENUINE' else '#ef4444'};">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div style="font-family:'Space Grotesk'; font-weight:700; color:#0f172a; font-size:1.05rem;">
                                {icon} {r['medicine']}
                            </div>
                            <span class="badge {badge_class}">{r['status']}</span>
                        </div>
                        <div style="font-size:0.82rem; color:#64748b; margin-top:0.4rem;">
                            Confidence: <b style="color:#0d9488;">{r['confidence']*100:.0f}%</b>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if r["status"] == "GENUINE":
                        st.markdown(f"""
                        <div class="info-row"><span class="info-label">Manufacturer</span><span class="info-value">{r['manufacturer']}</span></div>
                        <div class="info-row"><span class="info-label">Category</span><span class="info-value">{r['category']}</span></div>
                        <div class="info-row"><span class="info-label">Dosage</span><span class="info-value">{r['dosage']}</span></div>
                        <div class="info-row"><span class="info-label">DRAP Price</span><span class="info-value">{r['price']}</span></div>
                        """, unsafe_allow_html=True)

                if result["has_fake"]:
                    st.error("🚨 **Suspicious medicine detected!** We recommend filing a complaint.")
                    if st.button("📢  File a Complaint Now", type="primary", use_container_width=True):
                        st.session_state["goto_complaint"] = True
                        # Auto-file a complaint
                        for r in result["results"]:
                            if r["status"] == "SUSPICIOUS":
                                cid = file_complaint(
                                    medicine_name=r["medicine"],
                                    pharmacy_name="Unknown (via image upload)",
                                    city="Unknown",
                                    description=f"Suspicious medicine detected via image verification. Confidence: {r['confidence']*100:.0f}%",
                                    reporter="MediScan AI (Auto)"
                                )
                                st.success(f"✅ Complaint auto-filed! ID: **{cid}**")
                                st.info("📨 Your complaint has been sent to the Department Panel for review.")
                                st.balloons()
                                break
        st.markdown('</div>', unsafe_allow_html=True)

    # Professional checklist
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="page-eyebrow">VISUAL VERIFICATION GUIDE</div>
    <h2 style="font-family:'Space Grotesk'; font-size:1.3rem; font-weight:700; color:#0f172a; margin:0 0 1rem 0;">
        How to Spot a Fake Medicine
    </h2>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    for i, item in enumerate(get_verification_checklist(), 1):
        st.markdown(f"""
        <div class="checklist-item">
            <div class="checklist-num">{i}</div>
            <div>
                <div class="checklist-title">{item['title']}</div>
                <div class="checklist-desc">{item['desc']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PRESCRIPTION READER
# ============================================================
elif page == "📸  Read Prescription":
    st.markdown("""
    <div class="page-head">
        <div class="page-eyebrow">PRESCRIPTION READER</div>
        <h1 class="page-title">Read Your Prescription</h1>
        <div class="page-desc">Upload a prescription photo — get a clean list of medicines you can download</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📤 Upload Prescription</div>', unsafe_allow_html=True)
        st.caption("Make sure the medicine names are clearly visible")

        uploaded = st.file_uploader(
            "Upload image",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed",
            key="rx_upload"
        )

        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption="Original Prescription", use_container_width=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">📸</div>
                <p>Upload a prescription photo</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📄 Extracted Medicines</div>', unsafe_allow_html=True)

        if not uploaded:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">📄</div>
                <p>Clean medicine list will appear here</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("🤖 Reading prescription..."):
                uploaded.seek(0)
                raw_text = extract_text_from_image(uploaded)
                medicines_found = extract_medicine_names(raw_text)

            if "OCR_ERROR" in raw_text:
                st.error("❌ Could not read the image.")
            elif medicines_found:
                st.success(f"✅ Found **{len(medicines_found)}** medicine(s)")
                for m in medicines_found:
                    st.markdown(f"""
                    <div style="padding:0.9rem 1.1rem; background:#f0fdfa; border-radius:12px; margin-bottom:0.6rem; border-left:4px solid #0d9488;">
                        <div style="font-family:'Space Grotesk'; font-weight:700; color:#0f172a; font-size:1rem;">
                            💊 {m['medicine']}
                        </div>
                        <div style="font-size:0.82rem; color:#64748b; margin-top:0.3rem;">
                            Generic: <b>{m['generic']}</b> · 
                            Confidence: <b style="color:#0d9488;">{m['confidence']*100:.0f}%</b>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Download
                formatted = format_prescription(medicines_found)
                st.markdown("<br>", unsafe_allow_html=True)

                csv_content = "Medicine,Generic,Confidence\n" + "\n".join(
                    [f"{m['medicine']},{m['generic']},{m['confidence']}" for m in medicines_found]
                )

                dc1, dc2 = st.columns(2)
                with dc1:
                    st.download_button(
                        "⬇️ Download as TXT",
                        formatted,
                        file_name=f"prescription_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with dc2:
                    st.download_button(
                        "⬇️ Download as CSV",
                        csv_content,
                        file_name=f"prescription_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            else:
                st.warning("⚠️ No medicines detected. Try a clearer photo.")
                st.caption("Make sure medicine names are clearly visible")

            with st.expander("📄 View raw OCR text"):
                st.text(raw_text)
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# SYMPTOM CHECKER
# ============================================================
elif page == "🩺  Symptom Checker":
    st.markdown("""
    <div class="page-head">
        <div class="page-eyebrow">SYMPTOM CHECKER</div>
        <h1 class="page-title">What Are You Feeling?</h1>
        <div class="page-desc">Describe your symptoms in plain words — get safe OTC medicine suggestions</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📝 Describe Your Symptoms</div>', unsafe_allow_html=True)

        symptom_text = st.text_input(
            "Symptoms (comma-separated)",
            placeholder="e.g., fever, headache, body ache",
            label_visibility="collapsed"
        )
        st.caption("Examples: fever, headache, cough, cold, heartburn, stomach pain, back pain, sore throat, diarrhea, vomiting, menstrual cramps")

        age_group = st.selectbox(
            "Age Group",
            ["Adult", "Child (0-12)", "Elderly (60+)"]
        )

        if st.button("🔍  Get Suggestions", type="primary", use_container_width=True):
            st.session_state["symptom_result"] = suggest_medicines(symptom_text, age_group)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">💡 Suggestions</div>', unsafe_allow_html=True)

        result = st.session_state.get("symptom_result")

        if not result:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">💡</div>
                <p>Enter your symptoms to get suggestions</p>
            </div>
            """, unsafe_allow_html=True)
        elif not result.get("found"):
            st.warning(result["message"])
        else:
            for r in result["results"]:
                st.markdown(f"""
                <div style="padding:1rem 1.2rem; background:#f0fdfa; border-radius:12px; margin-bottom:1rem; border-left:4px solid #0d9488;">
                    <div style="font-family:'Space Grotesk'; font-weight:700; color:#0f172a; font-size:1rem;">
                        🩺 {r['symptom'].title()}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if r["medicines"]:
                    st.markdown("**💊 Suggested OTC Medicines:**")
                    for m in r["medicines"]:
                        st.markdown(f"""
                        <div style="padding:0.8rem 1rem; background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; margin-bottom:0.5rem;">
                            <div style="font-weight:700; color:#0f172a;">{m['name']}</div>
                            <div style="font-size:0.8rem; color:#64748b; margin-top:0.2rem;">
                                {m['generic']} · {m['dosage']} · <b style="color:#0d9488;">{m['price']}</b>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No OTC medicine — please consult a doctor")

                st.markdown("**⚠️ Warnings:**")
                for w in r["warnings"]:
                    st.markdown(f"- {w}")

                st.markdown("**🚨 See a Doctor If:**")
                for rf in r["red_flags"]:
                    st.markdown(f"- {rf}")

                st.markdown("---")
        st.markdown('</div>', unsafe_allow_html=True)

    st.caption("⚠️ This is NOT a medical diagnosis. Always consult a licensed doctor before taking any medicine.")


# ============================================================
# COMPLAINTS
# ============================================================
elif page == "📢  Complaints":
    st.markdown("""
    <div class="page-head">
        <div class="page-eyebrow">COMMUNITY REPORTS</div>
        <h1 class="page-title">Report & Track Complaints</h1>
        <div class="page-desc">File a complaint about a fake medicine — track it and see the department's response</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📝 File New Complaint", "📋 View All Complaints"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">File a Complaint</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            med_name = st.text_input("Medicine Name", placeholder="e.g., Panadol")
            city = st.selectbox("City", ["Karachi", "Lahore", "Islamabad", "Rawalpindi",
                                         "Faisalabad", "Multan", "Peshawar", "Quetta"])
        with c2:
            pharmacy = st.text_input("Pharmacy / Shop Name", placeholder="e.g., XYZ Medical Store")
            reporter = st.text_input("Your Name (optional)", value="Anonymous")

        description = st.text_area(
            "Description",
            placeholder="Describe the issue: What did you notice? Where did you buy it? Any symptoms?",
            height=100
        )

        if st.button("📤  Submit Complaint", type="primary", use_container_width=True):
            if not med_name.strip() or not pharmacy.strip() or not description.strip():
                st.error("Please fill all required fields.")
            else:
                cid = file_complaint(med_name, pharmacy, city, description, reporter)
                st.success(f"✅ Complaint submitted! ID: **{cid}**")
                st.info("📨 Your complaint has been forwarded to the Department Panel for review.")
                st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        complaints = get_all_complaints()

        if not complaints:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">📭</div>
                <p>No complaints yet</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for c in complaints:
                badge_class = "badge-resolved" if c["status"] == "Resolved" else "badge-pending"
                with st.expander(f"🆔 {c['id']} — 💊 {c['medicine']} — {c['status']}"):
                    st.markdown(f"""
                    <div style="padding:1rem; background:#f8fafc; border-radius:12px; margin-bottom:1rem;">
                        <div class="info-row"><span class="info-label">Medicine</span><span class="info-value">{c['medicine']}</span></div>
                        <div class="info-row"><span class="info-label">Pharmacy</span><span class="info-value">{c['pharmacy']}</span></div>
                        <div class="info-row"><span class="info-label">City</span><span class="info-value">{c['city']}</span></div>
                        <div class="info-row"><span class="info-label">Reported by</span><span class="info-value">{c['reporter']}</span></div>
                        <div class="info-row"><span class="info-label">Date</span><span class="info-value">{c['date']}</span></div>
                        <div class="info-row"><span class="info-label">Status</span><span class="info-value"><span class="badge {badge_class}">{c['status']}</span></span></div>
                    </div>
                    <div style="padding:1rem; background:#fef3c7; border-radius:10px; margin-bottom:1rem;">
                        <b>Description:</b><br>{c['description']}
                    </div>
                    """, unsafe_allow_html=True)

                    col_up, col_comment = st.columns([1, 3])
                    with col_up:
                        if st.button(f"👍 Upvote ({c['upvotes']})", key=f"up_{c['id']}", use_container_width=True):
                            upvote_complaint(c["id"])
                            st.rerun()

                    with col_comment:
                        comment = st.text_input(
                            "Add comment",
                            placeholder="Your comment...",
                            key=f"comment_{c['id']}",
                            label_visibility="collapsed"
                        )
                        if st.button("💬  Post Comment", key=f"cbtn_{c['id']}"):
                            if comment.strip():
                                add_comment(c["id"], comment)
                                st.rerun()

                    if c["comments"]:
                        st.markdown("**💬 Comments:**")
                        for cm in c["comments"]:
                            st.markdown(f"- **{cm['user']}** ({cm['date']}): {cm['text']}")

                    if c["status"] == "Resolved" and c["resolution"]:
                        st.success(f"✅ **Resolved:** {c['resolution']}")
                        st.caption(f"Resolved on: {c['resolved_date']}")


# ============================================================
# DEPARTMENT PANEL
# ============================================================
elif page == "🛠️  Department Panel":
    st.markdown("""
    <div class="page-head">
        <div class="page-eyebrow">GOVERNMENT ACCESS</div>
        <h1 class="page-title">Department Panel</h1>
        <div class="page-desc">Review, investigate, and resolve complaints from citizens</div>
    </div>
    """, unsafe_allow_html=True)

    complaints = get_all_complaints()
    pending = [c for c in complaints if c["status"] == "Pending"]

    if not pending:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🎉</div>
            <h3 style="color:#10b981;">All caught up!</h3>
            <p>No pending complaints awaiting action.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"**{len(pending)}** pending complaint(s) awaiting review.")

        for c in pending:
            with st.expander(f"🆔 {c['id']} — 💊 {c['medicine']} — {c['pharmacy']}, {c['city']}"):
                st.markdown(f"""
                <div class="info-row"><span class="info-label">Medicine</span><span class="info-value">{c['medicine']}</span></div>
                <div class="info-row"><span class="info-label">Pharmacy</span><span class="info-value">{c['pharmacy']}</span></div>
                <div class="info-row"><span class="info-label">City</span><span class="info-value">{c['city']}</span></div>
                <div class="info-row"><span class="info-label">Reported by</span><span class="info-value">{c['reporter']}</span></div>
                <div class="info-row"><span class="info-label">Date</span><span class="info-value">{c['date']}</span></div>
                <div class="info-row"><span class="info-label">Upvotes</span><span class="info-value">👍 {c['upvotes']}</span></div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="padding:0.9rem 1rem; background:#fef3c7; border-radius:10px; margin:0.8rem 0;">
                    <b>Description:</b><br>{c['description']}
                </div>
                """, unsafe_allow_html=True)

                resolution = st.text_area(
                    "Resolution notes",
                    placeholder="What action was taken? e.g., Pharmacy inspected, medicine seized, warning issued...",
                    key=f"res_{c['id']}",
                    height=80
                )

                if st.button("✅  Mark as Resolved", key=f"resolve_{c['id']}",
                             type="primary", use_container_width=True):
                    if resolution.strip():
                        resolve_complaint(c["id"], resolution)
                        st.success(f"Resolved {c['id']}")
                        st.rerun()
                    else:
                        st.error("Please add resolution notes.")


# ============================================================
# FOOTER
# ============================================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#94a3b8; font-size:0.78rem; padding:1rem 0; border-top:1px solid #e2e8f0;">
    MediScan AI v3.0  ·  Educational purposes only  ·  Built with Streamlit + Tesseract OCR
</div>
""", unsafe_allow_html=True)
