# 09. AI Engine & Vector Search

The core reasoning capability of TenantMind AI relies on a resilient LLM selection framework coupled with a Qdrant Retrieval-Augmented Generation (RAG) vector repository.

## 1. RAG Ingestion Pipeline

1. **Document Upload**: Signed lease PDFs are uploaded through the FastAPI Backend to MinIO object storage.
2. **Text Extraction & Chunking**: Celery parses the document page-by-page, chunking text into overlapping paragraphs of approximately 500 characters.
3. **Embedding Generation**: Chunks are processed via the local `sentence-transformers/all-MiniLM-L6-v2` model:
   * **Dimensions**: 384.
   * **Payload Metadata**: Appended with `tenant_id`, `lease_id`, and `chunk_id`.
4. **Qdrant Storage**: Inserted into the `lease_documents` collection with a cosine similarity metric configuration.

---

## 2. Multi-Model LLM Fallback Architecture

To handle API rate limits and network outages, `ModelGateway` executes a sequential fallback chain:

```
[User Request]
      |
      v
  1. Gemini  ---(Success)---> [Return Result]
      | (Fail / No Key)
      v
  2. Groq    ---(Success)---> [Return Result]
      | (Fail / No Key)
      v
  3. OpenRouter --(Success)--> [Return Result]
      | (Fail / No Key)
      v
  4. Ollama  ---(Success)---> [Return Result]
      | (Fail / No Key)
      v
  5. Mock Fallback (System Resilience)
```

This guarantees that the user interface never crashes, even when third-party AI providers fail.

---

## 3. Query Execution Pattern

When a query is received:
1. Embed the search term (e.g., *"How much is late rent fee?"*).
2. Retrieve chunks from **Qdrant** applying a filter: `tenant_id == token.tenant_id`. This prevents cross-tenant document exposure.
3. Construct the prompt:
   ```
   System Prompt: Use the following lease context to answer the query. If the answer is not in the context, say "Information not found in lease."
   Context: [Retrieved Chunks]
   User Query: [Tenant Query]
   ```
4. Run through the `ModelGateway.generate()` pipeline and return the result.
