# Feature 09: Tenant Screening & Background Check

## Layman Guide
Checks criminal, credit, and eviction reports of applicants.

## Technical Guide
FastAPI integrates third-party APIs (e.g. Checkr / TransUnion). Reports saved under encrypted MongoDB collections.

## Flow
1. Applicant authorizes screening.
2. Backend requests background check API.
3. Webhook updates database with report URL.

## Data Schema
```json
{
  "screening_id": "uuid",
  "applicant_id": "uuid",
  "score": 750,
  "verdict": "APPROVED"
}
```

## Edge Cases
- **Incorrect SSN/identity mismatch**: Flag the report for manual review, preventing auto-rejection.
