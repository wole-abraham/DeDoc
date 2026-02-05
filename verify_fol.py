import asyncio
from app.logic.facts import Facts
from app.logic.inference import Inference

async def test_fol_logic():
    print("--- Starting FOL Verification (Chaining & Expanded Diagnoses) ---")
    
    facts_base = Facts()
    inference_engine = Inference()
    
    # CASE 1: Chain Logic Check - Dengue with Warning
    print("\nCase 1: Dengue + Warning Test")
    p1 = "Patient_Warning"
    facts_base.add_fact("has_symptom", p1, "fever")
    facts_base.add_fact("has_symptom", p1, "severe_headache")
    facts_base.add_fact("has_symptom", p1, "retro_orbital_pain")
    facts_base.add_fact("has_symptom", p1, "mosquito_exposure")
    facts_base.add_fact("has_symptom", p1, "abdominal_pain") # Trigger warning
    
    # CASE 2: New Diagnosis - Meningitis
    print("Case 2: Meningitis Test")
    p2 = "Patient_Meningitis"
    facts_base.add_fact("has_symptom", p2, "high_fever")
    facts_base.add_fact("has_symptom", p2, "severe_headache")
    facts_base.add_fact("has_symptom", p2, "stiff_neck")
    facts_base.add_fact("has_symptom", p2, "sensitivity_light")
    
    # CASE 3: New Diagnosis - Pneumonia w/ Sepsis Risk
    print("Case 3: Pneumonia + Sepsis Risk Test")
    p3 = "Patient_Pneumonia"
    facts_base.add_fact("has_symptom", p3, "high_fever")
    facts_base.add_fact("has_symptom", p3, "cough")
    facts_base.add_fact("has_symptom", p3, "shortness_of_breath")
    facts_base.add_fact("has_symptom", p3, "chest_pain")
    facts_base.add_fact("has_symptom", p3, "severe_fatigue") # Trigger Sepsis Risk

    print("\nRunning Iterative Inference...")
    results = inference_engine.infer(facts_base)
    
    print(f"All Inferred Facts: {results}")
    
    # Verify Checks
    dengue_found = ("diagnosis", p1, "dengue") in results
    warning_found = ("warning", p1, "dengue_hemorrhagic_risk") in results
    meningitis_found = ("diagnosis", p2, "meningitis") in results
    pneumonia_found = ("diagnosis", p3, "pneumonia") in results
    sepsis_found = ("risk", p3, "sepsis_alert") in results
    
    if (dengue_found and warning_found and meningitis_found and pneumonia_found and sepsis_found):
        print("\nSUCCESS: All complex diagnoses and CHAINED warnings verified!")
    else:
        print("\nFAILURE: Missing expected inferences.")
        print(f"Dengue: {dengue_found}, Warning: {warning_found}")
        print(f"Meningitis: {meningitis_found}")
        print(f"Pneumonia: {pneumonia_found}, Sepsis: {sepsis_found}")

if __name__ == "__main__":
    asyncio.run(test_fol_logic())
