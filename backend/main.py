from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class MatchRequest(BaseModel):
    resume_text: str
    job_description: str

@app.get("/")
def root():
    return {"message": "FastAPI is running 🚀"}

@app.post("/match")
def match_resume(data: MatchRequest):
    return {
        "score": 85,
        "feedback": "Good match! Missing more Python experience."
    }
