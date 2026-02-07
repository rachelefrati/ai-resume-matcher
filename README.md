# AI Resume Matcher

An AI-powered web application that analyzes resumes and job descriptions to measure skill and content similarity, helping users understand how well a resume matches a specific role.

---

## 🚀 Project Goal

The goal of this project is to demonstrate how Natural Language Processing (NLP) and semantic similarity models can be used to compare resumes with job descriptions in a practical, real-world application.

This project was built as a full-stack application to showcase backend API development, AI model integration, and frontend interaction.

---

## ✨ Features

- Upload and analyze resumes (PDF / text)
- Compare resume content with a job description
- AI-based semantic similarity using sentence embeddings
- Chunked text processing for long documents
- Similarity score output
- Clean REST API built with FastAPI
- Simple frontend interface

---

## 🛠️ Tech Stack

**Backend**
- Python
- FastAPI
- Sentence Transformers (`all-MiniLM-L6-v2`)
- PyMuPDF
- Uvicorn

**Frontend**
- HTML
- CSS
- JavaScript

**AI / NLP**
- Sentence Embeddings
- Cosine Similarity

**Deployment**
- Railway.app

---

## ⚙️ Setup Instructions (Local)

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-resume-matcher.git
   cd ai-resume-matcher