# Medical Expert System - User Guide

## 1. Project Overview

**DeDoc** is a deterministic Medical Expert System powered by First-Order Logic (FOL). Unlike probability-based AI, this system uses strict rule-based deductions to identify potential diagnoses based on your reported symptoms.

### Key Features
-   **Deterministic Logic**: Diagnoses are strictly derived from logical rules (e.g., `IF fever AND cough AND ... THEN Influenza`).
-   **Explainability**: Every diagnosis can be traced back to the specific symptoms that triggered it.
-   **Privacy**: Operating entirely locally, no data is sent to external servers.

---

## 2. Getting Started

### Prerequisites
-   **Python 3.8+** must be installed on your system.

### Installation
1.  Open your terminal or command prompt.
2.  Navigate to the `dedoc` directory:
    ```bash
    cd dedoc
    ```
3.  Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## 3. Usage Guide

You can interact with the expert system in two ways: via the Command Line Interface (CLI) or the Web Interface.

### Option A: Command Line Interface (CLI)
This is the most direct way to test the logic engine.

1.  Run the interactive diagnosis script:
    ```bash
    python run_interactive_diagnosis.py
    ```
2.  The system will ask you a series of `Yes/No` questions relative to your symptoms.
3.  Type `y` for Yes, `n` for No, or `s` to Skip/Unknown.
4.  The system will output a confirmed diagnosis once logical certainty is reached, or inform you if no diagnosis matches your strict criteria.

### Option B: Web Interface
A user-friendly visual interface for the expert system.

1.  Navigate to the `frontend` directory.
2.  Open the `index.html` file in your web browser (Chrome, Firefox, Edge, etc.).
    -   You can double-click the file, or right-click -> Open with -> [Browser].
3.  Click "Start Diagnosis" and answer the questions presented on the screen.
4.  The system will display the result at the end of the process.

---

## 4. Troubleshooting

-   **"Module not found" error**: Ensure you have installed the requirements using `pip install -r requirements.txt`.
-   **No diagnosis found**: The system is strict. If your symptoms do not perfectly match the clinical definition encoded in the rules, it will default to "Undiagnosed" rather than guessing. This is a safety feature.

---

## 5. Medical Disclaimer

**IMPORTANT**: This software is for **educational and research purposes only**. It is **NOT** a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
