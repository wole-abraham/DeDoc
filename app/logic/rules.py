class Rules:
    @staticmethod
    def normalize_symptoms(facts_db):
        implications = {
            "dry_cough": "cough",
            "productive_cough": "cough",
            "high_fever": "fever",
            "intermittent_fever": "fever",
            "severe_headache": "headache",
            "severe_diarrhea": "diarrhea",
            "retro_orbital_pain": "headache"
        }

        for specific, general in implications.items():
            candidates = facts_db.query(predicate="has_symptom", object_val=specific)
            for _, patient, _ in candidates:
                yield ("has_symptom", patient, general)

    @staticmethod
    def derive_clinical_states(facts_db):
        for _, patient, _ in facts_db.query("has_symptom", object_val="sudden_onset"):
            yield ("derived_fact", patient, "acute_condition")

        for _, patient, _ in facts_db.query("has_symptom", object_val="fever"):
            if facts_db.exists("has_symptom", patient, "fatigue"):
                yield ("derived_fact", patient, "systemic_illness")

        cough_cases = facts_db.query("has_symptom", object_val="cough")
        sob_cases = facts_db.query("has_symptom", object_val="shortness_of_breath")
        
        all_resp = set([c[1] for c in cough_cases] + [c[1] for c in sob_cases])
        for patient in all_resp:
            yield ("derived_fact", patient, "respiratory_involvement")

        for _, patient, _ in facts_db.query("has_symptom", object_val="stiff_neck"):
            if facts_db.exists("has_symptom", patient, "sensitivity_light"):
                yield ("derived_fact", patient, "meningeal_signs")

        vomit = facts_db.query("has_symptom", object_val="vomiting")
        diarrhea = facts_db.query("has_symptom", object_val="diarrhea")
        all_gi = set([c[1] for c in vomit] + [c[1] for c in diarrhea])
        for patient in all_gi:
            yield ("derived_fact", patient, "gastrointestinal_involvement")

    @staticmethod
    def diagnose_flu(facts_db):
        candidates = facts_db.query("derived_fact", object_val="systemic_illness")
        for _, patient, _ in candidates:
            if (facts_db.exists("derived_fact", patient, "respiratory_involvement") and
                facts_db.exists("derived_fact", patient, "acute_condition") and
                facts_db.exists("has_symptom", patient, "muscle_pain")):
                yield ("possible_diagnosis", patient, "influenza")

    @staticmethod
    def diagnose_pneumonia(facts_db):
        candidates = facts_db.query("derived_fact", object_val="respiratory_involvement")
        for _, patient, _ in candidates:
            if (facts_db.exists("has_symptom", patient, "high_fever") and
                facts_db.exists("has_symptom", patient, "shortness_of_breath") and
                facts_db.exists("has_symptom", patient, "chest_pain")):
                yield ("possible_diagnosis", patient, "pneumonia")

    @staticmethod
    def diagnose_common_cold(facts_db):
        candidates = facts_db.query("derived_fact", object_val="respiratory_involvement")
        for _, patient, _ in candidates:
            if (facts_db.exists("has_symptom", patient, "gradual_onset") and
                not facts_db.exists("has_symptom", patient, "fever") and
                not facts_db.exists("has_symptom", patient, "shortness_of_breath")):
                yield ("possible_diagnosis", patient, "common_cold")
    
    @staticmethod
    def diagnose_meningitis(facts_db):
        candidates = facts_db.query("derived_fact", object_val="meningeal_signs")
        for _, patient, _ in candidates:
            if (facts_db.exists("has_symptom", patient, "high_fever") and
                facts_db.exists("has_symptom", patient, "severe_headache")):
                yield ("possible_diagnosis", patient, "meningitis")

    @staticmethod
    def diagnose_malaria(facts_db):
        candidates = facts_db.query("has_symptom", object_val="fever")
        for _, patient, _ in candidates:
            if (facts_db.exists("has_symptom", patient, "chills") and
                facts_db.exists("has_symptom", patient, "sweating") and
                (facts_db.exists("has_symptom", patient, "mosquito_exposure") or 
                 facts_db.exists("has_symptom", patient, "intermittent_fever"))):
                yield ("possible_diagnosis", patient, "malaria")

    @staticmethod
    def diagnose_dengue(facts_db):
        candidates = facts_db.query("has_symptom", object_val="fever")
        for _, patient, _ in candidates:
            if (facts_db.exists("has_symptom", patient, "mosquito_exposure") and
                facts_db.exists("has_symptom", patient, "severe_headache") and
                (facts_db.exists("has_symptom", patient, "retro_orbital_pain") or 
                 facts_db.exists("has_symptom", patient, "joint_pain"))):
                yield ("possible_diagnosis", patient, "dengue")

    @staticmethod
    def diagnose_food_poisoning(facts_db):
        candidates = facts_db.query("derived_fact", object_val="gastrointestinal_involvement")
        for _, patient, _ in candidates:
            if (facts_db.exists("has_symptom", patient, "sudden_onset") and
                facts_db.exists("has_symptom", patient, "unsafe_food_exposure")):
                yield ("possible_diagnosis", patient, "food_poisoning")