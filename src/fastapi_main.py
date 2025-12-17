from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import json

from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from clients import _groq_client
from prompts import prompt_to_grade


load_dotenv()

with open("../data/questions.json", "rt") as fid:
    QUESTIONS = json.load(fid)  

app = FastAPI(
    title="Assessment Grading API",
    description="AI-powered assessment grading system",
    version="1.0.0"
)


# Add CORS - allow Streamlit to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # Local Streamlit
        "https://visionomy-edtech-app.streamlit.app",  # Deployed Streamlit
        # "*"  # Or allow all for demo (less secure)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoints
@app.get("/")
def root():
    return {
        "message": "Assessment Grading API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


class QuestionInfo(BaseModel):
    id: str
    subject: str
    topic: str
    question: str

@app.get("/api/questions", response_model=List[QuestionInfo])
def list_questions():
    """Get list of available questions"""
    return [
        {
            "id": q["id"],
            "subject": q["subject"],
            "topic": q["topic"],
            "question": q["question"],
        }
        for q in QUESTIONS
    ]


@app.get("/api/questions/{question_id}")
def get_question(question_id: str):
    """Get details of a specific question including rubric"""
    matches = (q for q in QUESTIONS if q["id"] == question_id)
    question = next(matches, None)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    return question


# Request/Response models
class GradeRequest(BaseModel):
    question_text: str = Field(..., description="Full text of the question to grade", min_length=1)
    answer_text: str = Field(..., description="Student's answer text", min_length=1)

class _CriterionScore(BaseModel):
    criterion: str
    assigned_score: float
    justification: str

class GradeResponse(BaseModel):
    scores_by_criteria: List[_CriterionScore]


grader = _groq_client.GroqClient()

@app.post("/api/grade", response_model=GradeResponse)
async def grade_answer(request: GradeRequest):
    """Grade a student answer"""
    matches = (q for q in QUESTIONS if q["question"] == request.question_text)
    question = next(matches, None)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    try:
        result = grader.request(
            prompt_to_grade(
                request.answer_text,
                question["question"], 
                question["rubric"],
            ),
            temperature=1.5,
            output_schema="grading",
        )
        
        result["question_id"] = question["id"]
        result["question_text"] = question["question"]
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Grading error: {str(e)}")


# Run with: uvicorn main:app --reload