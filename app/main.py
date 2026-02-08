from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
import re

from app.logic.facts import Facts
from app.logic.inference import Inference
from app.logic.inquiry import InquiryEngine


app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DiagnosisRequest(BaseModel):
    symptoms: List[str]
    symptoms_no: List[str] = []


@app.get("/")
async def status():
    return JSONResponse(status_code=200, content={"status": "good"})


@app.post("/diagnose")
async def diagnose(payload: DiagnosisRequest):
    facts_db = Facts()
    inference_engine = Inference()

    patient_id = "current_patient"
    
    for symptom in payload.symptoms:
        facts_db.add_fact("has_symptom", patient_id, symptom.lower())
        
    for symptom in payload.symptoms_no:
        facts_db.add_fact("not_has_symptom", patient_id, symptom.lower())

    inferred_knowledge = inference_engine.infer(facts_db)
    
    diagnoses = []
    derived_facts = []
    explanation_trace = []

    for fact in inferred_knowledge:
        predicate, subject, object_val = fact
        if subject == patient_id:
            if predicate == "possible_diagnosis":
                diagnoses.append(object_val)
                explanation_trace.append(f"POSSIBLE DIAGNOSIS: {object_val.replace('_', ' ').title()}")
            elif predicate == "derived_fact":
                derived_facts.append(object_val)
                explanation_trace.append(f"CLINICAL STATE: {object_val.replace('_', ' ').title()}")
            elif predicate in ["warning", "risk", "alert"]:
                explanation_trace.append(f"ALERT: {object_val.replace('_', ' ').title()}")

    next_question = None
    if not diagnoses:
        inquiry = InquiryEngine()
        next_question = inquiry.get_next_question(facts_db)

    return JSONResponse(status_code=200, content={
        "status": "completed",
        "input_symptoms": payload.symptoms,
        "inferred_diseases": list(set(diagnoses)),
        "clinical_states": list(set(derived_facts)),
        "explanation": explanation_trace,
        "next_question": next_question
    })