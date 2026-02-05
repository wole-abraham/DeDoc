
from app.logic.facts import Facts
from app.logic.inference import Inference

def check_case():
    print("--- Checking User Case ---")
    facts = Facts()
    engine = Inference()
    
    # User reports
    symptoms = [
        "fever",
        "intermittent_fever",
        "sweating",
        "headache",
        "fatigue",
        "gradual_onset"
    ]
    
    patient = "User"
    for s in symptoms:
        facts.add_fact("has_symptom", patient, s)
        
    print(f"Symptoms: {symptoms}")
    
    dataset = engine.infer(facts)
    diagnoses = [d[2] for d in dataset if d[0] == "diagnosis"]
    
    if diagnoses:
        print(f"Diagnosis Found: {diagnoses}")
    else:
        print("No Diagnosis Found.")

if __name__ == "__main__":
    check_case()
