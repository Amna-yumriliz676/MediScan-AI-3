"""
MediScan AI - Medicines & Symptoms data
Drug interactions removed.
"""

MEDICINES = [
    {"name": "Panadol", "generic": "Paracetamol",
     "uses": "Fever, headache, body ache", "dosage": "500mg every 6 hours",
     "side_effects": "Nausea, liver damage (overdose)", "category": "Analgesic",
     "manufacturer": "GSK Pakistan", "barcode": "8901234567890", "otc": True,
     "price": "Rs. 45"},
    {"name": "Brufen", "generic": "Ibuprofen",
     "uses": "Pain, inflammation, fever", "dosage": "400mg every 8 hours after food",
     "side_effects": "Stomach upset, ulcers", "category": "NSAID",
     "manufacturer": "Abbott Pakistan", "barcode": "8901234567891", "otc": True,
     "price": "Rs. 85"},
    {"name": "Augmentin", "generic": "Amoxicillin + Clavulanic Acid",
     "uses": "Bacterial infections", "dosage": "625mg every 12 hours",
     "side_effects": "Diarrhea, nausea, rash", "category": "Antibiotic",
     "manufacturer": "GSK Pakistan", "barcode": "8901234567892", "otc": False,
     "price": "Rs. 350"},
    {"name": "Glucophage", "generic": "Metformin",
     "uses": "Type 2 diabetes", "dosage": "500mg twice daily",
     "side_effects": "Nausea, B12 deficiency", "category": "Antidiabetic",
     "manufacturer": "Merck Pakistan", "barcode": "8901234567893", "otc": False,
     "price": "Rs. 180"},
    {"name": "Concor", "generic": "Bisoprolol",
     "uses": "High blood pressure", "dosage": "5mg once daily",
     "side_effects": "Fatigue, slow heart rate", "category": "Beta Blocker",
     "manufacturer": "Merck Pakistan", "barcode": "8901234567894", "otc": False,
     "price": "Rs. 220"},
    {"name": "Lipitor", "generic": "Atorvastatin",
     "uses": "High cholesterol", "dosage": "10-80mg once daily at night",
     "side_effects": "Muscle pain, liver issues", "category": "Statin",
     "manufacturer": "Pfizer Pakistan", "barcode": "8901234567895", "otc": False,
     "price": "Rs. 420"},
    {"name": "Warf", "generic": "Warfarin",
     "uses": "Blood thinning", "dosage": "Varies (INR-based)",
     "side_effects": "Bleeding, bruising", "category": "Anticoagulant",
     "manufacturer": "Getz Pharma", "barcode": "8901234567896", "otc": False,
     "price": "Rs. 150"},
    {"name": "Zoloft", "generic": "Sertraline",
     "uses": "Depression, anxiety", "dosage": "50-200mg once daily",
     "side_effects": "Nausea, insomnia", "category": "Antidepressant",
     "manufacturer": "Pfizer Pakistan", "barcode": "8901234567897", "otc": False,
     "price": "Rs. 480"},
    {"name": "Ventolin", "generic": "Salbutamol",
     "uses": "Asthma, COPD", "dosage": "100-200mcg inhaler as needed",
     "side_effects": "Tremor, palpitations", "category": "Bronchodilator",
     "manufacturer": "GSK Pakistan", "barcode": "8901234567898", "otc": False,
     "price": "Rs. 320"},
    {"name": "Risek", "generic": "Omeprazole",
     "uses": "Acid reflux, heartburn", "dosage": "20-40mg once daily",
     "side_effects": "Headache, B12 deficiency", "category": "PPI",
     "manufacturer": "Getz Pharma", "barcode": "8901234567899", "otc": True,
     "price": "Rs. 140"},
    {"name": "Calpol", "generic": "Paracetamol (Syrup)",
     "uses": "Fever in children", "dosage": "10-15mg/kg every 6 hours",
     "side_effects": "Nausea (overdose)", "category": "Pediatric",
     "manufacturer": "GSK Pakistan", "barcode": "8901234567800", "otc": True,
     "price": "Rs. 95"},
    {"name": "Ponstan", "generic": "Mefenamic Acid",
     "uses": "Pain, menstrual cramps", "dosage": "250-500mg three times daily",
     "side_effects": "Stomach upset, headache", "category": "NSAID",
     "manufacturer": "Pfizer Pakistan", "barcode": "8901234567801", "otc": True,
     "price": "Rs. 110"},
]


