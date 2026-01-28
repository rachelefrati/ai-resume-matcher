from file_parser import extract_text_from_pdf, extract_text_from_docx
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from services.ai_matcher import match_resume_with_job


app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/match-file")
async def match_file(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    # Step 1: extract text from file
    text = ""

    if resume_file.filename.endswith(".pdf"):
        file_bytes = await resume_file.read()
        text = extract_text_from_pdf(file_bytes)

    elif resume_file.filename.endswith(".docx"):
        file_bytes = await resume_file.read()
        text = extract_text_from_docx(file_bytes)

    else:
        return {"error": "Unsupported file type"}

    # Step 2: run AI matching logic
    result = match_resume_with_job(text, job_description)

    # Step 3: return result
    return result

@app.get("/")
def health():
    return {"status": "ok"}
