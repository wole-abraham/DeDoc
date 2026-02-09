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

    QUESTION_MAPPING = {
        "sudden_onset": "Did your symptoms start suddenly?",
        "gradual_onset": "Did your symptoms develop gradually?",
        "mosquito_exposure": "Have you been exposed to mosquitoes?",
        "unsafe_food_exposure": "Have you eaten any potentially unsafe food?",
        "loss_of_smell": "Have you lost your sense of smell?",
        "retro_orbital_pain": "Do you have pain behind your eyes?",
        "sweating": "Are you experiencing excessive sweating?",
        "chills": "Do you have chills?",
        "fatigue": "Do you feel fatigued?",
        "vomiting": "Have you been vomiting?", 
        "sensitivity_light": "Are your eyes sensitive to light?",
        "stiff_neck": "Do you have a stiff neck?",
        "fever": "Do you have a fever?",
        "high_fever": "Do you have a high fever?",
        "intermittent_fever": "Do you have an intermittent fever?",
        "cough": "Do you have a cough?",
        "dry_cough": "Do you have a dry cough?",
        "productive_cough": "Do you have a productive cough?",
        "shortness_of_breath": "Are you experiencing shortness of breath?",
        "diarrhea": "Do you have diarrhea?",
        "severe_diarrhea": "Do you have severe diarrhea?",
        "muscle_pain": "Do you have muscle pain?",
        "joint_pain": "Do you have joint pain?",
        "chest_pain": "Do you have chest pain?",
        "headache": "Do you have a headache?",
        "severe_headache": "Do you have a severe headache?",
        "sneezing": "Are you sneezing frequently?",
        "itchy_eyes": "Do you have itchy eyes?",
        "runny_nose": "Do you have a runny nose?",
        "facial_pain": "Do you have facial pain or pressure?",
        "nasal_congestion": "Do you have nasal congestion?",
        "heartburn": "Do you have heartburn?",
        "acid_reflux": "Do you experience acid reflux?",
        "difficulty_swallowing": "Do you have difficulty swallowing?",
        "nausea": "Do you feel nauseous?",
        "visual_aura": "Do you see flashing lights or zig-zag lines (visual aura)?",
        "persistent_cough": "Do you have a persistent cough (lasting more than 3 weeks)?",
        "weight_loss": "Have you experienced unexplained weight loss?",
        "night_sweats": "Do you have night sweats?",
        "itchy_rash": "Do you have an itchy rash?",
        "rash": "Do you have a rash?",
        "sore_throat": "Do you have a sore throat?",
        "swollen_nodes": "Do you have swollen lymph nodes?"
    }

    return JSONResponse(status_code=200, content={
        "status": "completed",
        "input_symptoms": payload.symptoms,
        "inferred_diseases": list(set(diagnoses)),
        "clinical_states": list(set(derived_facts)),
        "explanation": explanation_trace,
        "next_question": next_question,
        "next_question_text": QUESTION_MAPPING.get(next_question, f"Do you have {next_question.replace('_', ' ')}?") if next_question else None
    })

