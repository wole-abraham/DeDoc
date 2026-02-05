# Expansion Strategy for Expert System

## 1. Expanded Fact Taxonomy

We will expand the symbolic predicate space to include specific qualifiers, subtypes, temporal aspects, and context. All remain boolean predicates (True if present/confirmed).

### Base Symptoms (Expanded)
- `fever`
- `cough`
- `headache`
- `chills`
- `fatigue`
- `body_pain`
- `nausea`
- `sweating`
- **NEW**: `rash`
- **NEW**: `diarrhea`
- **NEW**: `abdominal_pain`
- **NEW**: `runny_nose`
- **NEW**: `sore_throat`
- **NEW**: `shortness_of_breath`

### Symptom Qualifiers & Subtypes
- `high_fever` (vs mild)
- `dry_cough` vs `productive_cough` (sputum)
- `retro_orbital_pain` (pain behind eyes - specific to Dengue)
- `severe_headache`
- `joint_pain` (arthralgia) vs `muscle_pain` (myalgia)
- `severe_fatigue` (prostration)

### Temporal Facts
- `sudden_onset` (symptoms appeared rapidly)
- `gradual_onset`
- `intermittent_fever` (comes and goes)
- `duration_gt_3_days`
- `duration_gt_7_days`

### Contextual / Exposure Facts
- `mosquito_exposure` (bites or endemic area)
- `recent_travel`
- `unsafe_food_exposure` (street food, unhygienic water)
- `sick_contact` (contact with someone having similar symptoms)

---

## 2. Question-to-Fact Mapping

These questions will be added to the frontend `questions` tree.

### Fever Qualifiers
- **Question**: "Is your fever very high (above 39°C / 102°F)?"
  - **Fact**: `high_fever`
- **Question**: "Does the fever come and go (intermittent)?"
  - **Fact**: `intermittent_fever`

### Pain Specifics
- **Question**: "Is the headache specifically located behind your eyes?"
  - **Fact**: `retro_orbital_pain`
- **Question**: "Is the body pain mostly in your joints (knees, elbows, wrists)?"
  - **Fact**: `joint_pain`
- **Question**: "Is the body pain mostly in your muscles?"
  - **Fact**: `muscle_pain`

### Cough Specifics
- **Question**: "Is the cough dry (no phlegm/mucus)?"
  - **Fact**: `dry_cough`
- **Question**: "Is the cough producing phlegm or mucus?"
  - **Fact**: `productive_cough`

### Stomach/Digestion
- **Question**: "Do you have pain in your stomach/abdomen?"
  - **Fact**: `abdominal_pain`
- **Question**: "Are you experiencing diarrhea?"
  - **Fact**: `diarrhea`

### Onset & Context
- **Question**: "Did your symptoms appear very suddenly (within a few hours)?"
  - **Fact**: `sudden_onset`
- **Question**: "Have you been exposed to mosquitoes or bitten recently?"
  - **Fact**: `mosquito_exposure`
- **Question**: "Have you eaten street food or potentially unsafe food recently?"
  - **Fact**: `unsafe_food_exposure`

---

## 3. Example Rule Upgrades

We will refine the Python `Rules` class to use strict logical conjunctions of these new facts.

### 1. Malaria
**Current**: Fever AND Chills AND Sweating
**Upgraded**:
```python
def malaria(facts_db):
    # Rule: Fever AND Chills AND Sweating AND (Mosquito_Exposure OR Intermittent_Fever)
    candidates = facts_db.query(predicate="has_symptom", object_val="fever")
    for _, patient, _ in candidates:
         if (facts_db.exists("has_symptom", patient, "chills") and 
             facts_db.exists("has_symptom", patient, "sweating")):
             
             # Refining evidence
             if (facts_db.exists("has_symptom", patient, "mosquito_exposure") or 
                 facts_db.exists("has_symptom", patient, "intermittent_fever")):
                 yield ("diagnosis", patient, "malaria")
```

### 2. Dengue
**Current**: Fever AND Headache AND Body Pain
**Upgraded**:
```python
def dengue(facts_db):
    # Rule: Fever AND (Retro_Orbital_Pain OR Rash) AND Joint_Pain AND Mosquito_Exposure
    candidates = facts_db.query(predicate="has_symptom", object_val="fever")
    for _, patient, _ in candidates:
        has_eye_pain = facts_db.exists("has_symptom", patient, "retro_orbital_pain")
        has_rash = facts_db.exists("has_symptom", patient, "rash")
        has_joint_pain = facts_db.exists("has_symptom", patient, "joint_pain")
        has_mosquito = facts_db.exists("has_symptom", patient, "mosquito_exposure")

        if (has_joint_pain and has_mosquito and (has_eye_pain or has_rash)):
             yield ("diagnosis", patient, "dengue")
```

### 3. Typhoid
**Current**: Fever AND Headache AND Fatigue
**Upgraded**:
```python
def typhoid(facts_db):
    # Rule: Fever AND Abdominal_Pain AND Unsafe_Food_Exposure
    candidates = facts_db.query(predicate="has_symptom", object_val="fever")
    for _, patient, _ in candidates:
        if (facts_db.exists("has_symptom", patient, "abdominal_pain") and 
            facts_db.exists("has_symptom", patient, "unsafe_food_exposure")):
            yield ("diagnosis", patient, "typhoid")
```

### 4. Influenza (Flu)
**Current**: Fever AND Cough AND Fatigue
**Upgraded**:
```python
def flu(facts_db):
    # Rule: Fever AND Cough AND Fatigue AND Sudden_Onset AND Muscle_Pain
    # Differentiates from Cold (Gradual, no fever) and Dengue (Joint pain, not cough focused)
    candidates = facts_db.query(predicate="has_symptom", object_val="fever")
    for _, patient, _ in candidates:
        if (facts_db.exists("has_symptom", patient, "cough") and
            facts_db.exists("has_symptom", patient, "fatigue") and
            facts_db.exists("has_symptom", patient, "sudden_onset") and
            facts_db.exists("has_symptom", patient, "muscle_pain")):
            yield ("diagnosis", patient, "influenza")
```

---

## 4. Design Rationale

1.  **Symbolic & Deterministic**: We are not assigning weights (e.g., "0.8 probability of Malaria"). We are adding strict *requirements* (preconditions) for a rule to fire. If the user does not report "mosquito_exposure", the strict Malaria rule (in this upgraded version) might NOT fire, or we might have a "Likely Malaria" vs "Possible Malaria" separation if we wanted, but strictly speaking, this increases specificity.
2.  **Logic Preservation**: The inference engine (`Inference.infer` and `facts_db`) requires zero changes. We are simply feeding it more granular symbols (`retro_orbital_pain`) instead of just broad ones (`headache`).
3.  **Explainability**: The system can now explain: "Diagnosis is Dengue BECAUSE you have fever, pain behind the eyes, valid mosquito exposure, and joint pain." This is much more convincing than just "Fever + Headache".
4.  **No ML**: No training data is needed. These rules are derived from medical heuristics (textbook definitions).
