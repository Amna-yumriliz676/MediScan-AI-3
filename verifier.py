"""
MediScan AI - Medicine Verifier (Image-based only)
"""
from database import MEDICINES


def verify_by_image_match(detected_medicines: list):
    """
    Given medicines detected from image, check if they're in our verified database.
    Returns per-medicine verification.
    """
    if not detected_medicines:
        return {
            "status": "UNKNOWN",
            "message": "Could not detect any medicine from image.",
            "results": [],
            "has_fake": False,
        }

    results = []
    has_fake = False

    for m in detected_medicines:
        med_name = m["medicine"]
        # Find in database
        found = None
        for db_med in MEDICINES:
            if db_med["name"].lower() == med_name.lower():
                found = db_med
                break

        if found:
            results.append({
                "medicine": found["name"],
                "status": "GENUINE",
                "manufacturer": found["manufacturer"],
                "barcode": found["barcode"],
                "price": found["price"],
                "category": found["category"],
                "dosage": found["dosage"],
                "confidence": m["confidence"],
            })
        else:
            has_fake = True
            results.append({
                "medicine": med_name,
                "status": "SUSPICIOUS",
                "manufacturer": "Unknown",
                "barcode": "-",
                "price": "-",
                "category": "-",
                "dosage": "-",
                "confidence": m["confidence"],
            })

    return {
        "status": "COMPLETE",
        "results": results,
        "has_fake": has_fake,
    }


def get_verification_checklist():
    """Professional visual verification checklist."""
    return [
        {
            "title": "Hologram Check",
            "desc": "Look for the holographic seal on the packaging — should shift colors when tilted"
        },
        {
            "title": "Batch & Expiry",
            "desc": "Both should be clearly printed (not stickers). Check if not expired"
        },
        {
            "title": "Font Consistency",
            "desc": "Compare font style with manufacturer's official packaging"
        },
        {
            "title": "Spelling Check",
            "desc": "Misspelled brand names are a common sign of fakes"
        },
        {
            "title": "Seal Integrity",
            "desc": "The medicine seal should be intact, not tampered with"
        },
        {
            "title": "Price Verification",
            "desc": "If price is far below DRAP rate, it may be fake"
        },
        {
            "title": "DRAP Registration",
            "desc": "Look for a valid DRAP registration number on the pack"
        },
    ]
