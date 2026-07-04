# Feature 14: Move-in / Move-out Inspection

## 1. Layman Guide
This feature provides a digital walkthrough checklist for move-in and move-out inspections. Users can document the condition of each room and upload photos to establish a clear deposit baseline.

---

## 2. Technical Guide
* **Offline Storage**: The Next.js frontend buffers forms in local storage to support offline use during inspections.
* **Storage upload**: Saves checklist assets to the MinIO `inspections` bucket.

---

## 3. Step-by-Step Flow
1. **Checklist**: Inspector fills out item conditions on the app.
2. **Photos**: Attaches photo evidence for damaged items.
3. **Submit**: Form data is posted to MongoDB and assets are saved to MinIO.
4. **Sign-off**: Landlord and tenant receive inspection logs for electronic signature.

---

## 4. Data Schema
```json
{
  "_id": "ObjectId",
  "lease_id": "ObjectId",
  "inspection_type": "MOVE_IN | MOVE_OUT",
  "checklist": [
    { "room": "kitchen", "item": "stove", "condition": "good" }
  ],
  "photos": ["inspections/kitchen_stove.jpg"]
}
```

---

## 5. Edge Cases & Mitigations
* **Network failure mid-upload**: If the connection drops during upload, the local app retains the checklist data and retries the upload once connection is restored.
