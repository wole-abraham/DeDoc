# Frontend Questions and Options (Current)

This file documents the hardcoded decision tree currently implemented in `frontend/app.js`.

## 1. Root
**Question:** "What is your primary concern today?"
- **High Temperature / Fever** (Adds: `fever`) → Next: `fever_q1`
- **Persistent Coughing** (Adds: `cough`) → Next: `cough_q1`
- **Shaking / Chills** (Adds: `chills`) → Next: `chills_q1`
- **Feeling Weak or General Pain** → Next: `general_q1`

---

## 2. Fever Branch
### fever_q1
**Question:** "Have you measured your body temperature?"
- **Yes, High (>39°C)** (Adds: `fever`, `high_fever`) → Next: `fever_pattern`
- **Yes, Moderate** (Adds: `fever`) → Next: `fever_pattern`
- **No, but I feel hot** (Adds: `fever`) → Next: `fever_pattern`
- **No, strictly normal** → Next: `fever_pattern`

### fever_pattern
**Question:** "Does the fever come and go (intermittent) or stay constant?"
- **Intermittent (Comes and goes)** (Adds: `intermittent_fever`) → Next: `fever_sweat`
- **Constant / Continuous** → Next: `fever_sweat`

### fever_sweat
**Question:** "Are you sweating profusely, even when not exerting yourself?"
- **Yes, heavy sweating** (Adds: `sweating`) → Next: `fever_chills`
- **No** → Next: `fever_chills`

### fever_chills
**Question:** "Do you experience shivering or shaking sensations (chills)?"
- **Yes, uncontrollably** (Adds: `chills`) → Next: `pain_head`
- **No** → Next: `pain_head`

---

## 3. Cough Branch
### cough_q1
**Question:** "Is your cough accompanied by a fever?"
- **Yes, I have a fever** (Adds: `fever`) → Next: `cough_type`
- **No fever** → Next: `cough_type`

### cough_type
**Question:** "Is the cough dry or does it produce phlegm?"
- **Dry (No phlegm)** (Adds: `dry_cough`) → Next: `resp_distress`
- **Productive (Phlegm)** (Adds: `productive_cough`) → Next: `resp_distress`

### resp_distress
**Question:** "Are you experiencing shortness of breath or difficulty breathing?"
- **Yes, struggling to breathe** (Adds: `shortness_of_breath`) → Next: `chest_pain_q`
- **No** → Next: `chest_pain_q`

### chest_pain_q
**Question:** "Do you feel pain or tightness specifically in your chest?"
- **Yes** (Adds: `chest_pain`) → Next: `neuro_smell`
- **No** → Next: `neuro_smell`

### neuro_smell
**Question:** "Have you noticed a sudden loss of taste or smell?"
- **Yes** (Adds: `loss_of_smell`) → Next: `pain_head`
- **No** → Next: `pain_head`

---

## 4. Chills / General Branch
### chills_q1
**Question:** "Do you also feel hot or feverish alongside the chills?"
- **Yes** (Adds: `fever`) → Next: `fever_sweat`
- **No, just cold/shaking** → Next: `pain_head`

### general_q1
**Question:** "Do you feel any specific fatigue or tiredness?"
- **Yes, exhausted** (Adds: `fatigue`) → Next: `pain_head`
- **No** → Next: `pain_head`

---

## 5. Convergence: Pain, Headache & Neuro
### pain_head
**Question:** "Are you experiencing a headache or facial pressure?"
- **Yes, Severe Headache** (Adds: `headache`, `severe_headache`) → Next: `head_neuro_1`
- **Yes, Facial Pressure/Sinus** (Adds: `headache`, `facial_pressure`, `congestion`) → Next: `head_neuro_1`
- **Yes, Mild** (Adds: `headache`) → Next: `head_neuro_1`
- **No** → Next: `pain_body`

### head_neuro_1
**Question:** "Does bright light hurt your eyes? Or is your neck stiff?"
- **Light Sensitivity** (Adds: `sensitivity_light`) → Next: `head_neuro_2`
- **Stiff Neck** (Adds: `stiff_neck`) → Next: `head_neuro_2`
- **Both** (Adds: `sensitivity_light`, `stiff_neck`) → Next: `head_neuro_2`
- **Neither** → Next: `pain_head_retro`

### head_neuro_2
**Question:** "Do you also have pain specifically BEHIND your eyes?"
- **Yes** (Adds: `retro_orbital_pain`) → Next: `pain_body`
- **No** → Next: `pain_body`

### pain_head_retro
**Question:** "Is the pain located specifically BEHIND your eyes?"
- **Yes, behind eyes** (Adds: `retro_orbital_pain`) → Next: `pain_body`
- **No** → Next: `pain_body`

---

## 6. Body Pain & Fatigue
### pain_body
**Question:** "Do you have generalized body aches or muscle pain?"
- **Yes, body hurts** (Adds: `body_pain`) → Next: `pain_body_type`
- **No** → Next: `fatigue_check`

### pain_body_type
**Question:** "Is the pain mostly in your joints or your muscles?"
- **Joints (Knees/Elbows)** (Adds: `joint_pain`) → Next: `fatigue_check`
- **Muscles (Aches)** (Adds: `muscle_pain`) → Next: `fatigue_check`
- **Both** (Adds: `joint_pain`, `muscle_pain`) → Next: `fatigue_check`

### fatigue_check
**Question:** "How severe is your fatigue or tiredness?"
- **Extreme / Prostrated** (Adds: `fatigue`, `severe_fatigue`) → Next: `stomach_check`
- **Moderate** (Adds: `fatigue`) → Next: `stomach_check`
- **Normal Energy** → Next: `stomach_check`

---

## 7. Gastrointestinal & Context
### stomach_check
**Question:** "Do you have any stomach pain, diarrhea, or nausea?"
- **Nausea/Vomiting** (Adds: `nausea`, `vomiting`) → Next: `stomach_check_2`
- **Stomach Pain** (Adds: `abdominal_pain`) → Next: `stomach_check_2`
- **No** → Next: `context_onset`

### stomach_check_2
**Question:** "Are you also experiencing diarrhea?"
- **Yes, Severe/Watery** (Adds: `diarrhea`, `severe_diarrhea`) → Next: `context_onset`
- **Yes, Mild** (Adds: `diarrhea`) → Next: `context_onset`
- **No** → Next: `context_onset`

### context_onset
**Question:** "Did these symptoms appear suddenly or gradually?"
- **Suddenly (Rapid onset)** (Adds: `sudden_onset`) → Next: `context_exposure`
- **Gradually (Over days)** (Adds: `gradual_onset`) → Next: `context_exposure`

### context_exposure
**Question:** "Have you had any recent travel or mosquito exposure?"
- **Mosquito Bites / Area** (Adds: `mosquito_exposure`) → Next: `context_food`
- **Recent Travel** (Adds: `recent_travel`) → Next: `context_food`
- **Both** (Adds: `mosquito_exposure`, `recent_travel`) → Next: `context_food`
- **No** → Next: `context_food` 

### context_food
**Question:** "Have you consumed any street food or potentially unsafe water recently?"
- **Yes** (Adds: `unsafe_food_exposure`) → Next: `final_review`
- **No** → Next: `final_review`

### final_review
**Question:** "We have gathered your symptoms. Ready to diagnose?"
- **Analyze Symptoms** → Next: `diagnose` (Triggers API call)
- **Start Over** → Next: `root`
