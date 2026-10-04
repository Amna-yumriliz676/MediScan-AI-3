"""
MediScan AI — Complete App
4 Features + Dashboard + Complaint System
"""
import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime

from database import (
    MEDICINES, INTERACTIONS, SYMPTOMS,
    search_medicine, check_interaction,
    get_all_medicine_names, get_otc_medicines,
)
from ocr_utils import (
    extract_text_from_image, extract_medicine_names, format_prescription,
)
from verifier import verify_by_barcode, verify_by_name, get_verification_checklist
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
# CSS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header {visibility: hidden;}
    .block-container { padding: 1.5rem 2rem; max-width: 100%; }
    .stApp { background: #f7f8fc; }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: #0f172a;
        min-width: 270px !important;
        max-width: 270px !important;
    }
    [data-testid="stSidebar"] * { color: #cbd5e1 !important; }
    [data-testid="stSidebar"] .stRadio > label { display: none; }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 4px; }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
        background: transparent; padding: 10px 16px; border-radius: 10px;
        cursor: pointer; transition: all 0.2s; font-weight: 500;
        font-size: 0.88rem; width: 100%; border: none;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
        background: rgba(255,255,255,0.06) !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(135deg, #10b981, #06b6d4) !important;
        box-shadow: 0 4px 12px rgba(16,185,129,0.35);
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) * {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stRadio input[type="radio"] { display: none; }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label > div:first-child {
        display: none;
    }

    /* BRAND */
    .brand { display: flex; align-items: center; gap: 0.7rem;
        padding: 1rem 0.5rem 1.5rem 0.5rem;
        border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 1rem; }
    .brand-logo { width: 42px; height: 42px;
        background: linear-gradient(135deg, #10b981, #06b6d4);
        border-radius: 12px; display: flex; align-items: center;
        justify-content: center; font-size: 1.3rem;
        box-shadow: 0 4px 12px rgba(16,185,129,0.4); }
    .brand-name { font-weight: 800; font-size: 1.1rem; color: #fff !important; }
    .brand-sub { font-size: 0.68rem; color: #10b981 !important;
        font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }

    /* PAGE HEADER */
    .page-header { margin-bottom: 1.5rem; }
    .page-title { font-size: 1.7rem; font-weight: 800; color: #0f172a;
        letter-spacing: -0.6px; margin: 0; }
    .page-sub { font-size: 0.88rem; color: #64748b; margin-top: 0.3rem; }

    /* HERO */
    .hero {
        background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
        padding: 1.8rem 2rem; border-radius: 18px; color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 15px 35px -15px rgba(16,185,129,0.4);
        position: relative; overflow: hidden;
    }
    .hero::before { content: ""; position: absolute; top: -50%; right: -10%;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(255,255,255,0.15), transparent 70%);
        border-radius: 50%; }
    .hero h1 { font-size: 1.8rem; font-weight: 800; margin: 0 0 0.4rem 0;
        letter-spacing: -0.5px; position: relative; }
    .hero p { font-size: 0.95rem; opacity: 0.95; margin: 0; position: relative; }

    /* CARD */
    .card { background: white; border: 1px solid #e2e8f0;
        border-radius: 14px; padding: 1.2rem 1.3rem;
        margin-bottom: 1rem; transition: all 0.2s; }
    .card:hover { box-shadow: 0 8px 20px -10px rgba(0,0,0,0.1);
        border-color: #cbd5e1; }

    /* KPI */
    .kpi-card { background: white; padding: 1.2rem 1.3rem;
        border-radius: 14px; border: 1px solid #eef0f4;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03); height: 100%; }
    .kpi-icon { width: 42px; height: 42px; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.2rem; margin-bottom: 0.8rem; }
    .kpi-icon.green { background: #d1fae5; }
    .kpi-icon.blue { background: #dbeafe; }
    .kpi-icon.orange { background: #ffedd5; }
    .kpi-icon.purple { background: #f3e8ff; }
    .kpi-icon.red { background: #fee2e2; }
    .kpi-label { font-size: 0.75rem; color: #64748b; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.3rem; }
    .kpi-value { font-size: 1.6rem; font-weight: 800;
        color: #0f172a; line-height: 1.1; }

    /* SEVERITY */
    .sev { display: inline-block; padding: 4px 12px;
        border-radius: 20px; font-size: 0.72rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.5px; }
    .sev-severe { background: #fee2e2; color: #991b1b; }
    .sev-moderate { background: #fef3c7; color: #92400e; }
    .sev-safe { background: #d1fae5; color: #065f46; }
    .sev-pending { background: #fef3c7; color: #92400e; }
    .sev-resolved { background: #d1fae5; color: #065f46; }

    /* INFO ROWS */
    .info-row { display: flex; padding: 0.6rem 0;
        border-bottom: 1px solid #f1f5f9; font-size: 0.88rem; }
    .info-row:last-child { border-bottom: none; }
    .info-label { font-weight: 600; color: #64748b;
        min-width: 140px; flex-shrink: 0; }
    .info-value { color: #0f172a; flex: 1; }

    /* BUTTONS */
    .stButton > button {
        border-radius: 10px; font-weight: 600; font-size: 0.85rem;
        padding: 0.5rem 1.1rem; transition: all 0.2s ease;
        border: 1px solid #e2e8f0; background: white; color: #334155;
    }
    .stButton > button:hover {
        border-color: #a7f3d0; color: #10b981; transform: translateY(-1px);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10b981, #06b6d4);
        border: none; color: white;
        box-shadow: 0 4px 12px -4px rgba(16,185,129,0.5);
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 8px 20px -6px rgba(16,185,129,0.6); color: white;
    }

    /* INPUTS */
    .stTextInput input, .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 10px !important; border-color: #e2e8f0 !important;
        font-size: 0.88rem !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 3px rgba(16,185,129,0.1) !important;
    }

    /* FILE UPLOADER */
    [data-testid="stFileUploader"] {
        border-radius: 14px; border: 2px dashed #a7f3d0;
        background: #f0fdf4; padding: 1rem;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #10b981; background: #ecfdf5;
    }

    /* EMPTY STATE */
    .empty-state { text-align: center; padding: 3rem 1rem; color: #94a3b8; }
    .empty-state-icon { font-size: 3rem; margin-bottom: 0.7rem; opacity: 0.4; }

    /* METRIC SIDEBAR */
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04); padding: 0.7rem 0.9rem;
        border-radius: 10px; border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 0.5rem;
    }
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] * {
        color: #94a3b8 !important; font-size: 0.75rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stMetricValue"] * {
        color: #ffffff !important; font-size: 1.3rem !important;
        font-weight: 700 !important;
    }

    @media (max-width: 768px) {
        .block-container { padding: 1rem !important; }
        .page-title { font-size: 1.3rem; }
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
            "💊  Medicine Verifier",
            "📸  Prescription Reader",
            "⚗️  Interaction Checker",
            "🩺  Symptom Suggester",
            "📢  Complaints",
            "🛠️  Department Panel",
            "💾  Database",
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
# PAGE: DASHBOARD
# ============================================================
if page == "🏠  Dashboard":
    st.markdown("""
    <div class="hero">
        <h1>💊 MediScan AI Dashboard</h1>
        <p>Real-time overview of medicine safety, complaints, and activity</p>
    </div>
    """, unsafe_allow_html=True)

    # Live stats
    stats = get_complaint_stats()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon green">💊</div>
            <div class="kpi-label">Medicines in DB</div>
            <div class="kpi-value">{len(MEDICINES)}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon blue">⚗️</div>
            <div class="kpi-label">Interactions</div>
            <div class="kpi-value">{len(INTERACTIONS)}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon orange">📢</div>
            <div class="kpi-label">Pending Complaints</div>
            <div class="kpi-value">{stats['pending']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon purple">👍</div>
            <div class="kpi-label">Total Upvotes</div>
            <div class="kpi-value">{stats['upvotes']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎯 Quick Actions")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card">
            <h3 style="margin:0 0 0.5rem 0; color:#0f172a;">💊 Verify a Medicine</h3>
            <p style="color:#64748b; font-size:0.9rem; margin:0;">
                Barcode ya naam se check karo — genuine hai ya fake.
            </p>
        </div>
        <div class="card">
            <h3 style="margin:0 0 0.5rem 0; color:#0f172a;">📸 Read Prescription</h3>
            <p style="color:#64748b; font-size:0.9rem; margin:0;">
                Photo upload karo, clean text mile + download karo.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <h3 style="margin:0 0 0.5rem 0; color:#0f172a;">⚗️ Check Interactions</h3>
            <p style="color:#64748b; font-size:0.9rem; margin:0;">
                Do ya zyada medicines safe hain ya nahi — pata karo.
            </p>
        </div>
        <div class="card">
            <h3 style="margin:0 0 0.5rem 0; color:#0f172a;">📢 File a Complaint</h3>
            <p style="color:#64748b; font-size:0.9rem; margin:0;">
                Fake medicine mile to government tak report karo.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Recent complaints
    st.markdown("### 📢 Recent Complaints")
    complaints = get_all_complaints()[:5]
    if complaints:
        for c in complaints:
            status_class = "sev-resolved" if c["status"] == "Resolved" else "sev-pending"
            st.markdown(f"""
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:start;">
                    <div>
                        <h4 style="margin:0 0 0.3rem 0; color:#0f172a;">🆔 {c['id']}</h4>
                        <div style="font-size:0.88rem; color:#334155;">
                            💊 {c['medicine']} — 🏪 {c['pharmacy']}, {c['city']}
                        </div>
                        <div style="font-size:0.75rem; color:#94a3b8; margin-top:0.4rem;">
                            📅 {c['date']} · 👍 {c['upvotes']} upvotes · 💬 {len(c['comments'])} comments
                        </div>
                    </div>
                    <span class="sev {status_class}">{c['status']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No complaints yet. Go to Complaints tab to file one.")


# ============================================================
# PAGE: MEDICINE VERIFIER
# ============================================================
elif page == "💊  Medicine Verifier":
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">💊 Medicine Verifier</h1>
        <div class="page-sub">Barcode ya naam se verify karo — genuine hai ya fake</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔢 By Barcode", "🔤 By Name"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### Barcode enter karo")
        st.caption("Demo barcodes: 8901234567890 (Panadol), 8901234567891 (Brufen)")
        barcode = st.text_input("Barcode", placeholder="e.g., 8901234567890",
                                label_visibility="collapsed")

        if st.button("🔍  Verify Barcode", type="primary", use_container_width=True):
            result = verify_by_barcode(barcode)
            if result["status"] == "GENUINE":
                st.success(result["message"])
                if result["medicine"]:
                    med = result["medicine"]
                    st.markdown(f"""
                    <div class="card">
                        <div class="info-row"><span class="info-label">Brand</span><span class="info-value">{med['name']}</span></div>
                        <div class="info-row"><span class="info-label">Generic</span><span class="info-value">{med['generic']}</span></div>
                        <div class="info-row"><span class="info-label">Manufacturer</span><span class="info-value">{med['manufacturer']}</span></div>
                        <div class="info-row"><span class="info-label">Category</span><span class="info-value">{med['category']}</span></div>
                        <div class="info-row"><span class="info-label">Dosage</span><span class="info-value">{med['dosage']}</span></div>
                        <div class="info-row"><span class="info-label">Price</span><span class="info-value">{med['price']}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                for check in result.get("checks", []):
                    st.markdown(f"- {check}")
            elif result["status"] == "SUSPICIOUS":
                st.error(result["message"])
                st.markdown("**🚨 Recommended:**")
                for check in result.get("checks", []):
                    st.markdown(f"- {check}")
                st.markdown("---")
                if st.button("📢 File a Complaint", type="primary"):
                    st.session_state["goto_complaint"] = barcode
                    st.info("Go to Complaints tab to report this.")
            else:
                st.warning(result["message"])
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        name = st.text_input("Medicine name", placeholder="e.g., Panadol",
                             label_visibility="collapsed")

        if st.button("🔍  Verify Name", type="primary", use_container_width=True):
            result = verify_by_name(name)
            if result["status"] == "GENUINE":
                st.success(result["message"])
                med = result["medicine"]
                st.markdown(f"""
                <div class="card">
                    <div class="info-row"><span class="info-label">Uses</span><span class="info-value">{med['uses']}</span></div>
                    <div class="info-row"><span class="info-label">Dosage</span><span class="info-value">{med['dosage']}</span></div>
                    <div class="info-row"><span class="info-label">Side Effects</span><span class="info-value">{med['side_effects']}</span></div>
                </div>
                """, unsafe_allow_html=True)
            elif result["status"] == "SUSPICIOUS":
                st.warning(result["message"])
            else:
                st.error(result["message"])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ✅ Visual Verification Checklist")
    for item in get_verification_checklist():
        st.markdown(f"- {item}")


# ============================================================
# PAGE: PRESCRIPTION READER
# ============================================================
elif page == "📸  Prescription Reader":
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">📸 Prescription Reader</h1>
        <div class="page-sub">Photo upload karo → Clean readable text mile + Download</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📤 Upload Prescription")
        uploaded = st.file_uploader(
            "Choose image",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption="Original Prescription", use_container_width=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">📸</div>
                <p>Upload a prescription photo</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📄 Extracted (Readable)")

        if not uploaded:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">📄</div>
                <p>Readable text will appear here</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("🤖 Reading prescription..."):
                uploaded.seek(0)
                raw_text = extract_text_from_image(uploaded)
                medicines_found = extract_medicine_names(raw_text)

            if "OCR_ERROR" in raw_text:
                st.error("❌ Could not read the image.")
            else:
                if medicines_found:
                    st.success(f"✅ Found **{len(medicines_found)}** medicine(s)")
                    for m in medicines_found:
                        conf_color = "#10b981" if m["confidence"] > 0.85 else "#f59e0b"
                        st.markdown(f"""
                        <div class="card">
                            <h4 style="margin:0 0 0.4rem 0;">💊 {m['medicine']}</h4>
                            <div class="info-row">
                                <span class="info-label">Generic</span>
                                <span class="info-value">{m['generic']}</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">Confidence</span>
                                <span class="info-value" style="color:{conf_color}; font-weight:700;">
                                    {m['confidence']*100:.0f}%
                                </span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ No medicines detected.")

                # Download section
                st.markdown("---")
                st.markdown("##### ⬇️ Download")
                formatted = format_prescription(medicines_found, raw_text)

                c1, c2 = st.columns(2)
                with c1:
                    st.download_button(
                        "⬇️ Download TXT",
                        formatted,
                        file_name=f"prescription_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with c2:
                    st.download_button(
                        "⬇️ Download CSV",
                        "Medicine,Generic,Confidence\n" + "\n".join(
                            [f"{m['medicine']},{m['generic']},{m['confidence']}"
                             for m in medicines_found]
                        ),
                        file_name=f"prescription_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

                with st.expander("📄 View raw OCR text"):
                    st.text(raw_text)
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PAGE: INTERACTION CHECKER
# ============================================================
elif page == "⚗️  Interaction Checker":
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">⚗️ Drug Interaction Checker</h1>
        <div class="page-sub">Do ya zyada medicines safe hain ya nahi</div>
    </div>
    """, unsafe_allow_html=True)

    med_names = get_all_medicine_names()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### Select medicines to check")

    num_meds = st.slider("How many medicines?", 2, 5, 2)
    selected = []
    cols = st.columns(num_meds)
    for i in range(num_meds):
        with cols[i]:
            selected.append(st.selectbox(
                f"Medicine {i+1}",
                med_names,
                index=min(i, len(med_names)-1),
                key=f"med_{i}"
            ))

    if st.button("🔍  Check All Interactions", type="primary", use_container_width=True):
        st.markdown("### 📋 Results")

        from itertools import combinations
        pairs = list(combinations(selected, 2))
        severe_count = 0

        for a, b in pairs:
            result = check_interaction(a, b)
            sev = result["severity"]
            badge_class = {"SEVERE": "sev-severe", "MODERATE": "sev-moderate",
                          "SAFE": "sev-safe"}.get(sev, "sev-safe")

            if sev == "SEVERE":
                severe_count += 1

            st.markdown(f"""
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4 style="margin:0;">{a} + {b}</h4>
                    <span class="sev {badge_class}">{sev}</span>
                </div>
                <div class="info-row" style="margin-top:0.6rem;">
                    <span class="info-label">Risk</span>
                    <span class="info-value">{result['risk']}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Action</span>
                    <span class="info-value">{result['action']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if severe_count > 0:
            st.error(f"🚨 **{severe_count} SEVERE interaction(s) found!** Consult doctor immediately.")
        elif all(check_interaction(a, b)["severity"] == "SAFE" for a, b in pairs):
            st.success("✅ All combinations are SAFE.")
        else:
            st.warning("⚠️ Some moderate interactions found. Take precautions.")
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PAGE: SYMPTOM SUGGESTER
# ============================================================
elif page == "🩺  Symptom Suggester":
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">🩺 Symptom-to-Medicine Suggester</h1>
        <div class="page-sub">Symptoms batao → Safe OTC medicines suggest karega</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    symptom_text = st.text_input(
        "Symptoms",
        placeholder="e.g., fever, headache, body ache",
        label_visibility="collapsed"
    )
    age_group = st.selectbox(
        "Age Group",
        ["Adult", "Child (0-12)", "Elderly (60+)"]
    )

    if st.button("🔍  Get Suggestions", type="primary", use_container_width=True):
        result = suggest_medicines(symptom_text, age_group)

        if not result.get("found"):
            st.warning(result["message"])
        else:
            st.success("✅ Suggestions found")
            for r in result["results"]:
                st.markdown(f"""
                <div class="card">
                    <h4 style="margin:0 0 0.6rem 0;">🩺 {r['symptom'].title()}</h4>
                """, unsafe_allow_html=True)

                if r["medicines"]:
                    st.markdown("**💊 Suggested OTC Medicines:**")
                    for m in r["medicines"]:
                        st.markdown(f"""
                        - **{m['name']}** ({m['generic']})
                          - Dosage: {m['dosage']}
                          - Price: {m['price']}
                        """)
                else:
                    st.info("No OTC medicine — consult doctor")

                st.markdown("**⚠️ Warnings:**")
                for w in r["warnings"]:
                    st.markdown(f"- {w}")

                st.markdown("**🚨 See Doctor If:**")
                for rf in r["red_flags"]:
                    st.markdown(f"- {rf}")

                st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.caption("⚠️ This is NOT a diagnosis. Always consult a licensed doctor.")


# ============================================================
# PAGE: COMPLAINTS
# ============================================================
elif page == "📢  Complaints":
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">📢 Complaints</h1>
        <div class="page-sub">Fake medicine report karo — government department tak pahunchao</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📝 File Complaint", "📋 View All"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### File a Complaint")

        c1, c2 = st.columns(2)
        with c1:
            med_name = st.text_input("Medicine Name", placeholder="e.g., Panadol")
            city = st.selectbox("City", ["Karachi", "Lahore", "Islamabad", "Rawalpindi",
                                         "Faisalabad", "Multan", "Peshawar", "Quetta"])
        with c2:
            pharmacy = st.text_input("Pharmacy / Shop Name", placeholder="e.g., XYZ Medical")
            reporter = st.text_input("Your Name (optional)", value="Anonymous")

        description = st.text_area("Description",
            placeholder="Kya masla hai? Kahan se kharidi? Kya hua?")

        if st.button("📤 Submit Complaint", type="primary", use_container_width=True):
            if not med_name.strip() or not pharmacy.strip() or not description.strip():
                st.error("Please fill all required fields.")
            else:
                cid = file_complaint(med_name, pharmacy, city, description, reporter)
                st.success(f"✅ Complaint submitted! ID: **{cid}**")
                st.info("📨 Your complaint has been sent to DRAP (Drug Regulatory Authority of Pakistan).")
                st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        complaints = get_all_complaints()

        if not complaints:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">📭</div>
                <p>No complaints yet</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for c in complaints:
                status_class = "sev-resolved" if c["status"] == "Resolved" else "sev-pending"
                with st.expander(f"🆔 {c['id']} — 💊 {c['medicine']} — {c['status']}"):
                    st.markdown(f"""
                    <div class="card">
                        <div style="display:flex; justify-content:space-between;">
                            <div>
                                <div class="info-row"><span class="info-label">Medicine</span><span class="info-value">{c['medicine']}</span></div>
                                <div class="info-row"><span class="info-label">Pharmacy</span><span class="info-value">{c['pharmacy']}, {c['city']}</span></div>
                                <div class="info-row"><span class="info-label">Reporter</span><span class="info-value">{c['reporter']}</span></div>
                                <div class="info-row"><span class="info-label">Date</span><span class="info-value">{c['date']}</span></div>
                                <div class="info-row"><span class="info-label">Status</span><span class="info-value"><span class="sev {status_class}">{c['status']}</span></span></div>
                            </div>
                        </div>
                        <div style="margin-top:0.8rem; padding:0.8rem; background:#f8fafc; border-radius:8px;">
                            <b>Description:</b><br>{c['description']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Upvote + comments
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
                        if st.button("💬 Post Comment", key=f"cbtn_{c['id']}"):
                            if comment.strip():
                                add_comment(c["id"], comment)
                                st.rerun()

                    # Show comments
                    if c["comments"]:
                        st.markdown("**💬 Comments:**")
                        for cm in c["comments"]:
                            st.markdown(f"- **{cm['user']}** ({cm['date']}): {cm['text']}")

                    # Resolution
                    if c["status"] == "Resolved" and c["resolution"]:
                        st.success(f"✅ **Resolved:** {c['resolution']}")
                        st.caption(f"Resolved on: {c['resolved_date']}")


# ============================================================
# PAGE: DEPARTMENT PANEL
# ============================================================
elif page == "🛠️  Department Panel":
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">🛠️ Department Panel</h1>
        <div class="page-sub">Government officials — complaints review aur resolve karein</div>
    </div>
    """, unsafe_allow_html=True)

    complaints = get_all_complaints()
    pending = [c for c in complaints if c["status"] == "Pending"]

    if not pending:
        st.success("🎉 All complaints resolved!")
    else:
        st.info(f"**{len(pending)}** pending complaints awaiting action.")

        for c in pending:
            with st.expander(f"🆔 {c['id']} — 💊 {c['medicine']} — {c['pharmacy']}"):
                st.markdown(f"""
                <div class="card">
                    <div class="info-row"><span class="info-label">Medicine</span><span class="info-value">{c['medicine']}</span></div>
                    <div class="info-row"><span class="info-label">Pharmacy</span><span class="info-value">{c['pharmacy']}, {c['city']}</span></div>
                    <div class="info-row"><span class="info-label">Reporter</span><span class="info-value">{c['reporter']}</span></div>
                    <div class="info-row"><span class="info-label">Date</span><span class="info-value">{c['date']}</span></div>
                    <div class="info-row"><span class="info-label">Upvotes</span><span class="info-value">👍 {c['upvotes']}</span></div>
                </div>
                <div style="margin:0.8rem 0; padding:0.8rem; background:#fef3c7; border-radius:8px;">
                    <b>Description:</b><br>{c['description']}
                </div>
                """, unsafe_allow_html=True)

                resolution = st.text_area(
                    "Resolution notes",
                    placeholder="Action taken...",
                    key=f"res_{c['id']}"
                )

                if st.button("✅ Mark as Resolved", key=f"resolve_{c['id']}",
                             type="primary", use_container_width=True):
                    if resolution.strip():
                        resolve_complaint(c["id"], resolution)
                        st.success(f"Resolved {c['id']}")
                        st.rerun()
                    else:
                        st.error("Please add resolution notes.")


# ============================================================
# PAGE: DATABASE
# ============================================================
elif page == "💾  Database":
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">💾 Medicine Database</h1>
        <div class="page-sub">Browse all verified medicines</div>
    </div>
    """, unsafe_allow_html=True)

    search = st.text_input("🔍 Search", placeholder="Name, generic, uses, category")
    filtered = search_medicine(search) if search.strip() else MEDICINES

    st.caption(f"Showing **{len(filtered)}** of **{len(MEDICINES)}** medicines")

    for med in filtered:
        otc_badge = "🟢 OTC" if med["otc"] else "🔴 Rx"
        with st.expander(f"💊 {med['name']} — {med['generic']}  ·  {otc_badge}  ·  {med['price']}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div class="card">
                    <div class="info-row"><span class="info-label">Brand</span><span class="info-value">{med['name']}</span></div>
                    <div class="info-row"><span class="info-label">Generic</span><span class="info-value">{med['generic']}</span></div>
                    <div class="info-row"><span class="info-label">Category</span><span class="info-value">{med['category']}</span></div>
                    <div class="info-row"><span class="info-label">Manufacturer</span><span class="info-value">{med['manufacturer']}</span></div>
                    <div class="info-row"><span class="info-label">Barcode</span><span class="info-value">{med['barcode']}</span></div>
                    <div class="info-row"><span class="info-label">Price</span><span class="info-value">{med['price']}</span></div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="card">
                    <div class="info-row"><span class="info-label">Uses</span><span class="info-value">{med['uses']}</span></div>
                    <div class="info-row"><span class="info-label">Dosage</span><span class="info-value">{med['dosage']}</span></div>
                    <div class="info-row"><span class="info-label">Side Effects</span><span class="info-value">{med['side_effects']}</span></div>
                </div>
                """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#94a3b8; font-size:0.78rem; padding:1rem 0; border-top:1px solid #e2e8f0;">
    MediScan AI v2.0  ·  Educational purposes only  ·  Built with Streamlit
</div>
""", unsafe_allow_html=True)
