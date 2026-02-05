# Detailed Expansion Plan: Scaling the Expert System

## SECTION 1 — Expanded Fact Taxonomy

This taxonomy integrates existing facts with carefully selected new facts to maximize diagnostic coverage.

### 1. Base Symptoms (Primary Complaints)
*Existing:* `fever`, `cough`, `headache`, `chills`, `fatigue`, `body_pain`, `nausea`, `sweating`
*New:*
- `shortness_of_breath` (Justification: Critical discriminator for Pneumonia, Asthma, severe COVID-19)
- `chest_pain` (Justification: Differentiates deep respiratory infections from upper respiratory)
- `congestion` (Justification: Key for Sinusitis and Cold differentiation)
- `sensitivity_light` (Justification: Specific to Migraine and Meningitis)
- `stiff_neck` (Justification: High specificity for Meningitis)

### 2. Qualifiers & Subtypes (Clarifications)
*Existing:* `high_fever`, `intermittent_fever`, `dry_cough`, `productive_cough`, `severe_headache`, `retro_orbital_pain`, `joint_pain`, `muscle_pain`, `abdominal_pain`, `diarrhea`, `vomiting`, `rash`
*New:*
- `severe_diarrhea` (Justification: Differentiates Cholera/Severe Dysentery from mild Gastroenteritis)
- `facial_pressure` (Justification: Specific to Sinusitis)
- `loss_of_smell` (Justification: highly specific discriminator for COVID-19)

### 3. Temporal Facts (Time Course)
*Existing:* `sudden_onset`, `gradual_onset`

### 4. Contextual Facts (Exposure/History)
*Existing:* `mosquito_exposure`, `recent_travel`, `unsafe_food_exposure`, `sick_contact`

---

## SECTION 2 — Expanded Diagnosis List (Target: 18 distinct diagnoses)

We expand from 5 to 18 diagnoses by effectively reusing combinations of facts.

| Diagnosis | Key Differentiating Facts | Overlap Risks (Handled by Rules) |
| :--- | :--- | :--- |
| **Influenza** | Sudden onset, Muscle pain, Fever, Dry cough | Common Cold, Dengue |
| **Common Cold** | Gradual onset, Congestion, No high fever | Flu, Sinusitis |
| **Malaria** | Fever, Chills, Sweating, Intermittent pattern | Dengue, Typhoid |
| **Typhoid Fever** | Fever, Headache, Abdominal pain, Unsafe food | Gastroenteritis |
| **Dengue Fever** | Retro-orbital/Joint pain, Mosquitoes | Malaria, Chikungunya |
| **Viral Gastroenteritis** | Nausea, Vomiting, Diarrhea, No unsafe food link | Food Poisoning |
| **Food Poisoning** | Vomiting, Diarrhea, Sudden onset, Unsafe food | Gastroenteritis |
| **Cholera** | Severe diarrhea, Vomiting, Unsafe water/food | Food Poisoning |
| **Pneumonia** | High fever, Productive cough, Chest pain, Breathlessness | Bronchitis, Flu |
| **Acute Bronchitis** | Cough (Productive/Dry), No high fever, Chest discomfort | Pneumonia, Cold |
| **Sinusitis** | Headache, Facial pressure, Congestion | Cold, Migraine |
| **Tension Headache** | Headache, Muscle pain (neck), No fever | Migraine, Sinusitis |
| **Migraine** | Severe headache, Light sensitivity, Nausea | Tension Headache |
| **Meningitis** | High fever, Stiff neck, Severe headache, Light sensitivity | Migraine, Flu |
| **COVID-19** | Fever, Dry cough, Loss of smell, Breathlessness | Flu, Cold |
| **Chikungunya** | High Fever, Severe Joint Pain, Mosquitoes | Dengue |
| **Tonsillitis** | Fever, Sore throat (implied by pain check), Swollen glands | Cold, Flu |
| **Gastritis** | Upper Abdominal pain, Nausea, No diarrhea | Gastroenteritis |

---

## SECTION 3 — Rule Set (Readable Logic Form)

### Group A: Respiratory & Viral
**Rule: Influenza**
IF `fever` AND `cough` AND `fatigue` AND `sudden_onset` AND `muscle_pain`
THEN `diagnosis(influenza)`

**Rule: Common Cold**
IF `cough` OR `congestion`
AND `gradual_onset`
AND NOT `high_fever`
AND NOT `shortness_of_breath`
THEN `diagnosis(common_cold)`

**Rule: COVID-19 (Classic)**
IF `fever` AND `dry_cough` AND `loss_of_smell`
THEN `diagnosis(covid19)`

**Rule: Pneumonia**
IF `high_fever` AND `cough` AND `shortness_of_breath` AND `chest_pain`
THEN `diagnosis(pneumonia)`

**Rule: Acute Bronchitis**
IF `cough` AND `chest_pain`
AND NOT `high_fever`
AND NOT `shortness_of_breath`
THEN `diagnosis(bronchitis)`

### Group B: Vector-Borne
**Rule: Malaria**
IF `fever` AND `chills` AND `sweating`
AND (`mosquito_exposure` OR `intermittent_fever`)
THEN `diagnosis(malaria)`

