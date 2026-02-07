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

# Initialize NLP Parser
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
    symptoms_no: List[str] = [] # User explicitly said NO to these

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
    """
    State-less, First-Order Logic Diagnosis Endpoint.
    Now supports Interactive Inquiry.
    """
    facts_db = Facts()
    inference_engine = Inference()

    patient_id = "current_patient"
    
    # Load Positive Facts
    for symptom in payload.symptoms:
        facts_db.add_fact("has_symptom", patient_id, symptom.lower())
        
    # Load Negative Facts (Crucial for Inquiry)
    for symptom in payload.symptoms_no:
        facts_db.add_fact("not_has_symptom", patient_id, symptom.lower())

    inferred_knowledge = inference_engine.infer(facts_db)
    
    diagnoses = []
    derived_facts = []
    explanation_trace = []

    # Map output predicates to categories
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

    # Determine Next Best Question if indeterminate
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
    """
    Conversational endpoint that uses NLP to extract symptoms 
    and maintains logic-based diagnosis flow.
    """
    
    # 1. Handle "Yes/No" context from previous question
    new_positive = []
    new_negative = []
    
    msg_lower = payload.message.lower().strip()
    
    if payload.last_question_symptom:
        # Check for affirmative
        if re.search(r'\b(yes|yeah|yep|sure|correct)\b', msg_lower):
            new_positive.append(payload.last_question_symptom)
        # Check for negative
        elif re.search(r'\b(no|nope|nah|negative)\b', msg_lower):
            new_negative.append(payload.last_question_symptom)

    # 2. Extract specific symptoms from text (NLP)
    extracted = symptom_parser.extract_symptoms(payload.message)
    
    # Combine all symptoms
    # Ensure they are lower case and unique
    current_positive = set(payload.symptoms + new_positive + extracted['present'])
    current_negative = set(payload.symptoms_no + new_negative + extracted['absent'])
    
    # Remove conflicts (if something is in both, maybe prioritize positive or keep as ambiguous? 
    # For now, let positive override negative if user stated it)
    current_negative = current_negative - current_positive
    
    # 3. Run Inference Logic (Reuse diagnose logic largely)
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
            
    # 4. Formulate Response
    response_text = ""
    next_q = None
    
    # If we found new symptoms from the text, acknowledge them
    new_found = set(new_positive + extracted['present'])
    if new_found:
        readable_symptoms = [s.replace('_', ' ') for s in new_found]
        if len(readable_symptoms) > 1:
            response_text += f"I've noted that you have: {', '.join(readable_symptoms)}. "
        else:
            response_text += f"I've noted that you have {readable_symptoms[0]}. "
            
    if diagnoses:
        # We have a diagnosis!
        diag_str = ", ".join([d.replace('_', ' ').title() for d in list(set(diagnoses))])
        response_text += f"Based on your symptoms, a possible diagnosis is: {diag_str}. Please consult a doctor for confirmation."
    else:
        # No diagnosis yet, ask next question
        inquiry = InquiryEngine()
        next_q = inquiry.get_next_question(facts_db)
        
        if next_q:
            # next_q is likely a symptom ID or similar. We need to make it a question.
            # Assuming inquiry engine returns a symptom ID string
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
        "last_question_symptom": next_q, # This sets the context for the NEXT turn
        "diagnosis_found": bool(diagnoses)
    })
