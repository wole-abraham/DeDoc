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
from app.nlp.parser import SymptomParser

app = FastAPI()

symptom_parser = SymptomParser()

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

class ChatRequest(BaseModel):
    message: str
    symptoms: List[str] = []
    symptoms_no: List[str] = []
    last_question_symptom: Optional[str] = None

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

@app.post("/chat")
async def chat(payload: ChatRequest):
    new_positive = []
    new_negative = []
    
    msg_lower = payload.message.lower().strip()
    
    if payload.last_question_symptom:
        if re.search(r'\b(yes|yeah|yep|sure|correct)\b', msg_lower):
            new_positive.append(payload.last_question_symptom)
        elif re.search(r'\b(no|nope|nah|negative)\b', msg_lower):
            new_negative.append(payload.last_question_symptom)

    extracted = symptom_parser.extract_symptoms(payload.message)
    
    current_positive = set(payload.symptoms + new_positive + extracted['present'])
    current_negative = set(payload.symptoms_no + new_negative + extracted['absent'])
    
    current_negative = current_negative - current_positive
    
    facts_db = Facts()
    patient_id = "current_patient"
    
    for s in current_positive:
        facts_db.add_fact("has_symptom", patient_id, s)
    for s in current_negative:
        facts_db.add_fact("not_has_symptom", patient_id, s)
        
    inference_engine = Inference()
    inferred_knowledge = inference_engine.infer(facts_db)
    
    diagnoses = []
    
    for fact in inferred_knowledge:
        predicate, subject, object_val = fact
        if subject == patient_id and predicate == "possible_diagnosis":
            diagnoses.append(object_val)
            
    response_text = ""
    next_q = None
    
    new_found = set(new_positive + extracted['present'])
    if new_found:
        readable_symptoms = [s.replace('_', ' ') for s in new_found]
        if len(readable_symptoms) > 1:
            response_text += f"I've noted that you have: {', '.join(readable_symptoms)}. "
        else:
            response_text += f"I've noted that you have {readable_symptoms[0]}. "
            
    if diagnoses:
        diag_str = ", ".join([d.replace('_', ' ').title() for d in list(set(diagnoses))])
        response_text += f"Based on your symptoms, a possible diagnosis is: {diag_str}. Please consult a doctor for confirmation."
    else:
        inquiry = InquiryEngine()
        next_q = inquiry.get_next_question(facts_db)
        
        if next_q:
            symptom_name = next_q.replace('_', ' ')
            response_text += f"Do you have {symptom_name}?"
        else:
            if not current_positive:
                 response_text += "Please describe your symptoms."
            else:
                 response_text += "I'm unable to determine a specific diagnosis with the current information. Please provide more details."

    return JSONResponse(status_code=200, content={
        "message": response_text,
        "symptoms": list(current_positive),
        "symptoms_no": list(current_negative),
        "last_question_symptom": next_q, 
        "diagnosis_found": bool(diagnoses)
    })
