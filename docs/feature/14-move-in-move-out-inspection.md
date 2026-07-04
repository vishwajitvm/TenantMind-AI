# Feature 14: Move-in / Move-out Inspection

## Layman Guide
A digital checklist to document apartment condition at move-in/out.

## Technical Guide
Next.js supports offline form submissions. FastAPI commits checklists and uploads media arrays to MinIO.

## Flow
1. Agent completes checklist.
2. Uploads photos.
3. Generates digital inspection sign-off.

## Data Schema
```json
{
  "inspection_id": "uuid",
  "unit_id": "uuid",
  "checklist": [{"item": "kitchen_sink", "status": "EXCELLENT"}]
}
```

## Edge Cases
- **Offline upload sync conflict**: Use local storage metadata timestamp to resolve concurrent edits on the server.