**Rule: Dengue (Classic)**
IF `fever` AND `mosquito_exposure`
AND (`retro_orbital_pain` OR `joint_pain`)
AND `severe_headache`
THEN `diagnosis(dengue)`

**Rule: Chikungunya**
IF `high_fever` AND `joint_pain` AND `mosquito_exposure`
AND NOT `retro_orbital_pain`  *(Differentiation from Dengue)*
THEN `diagnosis(chikungunya)`

### Group C: Gastrointestinal
**Rule: Food Poisoning**
IF `vomiting` OR `diarrhea`
AND `sudden_onset`
AND `unsafe_food_exposure`
THEN `diagnosis(food_poisoning)`

**Rule: Viral Gastroenteritis**
IF `vomiting` OR `diarrhea`
AND `nausea`
AND NOT `unsafe_food_exposure`
AND NOT `blood_in_stool` *(Future fact, assumed negative for now)*
THEN `diagnosis(viral_gastroenteritis)`

**Rule: Cholera**
IF `severe_diarrhea` AND `vomiting` AND `unsafe_food_exposure`
THEN `diagnosis(cholera)`

**Rule: Typhoid**
IF `fever` AND `headache` AND `abdominal_pain` AND `unsafe_food_exposure`
THEN `diagnosis(typhoid)`

### Group D: Head & Neurological
**Rule: Meningitis**
IF `high_fever` AND `severe_headache` AND `stiff_neck` AND `sensitivity_light`
THEN `diagnosis(meningitis)`

**Rule: Migraine**
IF `severe_headache` AND `sensitivity_light` AND `nausea`
AND NOT `fever`
THEN `diagnosis(migraine)`

**Rule: Sinusitis**
IF `headache` AND `congestion` AND `facial_pressure`
AND NOT `high_fever`
THEN `diagnosis(sinusitis)`

---

## SECTION 4 — Chaining Examples (Multi-Step Inference)

We can deduce secondary conditions or warnings based on primary diagnoses usually established in step 1.

**Example 1: Dengue Warning Signs**
*Base Facts:* `fever`, `mosquito_exposure`, `retro_orbital_pain`, `abdominal_pain`, `vomiting`
*Step 1 Inference:* `diagnosis(dengue)` hits.
*Step 2 Chaining Rule:*
IF `diagnosis(dengue)` AND (`abdominal_pain` OR `vomiting`)
THEN `warning(dengue_hemorrhagic_risk)`

**Example 2: Sepsis Risk**
*Base Facts:* `high_fever`, `low_bp` (if added) OR `extreme_fatigue`, `confusion` (if added)
*Scenario using current facts:*
IF `diagnosis(pneumonia)` AND `extreme_fatigue` AND `sudden_onset`
THEN `risk(severe_respiratory_distress)`

**Example 3:Dehydration Risk**
*Base Facts:* `severe_diarrhea`, `vomiting`
*Step 1 Inference:* `diagnosis(cholera)`
*Step 2 Chaining Rule:*
IF `diagnosis(cholera)` OR (`diagnosis(food_poisoning)` AND `severe_diarrhea`)
THEN `alert(severe_dehydration_risk)`

---

## SECTION 5 — Question-to-Fact Mapping

For the 7 new facts, we map them to specific binary questions.

### Branch: Respiratory (Cough/Breathing)
**Question:** "Are you experiencing shortness of breath or difficulty breathing?"
- **Yes** -> `shortness_of_breath`

**Question:** "Do you feel pain or tightness specifically in your chest?"
- **Yes** -> `chest_pain`

**Question:** "Is your nose blocked or congested?"
- **Yes** -> `congestion`

**Question:** "Have you noticed a sudden loss of taste or smell?"
- **Yes** -> `loss_of_smell`

### Branch: Head & Neck
**Question:** "Does bright light hurt your eyes or make your headache worse?"
- **Yes** -> `sensitivity_light`

**Question:** "Is your neck feeling stiff and difficult to move?"
- **Yes** -> `stiff_neck`

**Question:** "Do you feel pressure around your eyes, cheeks, or forehead?"
- **Yes** -> `facial_pressure`

### Branch: Digestion
**Question:** "Is the diarrhea very watery and severe?"
- **Yes** -> `severe_diarrhea`

---

## SECTION 6 — Design Rationale

1.  **Scale via Combinatorics**: By adding just ~7 key facts (`shortness_of_breath`, `stiff_neck`, etc.), we unlock an entire class of diagnoses (Scanning for Meningitis, Pneumonia, Sinusitis) that were previously impossible. This moves the system from "general fever checker" to "broad triage tool".
2.  **Logic Integrity**: We maintain strict First-Order Logic constraints. There are no probabilities "maybe flu". It is "If A and B and C and D -> Flu". This ensures 100% explainability. If the system says Meningitis, it is *only* because the user checked Yes for Stiff Neck, High Fever, and Light Sensitivity.
3.  **Ambiguity Handling**: We handle ambiguity through **negation logic**. For example, Tension Headache is defined not just by what it is (Headache + Muscle Pain) but by what it is *not* (Fever). This prevents it from firing when the user actually has the Flu.
4.  **No ML Required**: We are encoding expert medical heuristics directly. ML would attempt to learn these patterns from data (often successfully, but opaquely). Here, we explicitly encode the "classic textbook definitions" of diseases, which is safer for a deterministic triage system.
