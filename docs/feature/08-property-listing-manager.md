# Feature 08: Property Listing Manager

## 1. Layman Guide
Landlords can create listings for vacant apartments, upload photos, list property amenities (such as a gym or pool), specify monthly rent, and publish them to find new tenants.

---

## 2. Technical Guide
* **REST APIs**: CRUD operations via `/api/properties`.
* **Image Processing**: Uploads images to the MinIO `inspections` bucket and runs optimization checks to compress file sizes.
* **Storage**: Keeps metadata records in MongoDB `properties`.

---

## 3. Step-by-Step Flow
1. **Form**: Landlord enters property details and uploads images.
2. **Upload**: API saves image binaries in MinIO.
3. **Database Write**: Backend inserts the property metadata and image references into MongoDB.
4. **Publish**: The system updates the listing status to `active`.

---

## 4. Data Schema
```json
{
  "_id": "ObjectId",
  "name": "Oakridge Apartments",
  "address": {
    "street": "100 Oak Rd",
    "city": "Austin",
    "state": "TX",
    "zip": "78701"
  },
  "amenities": ["Pool", "Gym", "Garage"],
  "images": ["inspections/oakridge_front.jpg"],
  "status": "active"
}
```

---

## 5. Edge Cases & Mitigations
* **Corrupt file uploads**: The API runs mime-type validations on incoming file streams, rejecting files with headers that don't match safe image formats.
