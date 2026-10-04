"""
MediScan AI - Symptom Suggester (Text input, no dropdown)
"""
from database import find_symptom, find_medicine_by_name


def suggest_medicines(symptom_text: str, age_group: str = "Adult"):
    """Suggest OTC medicines based on symptoms."""
    if not symptom_text or not symptom_text.strip():
        return {"found": False, "message": "Please enter your symptoms."}

    text_lower = symptom_text.lower().strip()

    # Split by comma to allow multiple symptoms
    parts = [p.strip() for p in text_lower.split(",")]
    matched_symptoms = []
    seen = set()

    for part in parts:
        for key, val in __import__("database").SYMPTOMS.items():
            if (key in part or part in key) and key not in seen:
                matched_symptoms.append((key, val))
                seen.add(key)
                break

    if not matched_symptoms:
        return {
            "found": False,
            "message": "No matching symptoms found. Try: fever, headache, cough, cold, heartburn, stomach pain, back pain, etc."
        }

    results = []
    for symptom_name, data in matched_symptoms:
        medicines_info = []
        for med_name in data["otc"]:
            med = find_medicine_by_name(med_name)
            if med:
                if age_group == "Child (0-12)" and med["name"] not in ["Calpol", "Panadol"]:
                    continue
                medicines_info.append({
                    "name": med["name"],
                    "generic": med["generic"],
                    "dosage": med["dosage"],
                    "price": med["price"],
                })

        results.append({
            "symptom": symptom_name,
            "medicines": medicines_info,
            "warnings": data["warnings"],
            "red_flags": data["red_flags"],
        })

    return {"found": True, "results": results}
