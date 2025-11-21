🚀 Mock Interview AI System
AI-Powered Smart Interviewer with Voice Interaction, Semantic Evaluation & Personalized Improvement Plan

This project is an end-to-end AI-driven Mock Interview System that evaluates candidates using:

Resume + JD–aware question generation

Voice-based interaction (TTS + STT)

Hybrid scoring model (LLM + Semantic Similarity + Missing Keyword Analysis)

Automated follow-up questions

Gap-focused Improvement Plan

It simulates a real interviewer and gives AI-based feedback, confidence score, and personalized improvement roadmap.

✨ Features
🧾 1. Resume & Job Description Parsing

Upload Resume (PDF)

Upload Job Description (PDF)

Extract text using Fitz (PyMuPDF)

Parse into structured JSON using Groq LLM

🔥 2. AI-Generated Interview Questions

Groq LLM generates N contextual questions

Questions include:

Technical

Behavioral

Resume-based

JD requirement based

🔊 3. Text-to-Speech (TTS)

Converts each question into audio

Uses Google gTTS (free)

Autoplay in browser

🎤 4. Speech-to-Text (STT)

User answers by speaking

Audio → Whisper → Transcript

Whisper is local → free

🧠 5. Hybrid Answer Evaluation

Each answer is scored using:

Component	Description
LLM Evaluation	Rates correctness, keywords, reasoning, clarity
Semantic Similarity	Compares transcript vs ideal answer using MPNet embeddings
Keyword Check	Measures missing JD/resume keywords
Follow-up logic	Auto-triggered if low score or missing key concepts
💬 6. Follow-Up Question Generation

LLM generates follow-up question based on user weaknesses

Up to 3 follow-ups per question

📊 7. Session Tracking

For entire interview, system stores:

Questions asked

Answers (text)

Evaluation scores

Weaknesses

Semantic confidence

📘 8. Improvement Plan

LLM generates a personalized improvement report:

Summary of strengths & weaknesses

Skill gaps (resume vs JD)

Recommended exercises

Resources (videos, books, articles)

🏗️ System Architecture
                   ┌─────────────────────┐
                   │   Resume (PDF)      │
                   └─────────┬───────────┘
                             │
                   ┌─────────────────────┐
                   │  JD (PDF)           │
                   └─────────┬───────────┘
                             ▼
                    ┌───────────────────┐
                    │  Fitz PDF Extract │
                    └─────────┬─────────┘
                              ▼
                       ┌────────────┐
                       │  Groq LLM  │
                       │ Parsing    │
                       └─────┬──────┘
                             ▼
                ┌──────────────────────────┐
                │ Question Generation LLM  │
                └──────────┬──────────────┘
                           ▼
                ┌──────────────────────────┐
                │  Google TTS (gTTS)       │
                └──────────┬──────────────┘
                           ▼
                      User Listens
                           ▼
                   User Speaks Answer
                           ▼
                 ┌────────────────────┐
                 │ Whisper STT        │
                 └─────────┬──────────┘
                           ▼
      ┌────────────────────────────────────────────────────┐
      │ Hybrid Evaluator                                   │
      │  • LLM scoring                                     │
      │  • Semantic similarity (MPNet)                     │
      │  • Keyword detection                               │
      │  • Follow-up question LLM                          │
      └───────────────────────┬────────────────────────────┘
                               ▼
                      Next Question / Follow-up
                               ▼
                    Final Improvement Plan (LLM)

🛠️ Tech Stack
Frontend

HTML

CSS

JavaScript

In-browser audio recording

Backend (FastAPI)

Python 3.10+

FastAPI

PyMuPDF (Fitz)

Groq API (LLM)

Google gTTS

Whisper (local)

SentenceTransformers

BERTScore (optional)

📁 Project Structure
mock_interview/
│── app/
│   ├── routes/
│   ├── services/
│   ├── prompts/
│   ├── main.py
│── frontend/
│   ├── index.html
│   ├── upload.html
│   ├── interview.html
│   ├── improvement.html
│   ├── style.css
│── venv/  (ignored)
│── .env   (ignored)
│── README.md
│── requirements.txt

⚙️ Installation
Clone repository
git clone <repo-url>
cd mock_interview

Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows

Install dependencies
pip install -r requirements.txt

Setup .env
GROQ_API_KEY=your_key

Run server
uvicorn app.main:app --reload

Open in browser
http://localhost:8000

🧪 API Endpoints (Backend)
1. Upload Files
POST /api/upload-docs

2. Start Interview
POST /api/start-interview

3. Get Next Question
POST /api/get-question

4. Submit Text Answer
POST /api/submit-answer

5. Submit Audio Answer
POST /api/submit-answer-audio

6. Generate Improvement Plan
POST /api/generate-improvement

🎥 Screenshots (Optional Section)

(Add your screenshots here)

📄 Resume / JD Upload Page  
🎤 Interview Mode  
📊 Evaluation View  
📘 Improvement Plan  

📌 Future Enhancements

Multi-persona interviewers

Emotional tone evaluation

Resume–JD gap analysis scoring

Real-time feedback

Adaptive difficulty questions

Dashboard with detailed analytics

LangGraph conversion for agentic behavior

👨‍💻 Authors

Guransh Singh
Abhishek Mittal
2025

⭐ Summary

This project provides:

Smart interview simulation

LLM-powered adaptive questioning

Voice-enabled interaction

Hybrid evaluation metrics

Rich improvement plan

It is fully functional, modular, and extensible.
