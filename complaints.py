"""
MediScan AI - Complaint System
Users can report fake medicines → Government department resolves
"""
import streamlit as st
from datetime import datetime
import hashlib


# Initialize complaints in session state
def init_complaints():
    if "complaints" not in st.session_state:
        st.session_state.complaints = []


def generate_complaint_id(medicine: str, pharmacy: str) -> str:
    raw = f"{medicine}{pharmacy}{datetime.now()}"
    return "CMP-" + hashlib.md5(raw.encode()).hexdigest()[:6].upper()


def file_complaint(medicine_name: str, pharmacy_name: str, city: str,
                   description: str, reporter: str = "Anonymous"):
    """File a new complaint."""
    complaint_id = generate_complaint_id(medicine_name, pharmacy_name)

    complaint = {
        "id": complaint_id,
        "medicine": medicine_name,
        "pharmacy": pharmacy_name,
        "city": city,
        "description": description,
        "reporter": reporter,
        "status": "Pending",
        "priority": "High",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "upvotes": 0,
        "comments": [],
        "resolution": None,
        "resolved_date": None,
    }

    st.session_state.complaints.append(complaint)
    return complaint_id


def add_comment(complaint_id: str, comment: str, user: str = "Anonymous"):
    """Add a comment to a complaint."""
    for c in st.session_state.complaints:
        if c["id"] == complaint_id:
            c["comments"].append({
                "user": user,
                "text": comment,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
            return True
    return False


def upvote_complaint(complaint_id: str):
    """Upvote a complaint."""
    for c in st.session_state.complaints:
        if c["id"] == complaint_id:
            c["upvotes"] += 1
            return True
    return False


def resolve_complaint(complaint_id: str, resolution: str):
    """Mark complaint as resolved (department action)."""
    for c in st.session_state.complaints:
        if c["id"] == complaint_id:
            c["status"] = "Resolved"
            c["resolution"] = resolution
            c["resolved_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            return True
    return False


def get_all_complaints():
    return sorted(
        st.session_state.complaints,
        key=lambda x: x["date"],
        reverse=True
    )


def get_complaint_stats():
    complaints = st.session_state.complaints
    return {
        "total": len(complaints),
        "pending": len([c for c in complaints if c["status"] == "Pending"]),
        "resolved": len([c for c in complaints if c["status"] == "Resolved"]),
        "upvotes": sum(c["upvotes"] for c in complaints),
    }
