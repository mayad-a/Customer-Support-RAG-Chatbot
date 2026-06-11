# TP-Link Customer Support RAG Chatbot 🤖

This repository contains the production-ready FastAPI backend for an intelligent customer support chatbot trained on TP-Link product manuals, FAQs, and support tickets.

🚀 **Live API Demo (Swagger UI):** [https://mayada10-tplink-support-rag-api.hf.space/docs](https://mayada10-tplink-support-rag-api.hf.space/docs)

---

## 🌟 Features
- **100% Hit Rate** during evaluation on our Golden Test Set.
- **RAG Architecture** powered by `all-MiniLM-L6-v2` and `FAISS` for semantic search.
- **LLM Generation** via Groq (`llama-3.1-8b-instant`).
- **Production Ready** with Docker, FastAPI, and automated health checks.

---

## ⚙️ API Endpoints

- **`GET /docs`**: Interactive Swagger UI documentation (for live testing).
- **`POST /ask`**: Main RAG endpoint. Sends a support question and returns a grounded answer with its metadata sources.
- **`GET /health`**: API health check tracking indexing status and uptime safety.

---

## 📂 Project Structure
- `main.py`: Core API deployment code.
- `Dockerfile`: Container infrastructure configuration.
- `requirements.txt`: Locked Python dependencies.
- `startup.sh`: Automatic server deployment script.
- `corpus_final.jsonl`: Cleaned text chunks dataset (481 entries).
- `model_evaluation_report.md`: Milestone 2 evaluation results (ROUGE & BLEU scores).

---

## 🛠️ How to run locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
