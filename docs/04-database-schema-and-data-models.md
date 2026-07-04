# 04. Database Schema & Data Models

This document outlines the data schemas and relationships across MongoDB and Qdrant.

## MongoDB Collections
- `users`: Managed via Keycloak mapping; contains local profiles, roles, and preferences.
- `properties`: Property details, address, units, landlord references.
- `leases`: Lease terms, rent amounts, dates, and tenant IDs.
- `maintenance_tickets`: Title, description, priority, current state, and assigned vendor.
- `payments`: Transaction IDs, amounts, payment methods, status, and dates.

## Qdrant Collections
- `lease_documents`: Vector embeddings of parsed lease agreements for semantic RAG queries.
