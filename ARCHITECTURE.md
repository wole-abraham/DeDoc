# System Architecture

## Overview
DeDoc follows a **Client-Server** architecture where the frontend handles data collection via a decision tree, and the backend serves as a stateless expert system engine using First-Order Logic (FOL).

## Component Details

### 1. Frontend (Client)
-   **Technology**: HTML5, Vanilla CSS, Vanilla JavaScript.
-   **Responsibility**:
    -   Guides the user through a branching Questionnaire (Decision Tree).
    -   Collects symbolic symptoms (e.g., `fever`, `cough`) based on user answers.
    -   Sends the final list of symptoms to the backend API.
    -   Visualizes the diagnosis results and the logic trace.
-   **Key File**: `frontend/app.js`

### 2. Backend (Server)
-   **Technology**: Python 3, FastAPI.
-   **Responsibility**:
    -   Provides a stateless REST API (`POST /diagnose`).
    -   Orchestrates the Logic Engine.
    -   Converts input strings into logical predicates.
-   **Key File**: `app/main.py`

### 3. Logic Core (Expert System)
-   **Technology**: Custom Python Classes.
-   **Responsibility**:
    -   **Facts**: Maintains the state of the current patient's known attributes.
    -   **Rules**: Contains strict logical implications (e.g., `IF A AND B THEN C`).
    -   **Inference**: Performs **Forward Chaining** (Repeatedly applying rules until no new facts can be derived) to reach a deterministic conclusion.
-   **Key Files**: `app/logic/inference.py`, `app/logic/rules.py`
