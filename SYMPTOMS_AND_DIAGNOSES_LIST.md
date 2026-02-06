# Symptoms and Diagnoses Reference

This document provides a comprehensive list of all symptoms recognized by the system and the possible diagnoses that can be inferred.

## Possible Diagnoses

1.  **Influenza**
    *   *Logic*: Systemic Illness + Respiratory Involvement + Acute Onset + Muscle Pain
2.  **Pneumonia**
    *   *Logic*: Respiratory Involvement + High Fever + Shortness of Breath + Chest Pain
3.  **Common Cold**
    *   *Logic*: Respiratory Involvement + Gradual Onset + **NO** Fever + **NO** Shortness of Breath
4.  **COVID-19**
    *   *Logic*: Fever + Dry Cough + Loss of Smell
5.  **Meningitis**
    *   *Logic*: Meningeal Signs (Stiff Neck/Light Sensitivity) + High Fever + Severe Headache
6.  **Malaria**
    *   *Logic*: Fever + Chills + Sweating + (Mosquito Exposure **OR** Intermittent Fever)
7.  **Dengue**
    *   *Logic*: Fever + Mosquito Exposure + Severe Headache + (Retro-Orbital Pain **OR** Joint Pain)
8.  **Food Poisoning**
    *   *Logic*: GI Involvement + Sudden Onset + Unsafe Food Exposure

---

## Known Symptoms

The system can recognize and deduce the following symptoms.

### General / Systemic
-   `fever` (and `high_fever`, `intermittent_fever`)
-   `chills`
-   `sweating`
-   `fatigue`
-   `body_pain` (and `muscle_pain`, `joint_pain`)
-   `sudden_onset` (vs `gradual_onset`)

### Respiratory
-   `cough` (and `dry_cough`, `productive_cough`)
-   `shortness_of_breath`
-   `chest_pain`
-   `congestion` (Derived logic implicates cold, but not strictly used in current diagnosies as a primary key)

### Head & Neurological
-   `headache` (and `severe_headache`, `retro_orbital_pain`)
-   `stiff_neck`
-   `sensitivity_light`
-   `loss_of_smell`
-   `facial_pressure`

### Gastrointestinal
-   `nausea`
-   `vomiting`
-   `diarrhea` (and `severe_diarrhea`)
-   `abdominal_pain`

### Contextual
-   `mosquito_exposure`
-   `recent_travel`
-   `unsafe_food_exposure`
-   `sick_contact`
