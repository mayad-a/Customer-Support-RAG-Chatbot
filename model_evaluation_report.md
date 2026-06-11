# Model Evaluation Report — Milestone 2

## Pipeline Configuration
- Embedding model:  all-MiniLM-L6-v2 (384 dimensions)
- Vector store:     FAISS IndexFlatL2
- Generator:        Groq llama-3.1-8b-instant
- Retrieval k:      5 chunks
- Corpus size:      481 chunks (FAQs + Manuals + TP-Link Tickets)

## Evaluation Results
| Metric   | Score  | Status |
|----------|--------|--------|
| BLEU     | 0.202  | ✅ Good |
| ROUGE-1  | 0.427  | ✅ Good |
| ROUGE-2  | 0.258  | ✅ Good |
| ROUGE-L  | 0.417  | ✅ Good |
| Hit Rate | 100.0% | ✅ Good |

## Optimization Applied
- Switched from llama3-8b to llama-3.1-8b-instant for stability
- Retrieval k=5 chunks per query
- 2 second delay between requests for rate limit safety

## Conclusion
The RAG pipeline successfully retrieves relevant TP-Link
support content and generates accurate answers grounded
in the knowledge base corpus of 481 chunks.
