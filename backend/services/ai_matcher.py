
from sentence_transformers import SentenceTransformer, util
import re

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')


def chunk_text(text, max_words=100):
    """
    Split text into chunks of approximately `max_words` words.
    Filters out very short chunks.
    """
    paragraphs = text.split("\n")
    chunks = []

    for para in paragraphs:
        para = para.strip()
        if len(para.split()) < 3:
            continue  # skip very short paragraphs
        words = para.split()
        for i in range(0, len(words), max_words):
            chunk = " ".join(words[i:i+max_words])
            chunks.append(chunk)
    return chunks


def match_resume_with_job(resume_text: str, job_description: str):
    # Chunk the resume
    chunks = chunk_text(resume_text)

    # Encode job description
    job_embedding = model.encode(job_description, convert_to_tensor=True)

    results = []
    for chunk in chunks:
        chunk_embedding = model.encode(chunk, convert_to_tensor=True)
        similarity = util.cos_sim(job_embedding, chunk_embedding).item()
        results.append({"chunk": chunk, "similarity": round(similarity, 2)})

    # Compute overall similarity as average
    overall_similarity = round(sum(r["similarity"] for r in results)/len(results), 2) if results else 0.0

    # Return top 5 chunks
    top_chunks = sorted(results, key=lambda x: x["similarity"], reverse=True)[:5]

    match_score = int(overall_similarity * 100)

    if match_score >= 80:
        summary = "Strong match with the job requirements"
    elif match_score >= 50:
        summary = "Partial match — some key skills are missing"
    else:
        summary = "Low match — significant gaps detected"

    return {
        "match_score": match_score,
        "summary": summary,
        "top_matches": top_chunks
    }
