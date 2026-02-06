# System Architecture

## Overview
DeDoc follows a **Client-Server** architecture where the frontend handles data collection via a decision tree, and the backend serves as a stateless expert system engine using First-Order Logic (FOL).

```mermaid
graph TD
    subgraph Client ["Frontend (Web Interface)"]
        UI[User Interface (HTML/CSS)]
        JS[Logic Controller (app.js)]
        DT[Decision Tree (Hardcoded Questions)]
    end

    subgraph Server ["Backend (Python/FastAPI)"]
        API[API Endpoint (POST /diagnose)]
        Engine[Inference Engine (Forward Chaining)]
        KB[Knowledge Base (Transient Facts)]
        Rules[Rule Set (Symbolic Logic)]
    end

    User((User)) -->|Answers Questions| UI
    UI -->|Input Events| JS
    JS -->|Traverses| DT
    DT -->|Collects Symptoms| JS
    JS -->|POST {symptoms}| API
    API -->|Initialize| KB
    API -->|Run Inference| Engine
    Engine -->|Query| KB
    Engine -->|Apply Rules| Rules
    Rules -->|New Facts (Diagnoses)| KB
    Engine -->|Results & Explanation| API
    API -->|JSON Response| JS
    JS -->|Render Results| UI
```

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
