# Feature 05: Smart Vector Lease Search

## 1. Layman Guide
This feature allows tenants to query lease agreements in natural language (e.g. *"Am I responsible for cleaning gutters?"*). The system instantly searches the agreement and shows the exact clause.

---

## 2. Technical Guide
* **Vectorizing**: Queries are embedded using `sentence-transformers/all-MiniLM-L6-v2`.
* **Searching**: Queries the Qdrant database using tenant filtering criteria to limit the search scope to the user's own lease records.
* **LLM Formulation**: Fetches matching context clauses, inserts them into the prompt template, and sends them to the Model Gateway.

---

## 3. Step-by-Step Flow
1. **Query**: Tenant asks: *"Can I have a cat?"*
2. **Embed**: Backend translates query into a vector representation.
3. **Filter**: Qdrant executes cosine search filtering by `tenant_id`.
4. **Respond**: Model Gateway drafts the answer using retrieved context clauses.

---

## 4. Data Schema
```json
{
  "query_vector": [0.015, -0.082, "..."],
  "filter": {
    "tenant_id": "tenant-uuid-1"
  },
  "qdrant_matches": [
    {
      "chunk_text": "Section 12: Pets under 25lbs are allowed.",
      "score": 0.89
    }
  ]
}
```

---

## 5. Edge Cases & Mitigations
* **Malicious context injection**: If a user attempts to feed instructions asking the system to override policies, the strict system prompt rules enforce strict bounds to prevent unauthorized responses.
