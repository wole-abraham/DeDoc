from typing import List, Tuple, Union

class Condition:
    def __init__(self, predicate: str, object_val: str, truth_value: bool = True):
        self.predicate = predicate
        self.object_val = object_val
        self.truth_value = truth_value # True = MUST HAVE, False = MUST NOT HAVE

class Rule:
    def __init__(self, name: str, consequence: Tuple[str, str], conditions: List[Condition]):
        self.name = name
        self.consequence = consequence # (predicate, object_val)
        self.conditions = conditions

# Knowledge Base Definitions
RULES_KB = [
    # --- Normalization (Implicit) ---
    # These effectively are "If dry_cough -> cough". 
    # We'll treat them as facts derivation.
    Rule("norm_dry_cough", ("has_symptom", "cough"), [Condition("has_symptom", "dry_cough")]),
    Rule("norm_prod_cough", ("has_symptom", "cough"), [Condition("has_symptom", "productive_cough")]),
    Rule("norm_high_fever", ("has_symptom", "fever"), [Condition("has_symptom", "high_fever")]),
    Rule("norm_int_fever", ("has_symptom", "fever"), [Condition("has_symptom", "intermittent_fever")]),
    Rule("norm_sev_headache", ("has_symptom", "headache"), [Condition("has_symptom", "severe_headache")]),
    Rule("norm_sev_diarrhea", ("has_symptom", "diarrhea"), [Condition("has_symptom", "severe_diarrhea")]),
    Rule("norm_retro_pain", ("has_symptom", "headache"), [Condition("has_symptom", "retro_orbital_pain")]),

    # --- Derived Facts ---
    Rule("derive_acute", ("derived_fact", "acute_condition"), [Condition("has_symptom", "sudden_onset")]),
    Rule("derive_systemic", ("derived_fact", "systemic_illness"), [
        Condition("has_symptom", "fever"),
        Condition("has_symptom", "fatigue")
    ]),
    Rule("derive_resp_cough", ("derived_fact", "respiratory_involvement"), [Condition("has_symptom", "cough")]),
    Rule("derive_resp_sob", ("derived_fact", "respiratory_involvement"), [Condition("has_symptom", "shortness_of_breath")]),
    
    Rule("derive_meningeal", ("derived_fact", "meningeal_signs"), [
        Condition("has_symptom", "stiff_neck"),
        Condition("has_symptom", "sensitivity_light")
    ]),
    
    Rule("derive_gi_vomit", ("derived_fact", "gastrointestinal_involvement"), [Condition("has_symptom", "vomiting")]),
    Rule("derive_gi_diarrhea", ("derived_fact", "gastrointestinal_involvement"), [Condition("has_symptom", "diarrhea")]),

    # --- Diagnoses: Respiratory ---
    Rule("diag_flu", ("possible_diagnosis", "influenza"), [
        Condition("derived_fact", "systemic_illness"),
        Condition("derived_fact", "respiratory_involvement"),
        Condition("derived_fact", "acute_condition"),
        Condition("has_symptom", "muscle_pain")
    ]),
    
    Rule("diag_pneumonia", ("possible_diagnosis", "pneumonia"), [
        Condition("derived_fact", "respiratory_involvement"),
        Condition("has_symptom", "high_fever"),
        Condition("has_symptom", "shortness_of_breath"),
        Condition("has_symptom", "chest_pain")
    ]),

    Rule("diag_common_cold", ("possible_diagnosis", "common_cold"), [
        Condition("derived_fact", "respiratory_involvement"),
        Condition("has_symptom", "gradual_onset"),
        Condition("has_symptom", "fever", False), # NOT fever
        Condition("has_symptom", "shortness_of_breath", False) # NOT sob
    ]),
    
    Rule("diag_covid19", ("possible_diagnosis", "covid19"), [
        # Classic triad
        Condition("has_symptom", "fever"),
        Condition("has_symptom", "dry_cough"),
        Condition("has_symptom", "loss_of_smell")
    ]),

    Rule("diag_meningitis", ("possible_diagnosis", "meningitis"), [
        Condition("derived_fact", "meningeal_signs"),
        Condition("has_symptom", "high_fever"),
        Condition("has_symptom", "severe_headache")
    ]),

    # --- Vector Borne ---
    # Malaria (Split for OR condition)
    # 1. Mosquito path
    Rule("diag_malaria_1", ("possible_diagnosis", "malaria"), [
        Condition("has_symptom", "fever"),
        Condition("has_symptom", "chills"),
        Condition("has_symptom", "sweating"),
        Condition("has_symptom", "mosquito_exposure")
    ]),
    # 2. Intermittent path
    Rule("diag_malaria_2", ("possible_diagnosis", "malaria"), [
        Condition("has_symptom", "fever"),
        Condition("has_symptom", "chills"),
        Condition("has_symptom", "sweating"),
        Condition("has_symptom", "intermittent_fever")
    ]),

    # Dengue (Split for OR)
    Rule("diag_dengue_1", ("possible_diagnosis", "dengue"), [
        Condition("has_symptom", "fever"),
        Condition("has_symptom", "mosquito_exposure"),
        Condition("has_symptom", "severe_headache"),
        Condition("has_symptom", "retro_orbital_pain")
    ]),
    Rule("diag_dengue_2", ("possible_diagnosis", "dengue"), [
        Condition("has_symptom", "fever"),
        Condition("has_symptom", "mosquito_exposure"),
        Condition("has_symptom", "severe_headache"),
        Condition("has_symptom", "joint_pain")
    ]),

    # --- GI ---
    Rule("diag_food_poisoning", ("possible_diagnosis", "food_poisoning"), [
        Condition("derived_fact", "gastrointestinal_involvement"),
        Condition("has_symptom", "sudden_onset"),
        Condition("has_symptom", "unsafe_food_exposure")
    ])
]
