# First-Order Logic (FOL) Adherence Report

## Executive Summary
**Status: Partial / Hybrid Implementation**

The application successfully implements strict First-Order Logic (FOL) for the **diagnosis engine** (backend), but uses a **static decision tree** for data collection (frontend). While the final reasoning is sound and deterministic, the frontend collection method limits the flexibility of the expert system.

## 1. Backend (Logic Engine) - `app/logic/rules.py`
**Status: ✅ STRICT FOL COMPLIANCE**
The backend rules are implemented as rigid implications (`A ∧ B → C`), which is the core definition of First-Order Logic in expert systems.

*   **Evidence**:
    *   **Implication**: `IF systemic_illness AND respiratory AND acute AND muscle_pain THEN influenza`
    *   **Negation**: `IF ... AND NOT fever THEN common_cold` (Correctly uses negation for differentiation).
    *   **Quantification**: The code iterates over `candidates` (e.g., `for _, patient, _ in candidates`), which effectively implements Universal Quantification ($\forall x, Symptom(x) \to Diagnosis(x)$).

## 2. Frontend (Data Collection) - `frontend/app.js`
**Status: ⚠️ STATIC DECISION TREE (NOT FOL DRIVEN)**
The frontend forces the user down pre-determined paths. This is a "Decision Tree" structure, not a pure FOL inference engine.

*   **The Limitation**:
    *   In a pure FOL system, the engine should ask the *next most useful question* based on what it knows (e.g., "I know you have a fever, now I need to check for rash specifically").
    *   Currently, `app.js` runs a hardcoded script (`questions` object).
    *   **Impact**: Even if the logic engine *could* diagnose a rare disease given symptoms X and Y, the frontend might never ask about symptom Y because it's not in the hardcoded path.

## 3. Discrepancies & Risks
1.  **Symptom Mapping**: The backend expects specific predicates like `intermittent_fever`. The frontend correctly maps "Comes and goes" to `intermittent_fever` (Line 46), which is good.
2.  **Missing Flexibility**: If you add a new rule to the backend (e.g., for "Zika Virus"), it **will not** automatically work. You must also manually edit the `questions` object in `app.js` to ask about red eyes or rash. A pure FOL system would handle this dynamically.

## Conclusion
Your system **does** follow FOL for the *reasoning* part (making the diagnosis), which ensures explainability and determinism. usage of the "Decision Tree" for input is a valid design choice for simplicity, but it decouples the input logic from the reasoning logic.

**Verdict**: The system is a **Forward-Chaining Expert System** with a **Decision Tree Interface**.
