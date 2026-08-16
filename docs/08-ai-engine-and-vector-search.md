# 08. AI Engine & Vector Search

The AI system is powered by LLMs (Ollama, Gemini, Groq, OpenRouter) and Qdrant.

## Vector Search (RAG)
Lease documents are uploaded to MinIO, parsed, chunked, and embedded using `sentence-transformers`.
The embeddings are saved into Qdrant.
When a tenant asks a question about their lease, their query is embedded, and Qdrant retrieves relevant context chunks to build the prompt for the LLM.
