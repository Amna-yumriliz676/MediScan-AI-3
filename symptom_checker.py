"""
MediScan AI - Symptom to OTC Medicine Suggester
"""
from database import SYMPTOMS, find_symptom, find_medicine_by_name


def suggest_medicines(symptom_text: str, age_group: str = "Adult"):
    """Suggest OTC medicines based on symptoms."""
    if not symptom_text or not symptom_text.strip():
        return {"found": False, "message": "Please enter your symptoms."}

    matched_symptoms = []
    text_lower = symptom_text.lower()

    for key, val in SYMPTOMS.items():
        if key in text_lower:
            matched_symptoms.append((key, val))

    if not matched_symptoms:
        return {
            "found": False,
            "message": "No matching symptoms found. Try: fever, headache, cough, cold, heartburn, etc."
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
