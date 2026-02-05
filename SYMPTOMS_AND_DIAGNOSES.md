# Symptoms and Diagnoses

## 1. All Valid Symptoms (Symbolic Facts)
These are the accepted symbolic predicates the system recognizes.

### Base Symptoms
- `fever`, `cough`, `headache`, `chills`, `fatigue`, `body_pain`, `nausea`, `sweating`
- **NEW**: `shortness_of_breath`, `chest_pain`, `congestion`, `sensitivity_light`, `stiff_neck`, `facial_pressure`, `loss_of_smell`

### Qualifiers & Subtypes
- `high_fever`, `intermittent_fever`
- `dry_cough`, `productive_cough`
- `severe_headache`, `retro_orbital_pain`
- `joint_pain`, `muscle_pain`
- `abdominal_pain`, `diarrhea` (and `severe_diarrhea`), `vomiting`, `rash`

### Temporal & Context
- `sudden_onset`, `gradual_onset`
- `mosquito_exposure`, `recent_travel`, `unsafe_food_exposure`, `sick_contact`

---

## 2. Diagnoses & Logic Rules

### Respiratory
*   **Influenza**: Fever AND Cough AND Fatigue AND Sudden Onset AND Muscle Pain
*   **Common Cold**: Cough/Congestion AND Gradual Onset AND NOT (Fever OR Breathlessness)
*   **COVID-19**: Fever AND Dry Cough AND Loss of Smell
*   **Pneumonia**: High Fever AND Cough AND Shortness of Breath AND Chest Pain
*   **Acute Bronchitis**: Cough AND Chest Pain AND NOT (High Fever OR Breathlessness)

### Vector-Borne
*   **Malaria**: Fever + Chills + Sweating AND (Mosquito Exposure OR Intermittent Fever)
*   **Dengue**: Fever + Mosquito Exposure + Headache AND (Retro-orbital OR Joint Pain)
*   **Chikungunya**: High Fever + Joint Pain + Mosquito Exposure AND NOT Retro-orbital Pain

### Gastrointestinal
*   **Food Poisoning**: Vomiting/Diarrhea AND Sudden Onset AND Unsafe Food Exposure
*   **Cholera**: Severe Diarrhea + Vomiting + Unsafe Food
*   **Typhoid**: Fever + Headache + Abdominal Pain + Unsafe Food
*   **Viral Gastroenteritis**: Nausea + Vomiting/Diarrhea AND NOT Unsafe Food

### Neurological & Head
*   **Meningitis**: High Fever + Severe Headache + Stiff Neck + Light Sensitivity
*   **Migraine**: Severe Headache + Light Sensitivity + Nausea AND NOT Fever
*   **Sinusitis**: Headache + Congestion + Facial Pressure AND NOT High Fever

---

## 3. Alerts & Warnings (Chaining)
*   **Dengue Hemorrhagic Risk**: IF Dengue AND (Abdominal Pain OR Vomiting)
*   **Sepsis Alert**: IF (Pneumonia OR Meningitis) AND Severe Fatigue
*   **Severe Dehydration**: IF Cholera OR (Food Poisoning AND Severe Diarrhea)
