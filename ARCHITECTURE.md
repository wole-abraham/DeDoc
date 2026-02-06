# System Architecture

## Overview
DeDoc follows a **Client-Server** architecture. The Frontend is a thin client that collects symptoms and renders questions, while the Backend is a stateful Logic Engine that drives the entire diagnostic process using First-Order Logic (FOL).

```mermaid
graph TD
    subgraph Client ["Frontend (Web Interface)"]
        UI["User Interface (HTML/CSS)"]
        JS["Dynamic Controller (app.js)"]
    end

    subgraph Server ["Backend (Python/FastAPI)"]
        API["API Endpoint (POST /diagnose)"]
        
        subgraph LogicCore ["Expert System Engine"]
            Infer["Inference Engine (Forward Chaining)"]
            Inquiry["Inquiry Engine (Backward Chaining)"]
            KB["Knowledge Base (Facts)"]
            Rules["Declarative Rules (Logic Definitions)"]
        end
    end

    User((User)) -->|1. Selects Symptom| UI
    UI -->|2. Event| JS
    JS -->|3. POST {symptoms, symptoms_no}| API
    
    API -->|4. Initialize| KB
    API -->|5. Run Inference| Infer
    Infer -->|Read/Write| KB
    Infer -->|Apply| Rules
    
    Infer -->|6. Result: Diagnoses?| API
    
    API -.->|7a. If No Diagnosis| Inquiry
    Inquiry -->|Introspect| Rules
    Inquiry -->|Check Contradictions| KB
    Inquiry -->|8. Next Best Question| API
    
    API -->|9. JSON Response| JS
    JS -->|10. Render Question / Result| UI
```

## Component Details

### 1. Frontend (Client)
-   **Technology**: HTML5, Vanilla CSS, Vanilla JavaScript.
-   **Responsibility**:
    -   **Zero Logic**: Does not contain any medical rules.
    -   **Dynamic Rendering**: Renders questions exactly as instructed by the backend.
    -   **State Tracking**: Maintains the user's `YES` and `NO` answers during the session.
-   **Key File**: `frontend/app.js`

### 2. Backend (Server)
-   **Technology**: Python 3, FastAPI.
-   **Responsibility**:
    -   **Orchestration**: Manages the flow between the Inference and Inquiry engines.
    -   **API Interface**: Exposes a stateless `POST` endpoint that accepts the full patient history for every request.
-   **Key File**: `app/main.py`

### 3. Logic Core (Expert System)
-   **Technology**: Custom Python Classes.
-   **Responsibility**:
    -   **Inference Engine (Forward Chaining)**: Derives new facts (e.g., "Systemic Illness") from raw symptoms. *determines what is TRUE*.
    -   **Inquiry Engine (Backward Chaining)**: Scans the rule base to find what information is *MISSING* to confirm a diagnosis. *Determines what to ASK*.
    -   **Declarative Rules**: A passive data structure defining the medical logic.
-   **Key Files**: `app/logic/inference.py`, `app/logic/inquiry.py`, `app/logic/declarative_rules.py`
