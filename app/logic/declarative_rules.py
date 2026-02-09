from typing import List, Tuple, Union

class Condition:
    def __init__(self, predicate: str, object_val: str, truth_value: bool = True):
        self.predicate = predicate
        self.object_val = object_val
        self.truth_value = truth_value

class Rule:
    def __init__(self, name: str, consequence: Tuple[str, str], conditions: List[Condition]):
        self.name = name
        self.consequence = consequence
        self.conditions = conditions

RULES_KB = [
    Rule("norm_dry_cough", ("has_symptom", "cough"), [Condition("has_symptom", "dry_cough")]),
    Rule("norm_prod_cough", ("has_symptom", "cough"), [Condition("has_symptom", "productive_cough")]),
    Rule("norm_high_fever", ("has_symptom", "fever"), [Condition("has_symptom", "high_fever")]),
    Rule("norm_int_fever", ("has_symptom", "fever"), [Condition("has_symptom", "intermittent_fever")]),
    Rule("norm_sev_headache", ("has_symptom", "headache"), [Condition("has_symptom", "severe_headache")]),
    Rule("norm_sev_diarrhea", ("has_symptom", "diarrhea"), [Condition("has_symptom", "severe_diarrhea")]),
    Rule("norm_retro_pain", ("has_symptom", "headache"), [Condition("has_symptom", "retro_orbital_pain")]),

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
        Condition("has_symptom", "fever", False),
        Condition("has_symptom", "shortness_of_breath", False)
    ]),
    
    Rule("diag_covid19", ("possible_diagnosis", "covid19"), [
        Condition("has_symptom", "fever"),
        Condition("has_symptom", "dry_cough"),
        Condition("has_symptom", "loss_of_smell")
    ]),

    Rule("diag_meningitis", ("possible_diagnosis", "meningitis"), [
        Condition("derived_fact", "meningeal_signs"),
        Condition("has_symptom", "high_fever"),
        Condition("has_symptom", "severe_headache")
    ]),

    Rule("diag_malaria_1", ("possible_diagnosis", "malaria"), [
        Condition("has_symptom", "fever"),
        Condition("has_symptom", "chills"),
        Condition("has_symptom", "sweating"),
        Condition("has_symptom", "mosquito_exposure")
    ]),
    Rule("diag_malaria_2", ("possible_diagnosis", "malaria"), [
        Condition("has_symptom", "fever"),
        Condition("has_symptom", "chills"),
        Condition("has_symptom", "sweating"),
        Condition("has_symptom", "intermittent_fever")
    ]),

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

    Rule("diag_food_poisoning", ("possible_diagnosis", "food_poisoning"), [
        Condition("derived_fact", "gastrointestinal_involvement"),
        Condition("has_symptom", "sudden_onset"),
        Condition("has_symptom", "unsafe_food_exposure")
    ]),

    # --- New Diagnoses ---

    Rule("diag_allergies", ("possible_diagnosis", "allergies"), [
        Condition("has_symptom", "sneezing"),
        Condition("has_symptom", "itchy_eyes"),
        Condition("has_symptom", "runny_nose"),
        Condition("has_symptom", "fever", False)  # No fever
    ]),

    Rule("diag_sinusitis", ("possible_diagnosis", "sinusitis"), [
        Condition("has_symptom", "facial_pain"),
        Condition("has_symptom", "headache"),
        Condition("has_symptom", "nasal_congestion"),
        Condition("has_symptom", "fever")
    ]),

    Rule("diag_gerd", ("possible_diagnosis", "gerd"), [
        Condition("has_symptom", "heartburn"),
        Condition("has_symptom", "acid_reflux"),
        Condition("has_symptom", "difficulty_swallowing")
    ]),

    Rule("diag_migraine", ("possible_diagnosis", "migraine"), [
        Condition("has_symptom", "severe_headache"),
        Condition("has_symptom", "nausea"),
        Condition("has_symptom", "sensitivity_light"),
        Condition("has_symptom", "visual_aura")
    ]),

    Rule("diag_tuberculosis", ("possible_diagnosis", "tuberculosis"), [
        Condition("has_symptom", "persistent_cough"),
        Condition("has_symptom", "weight_loss"),
        Condition("has_symptom", "night_sweats"),
        Condition("has_symptom", "fever")
    ]),

    Rule("diag_chickenpox", ("possible_diagnosis", "chickenpox"), [
        Condition("has_symptom", "itchy_rash"),
        Condition("has_symptom", "fever"),
        Condition("has_symptom", "fatigue")
    ]),

    Rule("diag_measles", ("possible_diagnosis", "measles"), [
        Condition("has_symptom", "high_fever"),
        Condition("has_symptom", "cough"),
        Condition("has_symptom", "runny_nose"),
        Condition("has_symptom", "rash")
    ]),

    Rule("diag_strep_throat", ("possible_diagnosis", "strep_throat"), [
        Condition("has_symptom", "sore_throat"),
        Condition("has_symptom", "fever"),
        Condition("has_symptom", "swollen_nodes"),
        Condition("has_symptom", "cough", False)  # Usually no cough
    ])
]
