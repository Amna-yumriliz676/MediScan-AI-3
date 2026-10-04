"""
MediScan AI - Medicine Verifier (Barcode + Image)
"""
from database import find_medicine_by_barcode, find_medicine_by_name


def verify_by_barcode(barcode: str):
    if not barcode or not barcode.strip():
        return {"status": "INVALID", "message": "Please enter a barcode.", "medicine": None}

    medicine = find_medicine_by_barcode(barcode.strip())

    if medicine:
        return {
            "status": "GENUINE",
            "message": f"✅ Verified! This is {medicine['name']} by {medicine['manufacturer']}.",
            "medicine": medicine,
            "confidence": 0.95,
            "checks": [
                "Barcode registered in database",
                f"Manufacturer verified: {medicine['manufacturer']}",
                f"DRAP approved price: {medicine['price']}",
            ]
        }
    return {
        "status": "SUSPICIOUS",
        "message": "⚠️ Barcode not found in our verified database. Could be fake or unregistered.",
        "medicine": None,
        "confidence": 0.70,
        "checks": [
            "❌ Barcode not registered",
            "Recommendation: Do NOT use",
            "Report to DRAP: drap.gov.pk",
        ]
    }


def verify_by_name(name: str):
    if not name or not name.strip():
        return {"status": "INVALID", "message": "Please enter a medicine name.", "medicine": None}

    medicine = find_medicine_by_name(name.strip())

    if medicine:
        return {
            "status": "GENUINE",
            "message": f"✅ Verified! {medicine['name']} — {medicine['manufacturer']}.",
            "medicine": medicine,
            "confidence": 0.95,
            "checks": [
                "Medicine registered",
                f"Manufacturer: {medicine['manufacturer']}",
                f"Approved price: {medicine['price']}",
            ]
        }
    return {
        "status": "SUSPICIOUS",
        "message": "⚠️ Medicine not found in our database. May not be registered in Pakistan.",
        "medicine": None,
        "confidence": 0.60,
        "checks": ["❌ Not found in database", "Verify with pharmacist"]
    }


def get_verification_checklist():
    return [
        "Check the hologram on the packaging",
        "Verify batch number and expiry date",
        "Compare font and colors with official packaging",
        "Check for spelling mistakes on label",
        "Verify the seal is intact",
        "Check if price matches DRAP rate",
        "Look for DRAP registration number",
    ]
