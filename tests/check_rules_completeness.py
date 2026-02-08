import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.logic.inference import Inference
from app.logic.facts import Facts

def run_tests():
    inference_engine = Inference()
    
    test_cases = [
        {
            "id": "TC-01",
            "disease": "Influenza",
            "symptoms": ["fever", "cough", "sudden_onset", "muscle_pain", "fatigue"],
            "expected_diagnosis": "influenza"
        },
        {
            "id": "TC-02",
            "disease": "Pneumonia",
            "symptoms": ["high_fever", "shortness_of_breath", "chest_pain", "cough"],
            "expected_diagnosis": "pneumonia"
        },
        {
            "id": "TC-03",
            "disease": "COVID-19",
            "symptoms": ["fever", "dry_cough", "loss_of_smell"],
            "expected_diagnosis": "covid19" 
        },
        {
            "id": "TC-04",
            "disease": "Malaria",
            "symptoms": ["fever", "chills", "sweating", "mosquito_exposure"],
            "expected_diagnosis": "malaria"
        },
        {
            "id": "TC-05",
            "disease": "Dengue",
            "symptoms": ["fever", "mosquito_exposure", "severe_headache", "joint_pain"],
            "expected_diagnosis": "dengue"
        },
        {
            "id": "TC-06",
            "disease": "Food Poisoning",
            "symptoms": ["vomiting", "sudden_onset", "unsafe_food_exposure"], 
            "expected_diagnosis": "food_poisoning"
        },
        {
            "id": "TC-07",
            "disease": "Meningitis",
            "symptoms": ["stiff_neck", "sensitivity_light", "high_fever", "severe_headache"],
            "expected_diagnosis": "meningitis"
        }
    ]

    all_passed = True
    print("Running Logic Verification Tests (Appendix C)...")
    print("-" * 60)

    for case in test_cases:
        facts = Facts()
        for symptom in case["symptoms"]:
            facts.add_fact("has_symptom", "current_patient", symptom)
        
        results = inference_engine.infer(facts)
        
        diagnoses = [diagnosis for pred, subj, diagnosis in results if pred == "possible_diagnosis"]
        
        passed = case["expected_diagnosis"] in diagnoses
        
        status = "PASSED" if passed else "FAILED"
        if not passed:
            all_passed = False
            print(f"{case['id']} ({case['disease']}): {status}")
            print(f"  Inputs: {case['symptoms']}")
            print(f"  Expected: {case['expected_diagnosis']}")
            print(f"  Actual: {diagnoses}")
        else:
             print(f"{case['id']} ({case['disease']}): {status}")

    print("-" * 60)
    if all_passed:
        print("All test cases passed! Logic is complete and correct.")
    else:
        print("Some test cases failed.")

if __name__ == "__main__":
    run_tests()
