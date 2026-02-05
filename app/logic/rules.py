class Rules:
    """
    First-Order Logic Rules for Disease Inference.
    Domain: Medical Diagnosis
    Approach: Forward Chaining
    """

    # =========================================
    # LAYER 1: NORMALIZATION (Implication Rules)
    # =========================================
    @staticmethod
    def normalize_symptoms(facts_db):
        """
        Infers implicit base symptoms from specific qualifiers.
        ∀x (HasSymptom(x, dry_cough) → HasSymptom(x, cough))
        """
        # Map specific -> general
        implications = {
            "dry_cough": "cough",
            "productive_cough": "cough",
            "high_fever": "fever",
            "intermittent_fever": "fever",
            "severe_headache": "headache",
            "severe_diarrhea": "diarrhea",
            "retro_orbital_pain": "headache" # Medical ontology choice
        }

        # Scan for qualifiers
        for specific, general in implications.items():
            candidates = facts_db.query(predicate="has_symptom", object_val=specific)
            for _, patient, _ in candidates:
                yield ("has_symptom", patient, general)

    # =========================================
    # LAYER 2: ABSTRACTION (Derived Facts)
    # =========================================
    @staticmethod
    def derive_clinical_states(facts_db):
        """
        Infers higher-level clinical concepts from symptom clusters.
        """
        # Acute Condition: Sudden Onset
        for _, patient, _ in facts_db.query("has_symptom", object_val="sudden_onset"):
            yield ("derived_fact", patient, "acute_condition")

        # Systemic Illness: Fever + Fatigue (simplified)
        for _, patient, _ in facts_db.query("has_symptom", object_val="fever"):
            if facts_db.exists("has_symptom", patient, "fatigue"):
                yield ("derived_fact", patient, "systemic_illness")

        # Respiratory Involvement: Cough OR Difficulty Breathing
        cough_cases = facts_db.query("has_symptom", object_val="cough")
        sob_cases = facts_db.query("has_symptom", object_val="shortness_of_breath")
        
        all_resp = set([c[1] for c in cough_cases] + [c[1] for c in sob_cases])
        for patient in all_resp:
            yield ("derived_fact", patient, "respiratory_involvement")

        # Meningeal Signs: Stiff Neck + Light Sensitivity
        for _, patient, _ in facts_db.query("has_symptom", object_val="stiff_neck"):
            if facts_db.exists("has_symptom", patient, "sensitivity_light"):
                yield ("derived_fact", patient, "meningeal_signs")

        # GI Involvement: Vomiting OR Diarrhea
        vomit = facts_db.query("has_symptom", object_val="vomiting")
        diarrhea = facts_db.query("has_symptom", object_val="diarrhea")
        all_gi = set([c[1] for c in vomit] + [c[1] for c in diarrhea])
        for patient in all_gi:
            yield ("derived_fact", patient, "gastrointestinal_involvement")

    # =========================================
    # LAYER 3: DIAGNOSIS (Suggestion Rules)
    # =========================================
    
    # --- Respiratory ---
    @staticmethod
    def diagnose_flu(facts_db):
        # Systemic Illness + Acute + Respiratory + Muscle Pain
        candidates = facts_db.query("derived_fact", object_val="systemic_illness")
        for _, patient, _ in candidates:
            if (facts_db.exists("derived_fact", patient, "respiratory_involvement") and
                facts_db.exists("derived_fact", patient, "acute_condition") and
                facts_db.exists("has_symptom", patient, "muscle_pain")):
                yield ("possible_diagnosis", patient, "influenza")

    @staticmethod
    def diagnose_pneumonia(facts_db):
        # Respiratory Involvement + High Fever + Breathlessness + Chest Pain
        candidates = facts_db.query("derived_fact", object_val="respiratory_involvement")
        for _, patient, _ in candidates:
            if (facts_db.exists("has_symptom", patient, "high_fever") and
                facts_db.exists("has_symptom", patient, "shortness_of_breath") and
                facts_db.exists("has_symptom", patient, "chest_pain")):
                yield ("possible_diagnosis", patient, "pneumonia")

    @staticmethod
    def diagnose_common_cold(facts_db):
        # Respiratory + Gradual - Fever - Breathlessness
        candidates = facts_db.query("derived_fact", object_val="respiratory_involvement")
        for _, patient, _ in candidates:
            if (facts_db.exists("has_symptom", patient, "gradual_onset") and
                not facts_db.exists("has_symptom", patient, "fever") and
                not facts_db.exists("has_symptom", patient, "shortness_of_breath")):
                yield ("possible_diagnosis", patient, "common_cold")
    
    @staticmethod
    def diagnose_meningitis(facts_db):
        # Meningeal Signs + High Fever + Severe Headache
        candidates = facts_db.query("derived_fact", object_val="meningeal_signs")
        for _, patient, _ in candidates:
            if (facts_db.exists("has_symptom", patient, "high_fever") and
                facts_db.exists("has_symptom", patient, "severe_headache")):
                yield ("possible_diagnosis", patient, "meningitis")

    # --- Vector Borne ---
    @staticmethod
    def diagnose_malaria(facts_db):
        # Fever + Chills + Sweating + Context
        candidates = facts_db.query("has_symptom", object_val="fever")
        for _, patient, _ in candidates:
            if (facts_db.exists("has_symptom", patient, "chills") and
                facts_db.exists("has_symptom", patient, "sweating") and
                (facts_db.exists("has_symptom", patient, "mosquito_exposure") or 
                 facts_db.exists("has_symptom", patient, "intermittent_fever"))):
                yield ("possible_diagnosis", patient, "malaria")

    @staticmethod
    def diagnose_dengue(facts_db):
        # Fever + Mosquito + Severe Headache + (RetroOrbital OR JointPain)
        candidates = facts_db.query("has_symptom", object_val="fever")
        for _, patient, _ in candidates:
            if (facts_db.exists("has_symptom", patient, "mosquito_exposure") and
                facts_db.exists("has_symptom", patient, "severe_headache") and
                (facts_db.exists("has_symptom", patient, "retro_orbital_pain") or 
                 facts_db.exists("has_symptom", patient, "joint_pain"))):
                yield ("possible_diagnosis", patient, "dengue")

    # --- GI ---
    @staticmethod
    def diagnose_food_poisoning(facts_db):
        # GI Involvement + Acute + Unsafe Food
        candidates = facts_db.query("derived_fact", object_val="gastrointestinal_involvement")
        for _, patient, _ in candidates:
            if (facts_db.exists("has_symptom", patient, "sudden_onset") and
                facts_db.exists("has_symptom", patient, "unsafe_food_exposure")):
                yield ("possible_diagnosis", patient, "food_poisoning")