# ============================================================
# SYMPTOMS → OTC MEDICINES (dropdown removed — but data remains)
# ============================================================
SYMPTOMS = {
    "fever": {
        "otc": ["Panadol"],
        "warnings": ["Fever > 3 days → See doctor", "Fever > 103°F → Emergency"],
        "red_flags": ["Rash + fever", "Stiff neck + fever", "Confusion"],
    },
    "headache": {
        "otc": ["Panadol", "Brufen"],
        "warnings": ["Don't take both together", "Max 3 days continuous"],
        "red_flags": ["Sudden severe headache", "With vision changes"],
    },
    "body ache": {
        "otc": ["Panadol", "Brufen"],
        "warnings": ["Take after food (Brufen)", "Don't combine"],
        "red_flags": ["With rash", "With high fever", "Muscle weakness"],
    },
    "cough": {
        "otc": ["Calpol (kids)"],
        "warnings": ["Kids: consult pediatrician", "Adults: see doctor if > 2 weeks"],
        "red_flags": ["Blood in cough", "Breathing difficulty", "Chest pain"],
    },
    "cold": {
        "otc": ["Panadol"],
        "warnings": ["Rest + hydration", "See doctor if > 1 week"],
        "red_flags": ["High fever", "Ear pain", "Severe sore throat"],
    },
    "heartburn": {
        "otc": ["Risek"],
        "warnings": ["Take before meal", "See doctor if > 2 weeks"],
        "red_flags": ["Chest pain", "Difficulty swallowing"],
    },
    "menstrual cramps": {
        "otc": ["Ponstan", "Brufen"],
        "warnings": ["Take after food", "Don't take both"],
        "red_flags": ["Severe pain > 2 days", "Heavy bleeding"],
    },
    "diarrhea": {
        "otc": [],
        "warnings": ["ORS + hydration", "See doctor if > 2 days"],
        "red_flags": ["Blood in stool", "Severe dehydration"],
    },
    "allergy": {
        "otc": [],
        "warnings": ["Consult doctor for antihistamine"],
        "red_flags": ["Breathing difficulty", "Swelling"],
    },
    "sore throat": {
        "otc": ["Panadol"],
        "warnings": ["Warm water gargle", "See doctor if > 3 days"],
        "red_flags": ["Difficulty swallowing", "High fever"],
    },
    "vomiting": {
        "otc": [],
        "warnings": ["ORS + hydration", "See doctor if > 24 hours"],
        "red_flags": ["Blood in vomit", "Severe dehydration"],
    },
    "stomach pain": {
        "otc": ["Risek"],
        "warnings": ["Avoid spicy food", "See doctor if > 2 days"],
        "red_flags": ["Severe pain", "Blood in stool", "Fever"],
    },
    "back pain": {
        "otc": ["Panadol", "Brufen"],
        "warnings": ["Rest + hot compress", "See doctor if > 1 week"],
        "red_flags": ["Numbness in legs", "Loss of bladder control"],
    },
    "insomnia": {
        "otc": [],
        "warnings": ["Consult doctor", "Avoid caffeine after 4 PM"],
        "red_flags": ["Persistent > 2 weeks", "With depression"],
    },
    "anxiety": {
        "otc": [],
        "warnings": ["Consult doctor", "Deep breathing exercises"],
        "red_flags": ["Panic attacks", "Suicidal thoughts"],
    },
}


def search_medicine(query: str):
    query = query.lower().strip()
    return [
        m for m in MEDICINES
        if (query in m["name"].lower()
            or query in m["generic"].lower()
            or query in m["uses"].lower()
            or query in m["category"].lower())
    ]


def find_medicine_by_name(name: str):
    name = name.lower().strip()
    for m in MEDICINES:
        if m["name"].lower() == name or m["generic"].lower() == name:
            return m
    return None


def find_medicine_by_barcode(barcode: str):
    barcode = barcode.strip()
    for m in MEDICINES:
        if m["barcode"] == barcode:
            return m
    return None


def get_all_medicine_names():
    return [m["name"] for m in MEDICINES]


def get_otc_medicines():
    return [m for m in MEDICINES if m["otc"]]


def find_symptom(symptom_text: str):
    symptom_text = symptom_text.lower().strip()
    for key, val in SYMPTOMS.items():
        if key in symptom_text or symptom_text in key:
            return key, val
    return None, None
