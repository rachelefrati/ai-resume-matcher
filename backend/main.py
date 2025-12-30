import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class MatchRequest(BaseModel):
    resume_text: str
    job_description: str


SKILLS = [
    "python", "java", "javascript", "react", "sql",
    "fastapi", "django", "html", "css", "git"
]

def extract_words(text: str):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return set(text.split())


@app.post("/match")
def match_resume(data: MatchRequest):
    resume_words = extract_words(data.resume_text)
    job_words = extract_words(data.job_description)

    job_skills = [s for s in SKILLS if s in job_words]
    resume_skills = [s for s in SKILLS if s in resume_words]

    matched = set(resume_skills) & set(job_skills)
    missing = list(set(job_skills) - set(resume_skills))

    score = int((len(matched) / max(len(job_skills), 1)) * 100)

    return {
        "score": score,
        "feedback": "Good match!" if score > 60 else "Needs improvement",
        "missing_skills": missing
    }
