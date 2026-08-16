# Feature 05: Smart Vector Lease Search

## Layman Guide
Lets tenants ask questions about their lease, returning exact clauses directly.

## Technical Guide
FastAPI extracts text chunks, embeds using Sentence Transformers, and searches Qdrant. Context is passed to LLM for final formulation.

## Flow
1. Tenant inputs query.
2. Backend embeds query.
3. Qdrant returns top K hits.
4. LLM parses hits and returns response.

## Data Schema
```json
{
  "query": "Can I have pets?",
  "matches": [{"chunk": "Pets allowed up to 25lbs", "score": 0.89}]
}
```

## Edge Cases
- **Out-of-context query**: Filter results below a similarity score (e.g. < 0.65) and report "Information not found in lease".
