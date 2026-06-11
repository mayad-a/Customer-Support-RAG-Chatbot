
import faiss
import numpy as np
import json
import os
import traceback
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from groq import Groq

app = FastAPI(title="TP-Link RAG Support API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.environ.get("API_KEY", "dev-key-change-in-production")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(key: str = Depends(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return key

print("Loading models...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index(os.path.join(os.path.dirname(__file__), "vector_store.index"))
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY", "Your_API"))

chunks = []
with open(os.path.join(os.path.dirname(__file__), "corpus_final.jsonl")) as f:
    for line in f:
        chunks.append(json.loads(line))

print(f"Loaded {len(chunks)} chunks")

class AskRequest(BaseModel):
    question: str
    k: int = 5

class Source(BaseModel):
    text: str
    source_type: str
    score: float
    product: str

class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]
    chunks_used: int

def retrieve(query, k=5):
    vec = embedding_model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(vec, k)
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        c = chunks[idx]
        results.append({
            "text":     c["text"],
            "source":   c["source_type"],
            "metadata": c["metadata"],
            "score":    round(float(1 / (1 + dist)), 3)
        })
    return results

def generate(query, retrieved):
    context = "\n\n".join(
        "[Source " + str(i+1) + " | " + r["source"] + " | " + r["metadata"].get("product","") + "]\n" + r["text"]
        for i, r in enumerate(retrieved)
    )
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a TP-Link support assistant. Answer using ONLY the context. Be concise."
            },
            {
                "role": "user",
                "content": "Context:\n" + context + "\n\nQuestion: " + query + "\n\nAnswer:"
            }
        ],
        max_tokens=500
    )
    return response.choices[0].message.content

@app.get("/health")
def health():
    return {"status": "ok", "chunks": len(chunks), "version": "1.0.0"}

@app.get("/")
def root():
    return {"name": "TP-Link RAG Support API", "docs": "/docs"}

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest, api_key: str = Depends(verify_api_key)):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        retrieved = retrieve(request.question, k=request.k)
        answer    = generate(request.question, retrieved)
        sources   = [
            Source(
                text        = r["text"][:300],
                source_type = r["source"],
                score       = r["score"],
                product     = r["metadata"].get("product", "")
            )
            for r in retrieved
        ]
        return AskResponse(
            question     = request.question,
            answer       = answer,
            sources      = sources,
            chunks_used  = len(retrieved)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e) + " | " + traceback.format_exc())
