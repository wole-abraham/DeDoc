import asyncio
from app.logic.facts import Facts
from app.logic.inference import Inference

def test_strict_logic():
    print("--- Starting Strict FOL Verification ---")
    
    facts_db = Facts()
    engine = Inference()
    
    test_cases = [
        ("Patient_Flu", ["fever", "cough", "fatigue"], "flu"),
        ("Patient_Cold", ["cough"], "common_cold"),
        ("Patient_Malaria", ["fever", "chills", "sweating"], "malaria"),
        ("Patient_Typhoid", ["fever", "headache", "fatigue"], "typhoid"),
        ("Patient_Dengue", ["fever", "headache", "body_pain"], "dengue"),
        ("Patient_Healthy", ["fatigue"], None),
        ("Patient_Confused", ["fever", "cough"], None)
    ]
    
    print(f"Testing {len(test_cases)} scenarios...")
    
    passed = 0
    
    for name, symptoms, expected in test_cases:
        for s in symptoms:
            facts_db.add_fact("has_symptom", name, s)
    
    results = engine.infer(facts_db)
    
    for name, symptoms, expected in test_cases:
        has_diagnosis = ("diagnosis", name, expected) in results
        
        if expected is None:
            any_rel = any(d[1] == name and d[0] == "diagnosis" for d in results)
            if not any_rel:
                print(f"[PASS] {name}: Correctly diagnosed with Nothing.")
                passed += 1
            else:
                found = [d[2] for d in results if d[1] == name]
                print(f"[FAIL] {name}: Expected Nothing, got {found}")
        else:
            if has_diagnosis:
                print(f"[PASS] {name}: Correctly diagnosed with {expected}.")
                passed += 1
            else:
                print(f"[FAIL] {name}: Expected {expected}, but it was not found.")
                
    print(f"\n--- Verification Complete ({passed}/{len(test_cases)}) ---")

if __name__ == "__main__":
    test_strict_logic()
