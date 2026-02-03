from sentence_transformers import SentenceTransformer, util
import re

# -----------------------------
# Lazy-loaded model (CRITICAL)
# -----------------------------
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


# -----------------------------
# Helpers
# -----------------------------
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
            continue

        words = para.split()
        for i in range(0, len(words), max_words):
            chunk = " ".join(words[i:i + max_words])
            chunks.append(chunk)

    return chunks


# -----------------------------
# Main matcher
# -----------------------------
def match_resume_with_job(resume_text: str, job_description: str):
    model = get_model()  # model loads ONLY when this function is called

    chunks = chunk_text(resume_text)

    job_embedding = model.encode(job_description, convert_to_tensor=True)

    results = []

    for chunk in chunks:
        chunk_embedding = model.encode(chunk, convert_to_tensor=True)
        similarity = util.cos_sim(job_embedding, chunk_embedding).item()
        clean_chunk = re.sub(r"\s+", " ", chunk).strip()

        if len(clean_chunk) > 40:
            results.append({
                "chunk": clean_chunk,
                "similarity": round(similarity, 2)
            })

    # Top chunks for scoring
    top_for_score = sorted(results, key=lambda x: x["similarity"], reverse=True)[:5]

    overall_similarity = (
        round(
            sum(r["similarity"] for r in top_for_score) / len(top_for_score),
            2
        )
        if top_for_score else 0.0
    )

    match_score = int(overall_similarity * 100)

    if match_score >= 80:
        summary = (
            "Strong match. Your resume aligns well with the job requirements, "
            "especially in the main technical areas. You appear to be a good fit for this role."
        )
    elif match_score >= 50:
        summary = (
            "Moderate match. Your resume shows relevant experience, but some important "
            "requirements are only partially covered. Strengthening the highlighted areas "
            "could improve your alignment with the role."
        )
    else:
        summary = (
            "Low match. While your resume includes some relevant skills, many core "
            "requirements of the role are not strongly reflected. Consider emphasizing "
            "more relevant experience or skills."
        )

    top_chunks = sorted(results, key=lambda x: x["similarity"], reverse=True)[:5]

    return {
        "match_score": match_score,
        "summary": summary,
        "top_matches": top_chunks
    }
