# DeDoc System Internals

## 1. Introduction
This document provides a low-level walkthrough of the DeDoc Expert System, from the moment a user clicks a button to the final diagnosis. It covers the data flow, the logical reasoning engine, and the dynamic inquiry system.

---

## 2. Frontend Lifecycle (`app.js`)

### Step 2.1: Bootstrap (The Seed)
The user is presented with a **Static Question** ("What is your primary concern?").
-   **User Action**: Clicks "High Temperature / Fever".
-   **State Change**: The frontend adds `fever` to the `collectedSymptoms` Set.
-   **Trigger**: The frontend calls `runDynamicDiagnosis()`.

### Step 2.2: The API Request
The frontend packages the current state into a JSON payload and sends it to the backend.

**POST** `/diagnose`
```json
{
  "symptoms": ["fever"],
  "symptoms_no": []
}
```

---

## 3. Backend Processing (`main.py`)

### Step 3.1: Knowledge Base Initialization
The API receives the request and creates a fresh instance of `Facts` (The Knowledge Base).
-   It iterates through `symptoms` and adds: `("has_symptom", "current_patient", "fever")`.
-   It iterates through `symptoms_no` and adds negative facts (if any).

### Step 3.2: Forward Chaining Inference (`inference.py`)
The `Inference` engine loads the `RULES_KB` (from `declarative_rules.py`) and begins the **Match-Resolve-Act** cycle.

**Cycle 1:**
-   **Rule Check**: `derive_systemic` requires `fever` AND `fatigue`.
    -   We have `fever`. We are missing `fatigue`. -> Rule fails.
-   **Rule Check**: `norm_high_fever` requires `high_fever`. -> Rule fails.
-   **Result**: No new facts derived in this cycle.

### Step 3.3: The Inquiry Engine (`inquiry.py`)
Since no diagnosis was found, the `InquiryEngine` is invoked to find the next question.

**Introspection Process:**
1.  **Candidate Selection**: The engine scans all rules that output a `possible_diagnosis` (e.g., Flu, Malaria).
2.  **Viability Check**:
    -   **Flu**: Requires `systemic_illness` (which requires `fatigue`). We have `fever`. Is `fatigue` contradicted? NO. -> **Candidate found: Fatigue**.
    -   **Malaria**: Requires `chills`. Is `chills` contradicted? NO. -> **Candidate found: Chills**.
3.  **Heuristic Scoring**: The engine counts how often each missing symptom appears in viable rules.
    -   If `fatigue` appears 3 times and `chills` 1 time, `fatigue` wins.
4.  **Output**: The engine returns `fatigue` as `next_question`.

### Step 3.4: API Response
The backend sends the result back to the frontend.

```json
{
  "status": "completed",
  "inferred_diseases": [],
  "explanation": [],
  "next_question": "fatigue"
}
```

---

## 4. Frontend - The Loop Continues

### Step 4.1: Rendering the Dynamic Question
-   `app.js` sees `next_question: "fatigue"`.
-   It renders: **"Do you have fatigue?"** with [YES] and [NO] buttons.

### Step 4.2: User Interaction
-   **User Action**: Clicks "YES".
-   **State Change**: `fatigue` is added to `collectedSymptoms`.
-   **Loop**: `runDynamicDiagnosis()` is called again.

---

## 5. The Deduction (Cycle 2)

**New Payload:** `symptoms: ["fever", "fatigue"]`

**Backend Inference Cycle:**
1.  **Rule Match**: `derive_systemic` requires `fever` + `fatigue`.
    -   Both exist!
    -   **Action**: Add fact `("derived_fact", "current_patient", "systemic_illness")`.
2.  **Rule Match**: `diag_flu` requires `systemic_illness` + ...
    -   Now valid! (Assuming other conditions met).

If all conditions for a diagnosis are met, `possible_diagnosis` is added to the KB.

---

## 6. Final State
If a diagnosis is found:
1.  Backend returns `inferred_diseases: ["influenza"]`.
2.  Frontend displays **"DIAGNOSIS CONFIRMED: INFLUENZA"**.
3.  Frontend updates the "Fact Base" sidebar with the full derivation trace (e.g., "Clinical State: Systemic Illness").
