# DeDoc — a rule-based medical diagnosis expert system

DeDoc is a **first-order logic expert system** that narrows a set of reported
symptoms down to a likely condition. Rather than a statistical model, it uses a
classic inference engine: forward chaining to derive new facts from the symptoms
you give it, and backward chaining to work out which question to ask next.

The result is a diagnosis you can trace — every conclusion is backed by a rule
that fired, not a probability.

---

## How it works

The backend is a stateful logic engine; the frontend is a thin client that
collects symptoms and renders whatever question the engine asks next.

```
User selects symptoms
   └─> POST /diagnose { symptoms, symptoms_no }
         ├─ Knowledge Base initialised from the reported facts
         ├─ Inference Engine (forward chaining) derives everything entailed
         ├─ Inquiry Engine (backward chaining) picks the most informative
         │  unanswered question
         └─ Returns either the next question, or a final diagnosis
   └─> Client answers → loop until the engine concludes
```

Two chaining strategies, doing different jobs:

- **Forward chaining** (`inference.py`) — given the facts, fire every rule whose
  premises are satisfied, add the conclusions, repeat until nothing new appears.
- **Backward chaining** (`inquiry.py`) — given the candidate conclusions, work
  backwards to find which unknown fact would most usefully be resolved, and ask
  the user about that.

## Architecture

```
app/
  main.py                  FastAPI app — GET / and POST /diagnose
  logic/
    declarative_rules.py   Rule definitions (the knowledge base, as data)
    rules.py               Rule representation and matching
    facts.py               Fact store / working memory
    inference.py           Forward-chaining inference engine
    inquiry.py             Backward-chaining question selection
  data/
    symptoms.json          Symptom vocabulary presented to the client
frontend/
  index.html               UI shell
  app.js                   Dynamic controller — talks to /diagnose
  style.css                Styling
dataset.txt                Source data the rules were derived from
```

Separating `declarative_rules.py` (the *what*) from `inference.py` (the *how*)
is the point of the design: medical knowledge can be edited without touching
the engine.

## Stack

| Layer | Choice |
|---|---|
| Backend | Python 3.10+, FastAPI |
| Server | Uvicorn (via `fastapi dev`) |
| Frontend | Vanilla HTML / CSS / JavaScript — no build step |
| Reasoning | Hand-written forward and backward chaining, no ML dependency |

## Getting started

Requires Python 3.10+.

```bash
python -m venv venv
source venv/bin/activate        # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
fastapi dev
```

Then open `frontend/index.html` in a browser. The frontend is static — no build
or dev server needed — but the API must be running for it to do anything.

## API reference

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/` | Service check |
| `POST` | `/diagnose` | Submit `{ symptoms, symptoms_no }`; returns the next question or a final diagnosis |

Interactive docs at `/docs` while the server is running.

## Further reading

- [`ARCHITECTURE.md`](ARCHITECTURE.md) — system design with a Mermaid diagram of
  the client/server split and the engine internals.
- [`TECHNICAL_DOCUMENTATION.txt`](TECHNICAL_DOCUMENTATION.txt) — detailed notes
  on the rule format and inference behaviour.

## Status

Academic / demonstration project. The knowledge base covers the conditions in
`dataset.txt` only — **this is not a clinical tool and must not be used for
actual medical decisions.**
