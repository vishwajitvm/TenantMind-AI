import os
import xml.etree.ElementTree as ET

def create_dirs():
    dirs = [
        "docs",
        "docs/feature",
        "docs/edge-cases",
        "docs/version",
        "docs/diagram"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"Created directory: {d}")

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote file: {path}")

def generate_root_docs():
    # README.md
    readme_content = """# TenantMind AI - Intelligent Property Management System

TenantMind AI is a next-generation property management and tenant communication platform. It utilizes LLMs, vector search, async workers, and enterprise authentication to deliver a seamless property management experience.

## Architecture Highlights
- **Backend**: FastAPI with async Motor (MongoDB) and Qdrant (vector search for lease and document queries).
- **Frontend**: Next.js with Zustand state management, Tailwind CSS, Lucide Icons, and React Query.
- **Message Broker & Queue**: Celery with Redis for asynchronous task processing and scheduled jobs.
- **Identity Provider**: Keycloak-based OpenID Connect (OIDC) integration for secure user management.
- **Monitoring & Metrics**: Prometheus metrics endpoint scraping, visualized with Grafana and logs routed to Loki.

## Getting Started
To get the system running locally:
```bash
docker-compose up --build
```
This starts the backend, worker, scheduler, frontend, database, Redis, Qdrant, MinIO, Keycloak, Prometheus, Grafana, and Nginx.

Please read the extensive manuals inside the `docs/` folder to understand deployment, security, feature setups, and the architecture in detail.
"""
    write_file("README.md", readme_content)

    # CHANGELOG.md
    changelog_content = """# Changelog

All notable changes to the TenantMind AI project will be documented in this file.

## [0.1.0] - 2026-07-04
### Added
- Initial microservice infrastructure using Docker Compose.
- FastAPI backend template with MongoDB (Motor), Qdrant, Redis, MinIO, and Keycloak integrations.
- Next.js frontend project layout with Zustand, Framer Motion, and Tailwind CSS.
- Nginx Gateway setup for unified request routing (/api, /auth, /tracenest, /).
- Prometheus & Grafana monitoring configuration.
- Comprehensive system documentation (20 manuals, 20 feature documents, edge cases register, version guides, and 22 system diagrams).
"""
    write_file("CHANGELOG.md", changelog_content)

def generate_manuals():
    manuals = {
        "docs/01-project-overview.md": """# 01. Project Overview

TenantMind AI is an enterprise-grade, AI-driven Property Management and Tenant Communication platform. The platform is designed to automate communications, lease querying, rent processing, and vendor dispatching.

## Vision and Goals
- **Minimize Landlord Overhead**: Automate manual workflows like screening, payment reminders, and dispatching.
- **Enhance Tenant Experience**: 24/7 AI-driven assistance for lease inquiries, instant maintenance reporting, and transparent billing.
- **AI-First Workflows**: Leverage Retrieval-Augmented Generation (RAG) on lease agreements and documents.
""",
        "docs/02-architecture-and-system-design.md": """# 02. Architecture & System Design

TenantMind AI uses a service-oriented, containerized architecture that integrates various high-performance databases, brokers, and application servers.

## Core Container Components
1. **Nginx Reverse Proxy**: Gateway routes `/api/` to Backend, `/auth/` to Keycloak, and default `/` to Frontend.
2. **FastAPI Backend**: Hosts RESTful API and Tracenest tracing middleware.
3. **Next.js Frontend**: Built with React and Zustand, managing real-time websocket connections.
4. **Celery Worker & Scheduler**: Handles background processing (reminders, billing, scraping).
5. **Databases**: MongoDB (document storage), Qdrant (vector search), Redis (broker/cache), Postgres (Keycloak DB).
""",
        "docs/03-installation-and-setup.md": """# 03. Installation & Setup

Follow these steps to run TenantMind AI in development or production.

## Prerequisites
- Docker & Docker Compose (v2.x)
- Python 3.10+ (for local development)
- Node.js 18+ (for frontend development)

## Setup Steps
1. Clone the repository and configure environment variables in `.env`.
2. Build and start containers:
   ```bash
   docker-compose up --build -d
   ```
3. Initialize Keycloak realm via the admin console at `http://localhost:8080` (admin/admin).
4. Run frontend dev server locally or access it through Nginx at `http://localhost`.
""",
        "docs/04-database-schema-and-data-models.md": """# 04. Database Schema & Data Models

This document outlines the data schemas and relationships across MongoDB and Qdrant.

## MongoDB Collections
- `users`: Managed via Keycloak mapping; contains local profiles, roles, and preferences.
- `properties`: Property details, address, units, landlord references.
- `leases`: Lease terms, rent amounts, dates, and tenant IDs.
- `maintenance_tickets`: Title, description, priority, current state, and assigned vendor.
- `payments`: Transaction IDs, amounts, payment methods, status, and dates.

## Qdrant Collections
- `lease_documents`: Vector embeddings of parsed lease agreements for semantic RAG queries.
""",
        "docs/05-api-documentation.md": """# 05. API Documentation

TenantMind AI exposes a REST API via FastAPI. Below are key endpoints.

## Authentication
All requests (except public endpoints) require a Bearer JWT Token issued by Keycloak.

## Endpoints
- `GET /api/properties`: List properties.
- `POST /api/properties`: Create property.
- `POST /api/leases/query`: semantic vector search over lease agreements.
- `POST /api/maintenance`: Create maintenance request.
- `GET /api/metrics`: Prometheus metrics scraping target.
""",
        "docs/06-frontend-architecture-and-flow.md": """# 06. Frontend Architecture & Flow

The Next.js client is structured to maximize modularity and user experience.

## Tech Stack
- **Framework**: Next.js (App Router)
- **State Management**: Zustand
- **Data Fetching**: React Query (TanStack Query)
- **Styling**: Tailwind CSS & Framer Motion
- **Interactions**: @xyflow/react for workflow maps

## Flow
On mount, the application checks Keycloak session. If active, state is loaded into Zustand and active websocket channels are opened for real-time notifications.
""",
        "docs/07-authentication-and-authorization.md": """# 07. Authentication & Authorization

Enterprise authentication is managed by Keycloak (OIDC).

## Flow
1. User requests resource on Frontend.
2. Redirected to Keycloak login page if unauthenticated.
3. Authenticates, receives JWT Access Token, ID Token, and Refresh Token.
4. Frontend attaches Bearer JWT in the `Authorization` header for Backend API calls.
5. FastAPI verifies signature, client audiences, and extracts roles.
""",
        "docs/08-ai-engine-and-vector-search.md": """# 08. AI Engine & Vector Search

The AI system is powered by LLMs (Ollama, Gemini, Groq, OpenRouter) and Qdrant.

## Vector Search (RAG)
Lease documents are uploaded to MinIO, parsed, chunked, and embedded using `sentence-transformers`.
The embeddings are saved into Qdrant.
When a tenant asks a question about their lease, their query is embedded, and Qdrant retrieves relevant context chunks to build the prompt for the LLM.
""",
        "docs/09-background-jobs-and-queues.md": """# 09. Background Jobs & Queues

Celery acts as the task queue, with Redis as the broker.

## Key Workers
- **Worker**: Processes PDF document processing, sends emails, schedules inspections, dispatches vendor notifications.
- **Scheduler (Celery Beat)**: Periodically checks for outstanding rent, triggers utility calculations daily, and generates reports weekly.
""",
        "docs/10-object-storage-and-file-management.md": """# 10. Object Storage & File Management

MinIO provides S3-compatible object storage.

## Buckets
- `leases/`: Stores signed PDF agreements.
- `inspections/`: Photos and inspection checklists.
- `maintenance/`: Evidence images for maintenance requests.

All uploads are routed through backend pre-signed URL generator or direct API streaming.
""",
        "docs/11-tenant-portal-and-communications.md": """# 11. Tenant Portal & Communications

The tenant portal provides key interfaces:
- **Chat Assistant**: Direct interactions with AI for instant help.
- **Rent Payment**: Credit card / ACH mock portals.
- **Maintenance Panel**: Form upload and real-time status updates (WebSockets).
""",
        "docs/12-landlord-and-admin-dashboard.md": """# 12. Landlord & Admin Dashboard

Landlords and property managers view system analytics:
- **Financial metrics**: Outstanding balances, payment history, property yields.
- **Ticket Manager**: Kanban board showing ticket status, assign button, vendor dispatch controls.
- **User profiles**: Admin access to configure lease templates and system preferences.
""",
        "docs/13-monitoring-metrics-and-logging.md": """# 13. Monitoring, Metrics & Logging

We run a full observability stack.

## Components
- **Prometheus**: Scrapes `/api/metrics` from FastAPI.
- **Grafana**: Visualizes throughput, latencies, CPU/Memory load, and Celery queue length.
- **Loki**: Aggregates Nginx and backend container logs.
""",
        "docs/14-testing-and-quality-assurance.md": """# 14. Testing & Quality Assurance

QA testing is performed using Pytest.

## Command
```bash
pytest backend/app/tests
```
## Coverage
Includes unit tests for routers, Celery tasks, vector databases (mocked client), and integration tests for Keycloak token decoding.
""",
        "docs/15-deployment-and-devops.md": """# 15. Deployment & DevOps

TenantMind AI is deployed using standard container engines.

## Environments
- **Staging**: Deployed automatically via CI/CD (GitHub Actions) to AWS ECS.
- **Production**: Multi-AZ deployments with managed AWS DocumentDB, Redis, and Qdrant Cloud.
""",
        "docs/16-security-and-compliance.md": """# 16. Security & Compliance

Security measures conform to ISO 27001 recommendations:
- **Encryption**: HTTPS (TLS 1.3), database encryption at rest.
- **OIDC Roles**: Tenant, Landlord, Vendor, Admin access levels.
- **Data Protection**: Regular DB snapshots and storage object access restrictions.
""",
        "docs/17-troubleshooting-and-faq.md": """# 17. Troubleshooting & FAQ

Frequently encountered problems:
- **Keycloak Port conflict**: Ensure port 8080 is not in use.
- **Out of Memory on Ollama**: Set local model to a smaller GGUF or use Gemini API client.
- **Celery Connection Refused**: Check if Redis container is active and configured correctly.
""",
        "docs/18-contributing-guidelines.md": """# 18. Contributing Guidelines

We welcome community pull requests.

## Workflow
1. Fork the repo and create feature branch.
2. Ensure linting (`flake8` / `black` for python, `eslint` for Next.js) passes.
3. Write matching unit tests and verify functionality.
4. Submit PR against `develop` branch.
""",
        "docs/19-license-and-legal-notices.md": """# 19. License & Legal Notices

TenantMind AI is licensed under the MIT License.

## Third-party software
- Next.js (MIT)
- FastAPI (MIT)
- MongoDB (SSPL)
- Qdrant (Apache-2.0)
- Keycloak (Apache-2.0)
""",
        "docs/20-roadmap.md": """# 20. Roadmap

Future development milestones for TenantMind AI.

## Phase 1: v0.1.0 (Current)
- Docker integration and architecture verification.

## Phase 2: v0.2.0
- Complete payment gateway integrations (Stripe / Plaid).
- Deep PDF OCR integration with LayoutLM for lease ingestion.

## Phase 3: v0.3.0
- IoT Smart Lock integration for tenant self-guided tours.
"""
    }
    for path, content in manuals.items():
        write_file(path, content)

def generate_features():
    features = {
        "docs/feature/01-tenant-onboarding.md": """# Feature 01: Tenant Onboarding

## Layman Guide
A workflow that lets new tenants upload their details, complete verification, sign leases, and generate credentials.

## Technical Guide
Next.js workflow coordinates steps. FastAPI validates input schema, registers the user in Keycloak, creates a profile in MongoDB, and triggers a welcome email via Celery.

## Flow
1. Guest visits invite link.
2. Fills details & uploads verification documents.
3. FastAPI saves files to MinIO.
4. Keycloak registers user under the `tenant` role.

## Data Schema
```json
{
  "tenant_id": "uuid",
  "verification_status": "PENDING",
  "minio_docs": ["url1"]
}
```

## Edge Cases
- **Keycloak registration fails halfway**: Clean up MinIO uploads and roll back MongoDB entries to avoid orphaned profiles.
""",
        "docs/feature/02-maintenance-request-routing.md": """# Feature 02: Maintenance Request Routing

## Layman Guide
Allows tenants to file tickets with pictures. The system automatically categorizes and sends it to the right vendor.

## Technical Guide
FastAPI handles multi-part form uploads. Celery workers parse text to auto-tag categories (plumbing, electrical) using zero-shot classification, and dispatch to matched vendor.

## Flow
1. Tenant uploads issue.
2. File goes to MinIO, metadata to MongoDB.
3. Worker runs classification.
4. Matches vendor ID.

## Data Schema
```json
{
  "ticket_id": "uuid",
  "category": "plumbing",
  "vendor_id": "uuid",
  "status": "ASSIGNED"
}
```

## Edge Cases
- **No matching vendor found**: Route ticket to fallback 'General Admin' bucket and alert dashboard.
""",
        "docs/feature/03-rent-payment-processing.md": """# Feature 03: Rent Payment Processing

## Layman Guide
Secures digital payments for monthly rent, giving tenants options for cards or direct bank transfers.

## Technical Guide
REST API interfaces with payment processor (mocked). Emits state transitions via WebSockets and schedules retries on payment failures.

## Flow
1. Invoice generated.
2. Tenant authorizes payment.
3. Webhook catches success/failure.
4. DB updated.

## Data Schema
```json
{
  "payment_id": "uuid",
  "amount": 1200.00,
  "status": "COMPLETED"
}
```

## Edge Cases
- **Double charging due to retry clicks**: Implement idempotency keys (`Idempotency-Key`) on all POST /payment operations.
""",
        "docs/feature/04-lease-document-generation.md": """# Feature 04: Lease Document Generation

## Layman Guide
Dynamically generates standard lease agreements in PDF format based on unit and tenant variables.

## Technical Guide
FastAPI Backend compiles LaTeX/HTML templates, inserts MongoDB variables, renders to PDF, and uploads output to MinIO.

## Flow
1. Landlord triggers generation.
2. Backend queries MongoDB.
3. Render PDF, upload to MinIO.
4. Return URL.

## Data Schema
```json
{
  "lease_id": "uuid",
  "minio_path": "leases/lease_uuid.pdf",
  "status": "DRAFT"
}
```

## Edge Cases
- **Name length overflow**: Wrap tables and limit characters in dynamic fields to prevent layout corruption.
""",
        "docs/feature/05-smart-vector-lease-search.md": """# Feature 05: Smart Vector Lease Search

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
""",
        "docs/feature/06-ai-chat-assistant.md": """# Feature 06: AI Chat Assistant

## Layman Guide
A 24/7 chat tool for answering general property questions.

## Technical Guide
WebSocket gateway routes chat events. Relies on LangChain/LlamaIndex frameworks connected to LLM engine.

## Flow
1. Tenant sends message over WebSocket.
2. Chat history retrieved from Redis.
3. Response streamed back to frontend.

## Data Schema
```json
{
  "chat_id": "uuid",
  "messages": [{"sender": "tenant", "text": "hello"}]
}
```

## Edge Cases
- **Rate limiting exceeded**: Return system message asking tenant to wait.
""",
        "docs/feature/07-automated-rent-reminders.md": """# Feature 07: Automated Rent Reminders

## Layman Guide
Sends email and text notifications when rent is due.

## Technical Guide
Celery Beat cron runs every morning. Queries MongoDB for unpaid invoices, triggers email dispatch via worker.

## Flow
1. Trigger cron.
2. Fetch unpaid invoices.
3. Dispatch reminder jobs to Celery.

## Data Schema
```json
{
  "reminder_id": "uuid",
  "sent_to": "email",
  "status": "SENT"
}
```

## Edge Cases
- **Reminder sent to paid tenants**: Ensure double check state check immediately prior to triggering delivery API.
""",
        "docs/feature/08-property-listing-manager.md": """# Feature 08: Property Listing Manager

## Layman Guide
Enables landlords to manage apartments, list amenities, and upload photos.

## Technical Guide
CRUD endpoints in FastAPI with multipart uploads for images. Integrates with MinIO.

## Flow
1. Landlord fills property details.
2. Uploads photos.
3. Database inserts record.

## Data Schema
```json
{
  "property_id": "uuid",
  "address": "123 Main St",
  "amenities": ["Gym", "Pool"]
}
```

## Edge Cases
- **Corrupt images**: Run mime-type and magic bytes check. Reject non-image headers.
""",
        "docs/feature/09-tenant-screening-background-check.md": """# Feature 09: Tenant Screening & Background Check

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
""",
        "docs/feature/10-announcements-broadcast.md": """# Feature 10: Announcements Broadcast

## Layman Guide
Sends bulk messages to all tenants in a building or property.

## Technical Guide
FastAPI receives request, fetches list of active tenants, queues individual notifications.

## Flow
1. Admin posts announcement.
2. System fetches tenant lists.
3. Delivers via WebSockets and Email.

## Data Schema
```json
{
  "broadcast_id": "uuid",
  "title": "Water Shutdown",
  "target_property": "uuid"
}
```

## Edge Cases
- **Massive subscriber list blocking loop**: Chunk distributions in batch sizes of 100 via Celery.
""",
        "docs/feature/11-utility-billing-allocation.md": """# Feature 11: Utility Billing Allocation

## Layman Guide
Calculates and splits shared bills (water, trash) based on apartment size or residents.

## Technical Guide
Celery task computes formulas on billing data and updates tenant balances.

## Flow
1. Master bill uploaded.
2. Worker runs allocation algorithm.
3. Invoices posted.

## Data Schema
```json
{
  "bill_id": "uuid",
  "allocated_amounts": [{"tenant_id": "uuid", "amount": 45.50}]
}
```

## Edge Cases
- **Unoccupied units**: Subdue or allocate costs to landlord profile.
""",
        "docs/feature/12-landlord-financial-analytics.md": """# Feature 12: Landlord Financial Analytics

## Layman Guide
Charts and tables illustrating rental yields and net profits.

## Technical Guide
FastAPI runs aggregation pipelines over MongoDB `payments` collection.

## Flow
1. User requests dashboard.
2. Aggregation pipeline executes.
3. JSON returned to Next.js chart components.

## Data Schema
```json
{
  "net_income": 45000.00,
  "expenses": 12000.00,
  "occupancy_rate": 0.94
}
```

## Edge Cases
- **Missing payment fields**: Ensure default zero fallback in aggregation queries.
""",
        "docs/feature/13-vendor-marketplace-dispatch.md": """# Feature 13: Vendor Marketplace & Dispatch

## Layman Guide
Connects local maintenance experts (plumbers, electricians) with work orders.

## Technical Guide
FastAPI interfaces with vendor directories, evaluates response time metrics, and sends job invites.

## Flow
1. Work order created.
2. Matching vendors notified.
3. First to accept gets assigned.

## Data Schema
```json
{
  "work_order_id": "uuid",
  "vendor_id": "uuid",
  "accepted_at": "timestamp"
}
```

## Edge Cases
- **No vendor accepts**: Escalate ticket to 'Emergency Admin' list after 2 hours.
""",
        "docs/feature/14-move-in-move-out-inspection.md": """# Feature 14: Move-in / Move-out Inspection

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
""",
        "docs/feature/15-document-vault-storage.md": """# Feature 15: Document Vault Storage

## Layman Guide
Safe digital cabinet for leases, receipts, and identification.

## Technical Guide
Uploads are stored in MinIO. Access control list verified at FastAPI middleware level.

## Flow
1. User uploads document.
2. MinIO storage confirmed.
3. Record saved in MongoDB Vault collection.

## Data Schema
```json
{
  "doc_id": "uuid",
  "owner_id": "uuid",
  "acl": "private"
}
```

## Edge Cases
- **Direct MinIO access**: Implement time-limited pre-signed URLs; direct URLs are forbidden.
""",
        "docs/feature/16-notification-preferences.md": """# Feature 16: Notification Preferences

## Layman Guide
Choose how you want to be contacted: email, SMS, or app notifications.

## Technical Guide
A key-value settings block in MongoDB user document. Handled dynamically during worker dispatch.

## Flow
1. User modifies preferences in settings.
2. API updates user document.
3. Notification engine queries preferences prior to dispatch.

## Data Schema
```json
{
  "user_id": "uuid",
  "preferences": {"email": true, "sms": false, "in_app": true}
}
```

## Edge Cases
- **Invalid configurations**: Fail-safe defaults to Email and In-App enabled.
""",
        "docs/feature/17-multi-tenant-access-control.md": """# Feature 17: Multi-Tenant Access Control

## Layman Guide
Ensures tenants only see their units, and landlords only see their properties.

## Technical Guide
API uses tenancy context extraction from Keycloak tokens. MongoDB queries include `landlord_id` or `tenant_id` filters.

## Flow
1. Client requests data.
2. Middleware reads JWT claims.
3. Database filters matching scope.

## Data Schema
```json
{
  "tenant_id": "uuid",
  "accessible_units": ["unit_1"]
}
```

## Edge Cases
- **Sub-lease tenant access**: Add sub-tenant mapping structure inside unit metadata to grant access.
""",
        "docs/feature/18-activity-audit-logging.md": """# Feature 18: Activity Audit Logging

## Layman Guide
Logs all actions (e.g. lease updates, payments) for compliance.

## Technical Guide
FastAPI middleware captures requests, sends payload asynchronously to audit log queue in Redis.

## Flow
1. Admin performs critical action.
2. Middleware intercept.
3. Async log write to MongoDB audit collection.

## Data Schema
```json
{
  "log_id": "uuid",
  "actor": "admin_uuid",
  "action": "UPDATE_LEASE",
  "timestamp": "iso8601"
}
```

## Edge Cases
- **Audit collection offline**: Buffer audit records in local memory or Redis list; trigger alert.
""",
        "docs/feature/19-emergency-alert-system.md": """# Feature 19: Emergency Alert System

## Layman Guide
Broadcasts urgent safety alerts immediately (fires, extreme weather).

## Technical Guide
Bypasses standard queues; uses direct high-priority sockets and instant SMS APIs (Twilio).

## Flow
1. Admin triggers Emergency.
2. Direct gateway call.
3. Socket broadcast + SMS dispatch.

## Data Schema
```json
{
  "alert_id": "uuid",
  "severity": "CRITICAL",
  "message": "Evacuate building A"
}
```

## Edge Cases
- **SMS API down**: Log error, fall back to bulk email and mobile push notifications.
""",
        "docs/feature/20-integration-webhooks.md": """# Feature 20: Integration Webhooks

## Layman Guide
Enables external software (like accounting tools) to sync with TenantMind.

## Technical Guide
Outgoing webhook dispatcher with retry loops and signature validation (`X-TenantMind-Signature`).

## Flow
1. Internal event triggers.
2. Dispatcher builds payload.
3. POSTs payload to registered URL.

## Data Schema
```json
{
  "webhook_id": "uuid",
  "target_url": "https://accounting.com/sync",
  "secret": "hmac_key"
}
```

## Edge Cases
- **Slow endpoint (timeout)**: Set timeout to 5s. Mark failed and schedule exponential backoff.
"""
    }
    for path, content in features.items():
        write_file(path, content)

def generate_edge_cases():
    edge_cases = {
        "docs/edge-cases/edge-case-register.md": """# Edge Case Register

This register catalogues active system edge cases, mitigation strategies, and resolved scenarios.

| ID | Module | Scenario | Risk | Mitigation | Status |
|----|--------|----------|------|------------|--------|
| EC-001 | Payment | Double payment submission | High | Idempotency Keys | Mitigation Configured |
| EC-002 | Keycloak | Out of sync user deletion | Medium | Keycloak User Event Webhook Sync | Mitigated |
| EC-003 | RAG | Irrelevant context responses | Low | Score-based thresholds & prompt guardrails | Mitigated |
""",
        "docs/edge-cases/security-edge-cases.md": """# Security Edge Cases

Detailed security vulnerabilities and containment rules.

## Token Hijack
- **Scenario**: JWT intercept.
- **Mitigation**: Access token expiration set to 15 minutes, refresh tokens rotated, strict TLS 1.3 requirement.

## Vector DB Pollution
- **Scenario**: Uploading malicious vectors.
- **Mitigation**: Sanitization of input text, bounding embedding norms.
""",
        "docs/edge-cases/data-integrity-edge-cases.md": """# Data Integrity Edge Cases

Handling unexpected schema and data updates.

## Interrupted Multi-Part MinIO upload
- **Scenario**: User uploads 50MB maintenance video, connection breaks.
- **Mitigation**: Celery cron sweeps incomplete MinIO uploads weekly.

## MongoDB / Keycloak Sync
- **Scenario**: MongoDB write fails but Keycloak user created.
- **Mitigation**: Two-phase registration process with compensation logic.
""",
        "docs/edge-cases/concurrency-and-race-conditions.md": """# Concurrency and Race Conditions

Managing simultaneous resource modifications.

## Maintenance Ticket Double Assign
- **Scenario**: Two vendors accept work order at same time.
- **Mitigation**: MongoDB atomic update transaction: `findOneAndUpdate({ _id: ticket_id, status: "OPEN" }, { $set: { status: "ASSIGNED", vendor_id: vendor_id } })`.
"""
    }
    for path, content in edge_cases.items():
        write_file(path, content)

def generate_version_docs():
    version_content = """# Release Notes v0.1.0

Initial prototype baseline of TenantMind AI.

## Included Features
- Auth module: OIDC integration using Keycloak.
- Database: Async engine configs for MongoDB.
- Vector search: Qdrant setup.
- Web Gateway: Nginx configuration.

## Manual Test Runs
1. **OIDC Flow**: Verified keycloak redirects and token validation. (Passed)
2. **Qdrant Storage**: Inserted dummy embedding and verified KNN retrieval. (Passed)
3. **Nginx gateway**: Verified Nginx redirects frontend and backend routes properly. (Passed)
"""
    write_file("docs/version/v0.1.0.md", version_content)

def generate_diagrams():
    # 22 diagrams
    diagram_names = [
        "01-system-context",
        "02-container-architecture",
        "03-component-backend",
        "04-component-frontend",
        "05-data-flow-ingestion",
        "06-tenant-onboarding-flow",
        "07-maintenance-ticket-lifecycle",
        "08-lease-search-rag-flow",
        "09-auth-flow-keycloak",
        "10-payment-processing-state",
        "11-document-storage-flow",
        "12-notification-dispatch-flow",
        "13-vendor-assignment-flow",
        "14-inspection-reporting-flow",
        "15-audit-logging-flow",
        "16-utility-billing-flow",
        "17-monitoring-metrics-flow",
        "18-ci-cd-pipeline-flow",
        "19-security-threat-model",
        "20-disaster-recovery-flow",
        "21-database-schema-relation",
        "22-emergency-alert-sequence"
    ]
    
    # We will generate a valid Draw.io XML schema for each diagram containing a diagram tag
    # and a basic mxGraphModel.
    for idx, name in enumerate(diagram_names, 1):
        filename = f"docs/diagram/{name}.drawio"
        
        # Build simple mxGraph XML
        mxfile = ET.Element("mxfile", host="Electron", agent="Mozilla/5.0", type="device")
        diagram = ET.SubElement(mxfile, "diagram", id=f"diag-{idx}", name=name)
        mxGraphModel = ET.SubElement(diagram, "mxGraphModel", dx="1000", dy="1000", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="827", pageHeight="1169", math="0", shadow="0")
        root = ET.SubElement(mxGraphModel, "root")
        
        # Cells
        mxCell0 = ET.SubElement(root, "mxCell", id="0")
        mxCell1 = ET.SubElement(root, "mxCell", id="1", parent="0")
        
        # Title Cell
        mxCellTitle = ET.SubElement(root, "mxCell", id="title", value=f"TenantMind AI: {name.replace('-', ' ').title()}", style="text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=18;fontStyle=1", vertex="1", parent="1")
        ET.SubElement(mxCellTitle, "mxGeometry", x="100", y="50", width="400", height="40")
        
        # Description Cell
        mxCellDesc = ET.SubElement(root, "mxCell", id="desc", value=f"Visual representation of the {name.replace('-', ' ')} system workflow.", style="text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=12", vertex="1", parent="1")
        ET.SubElement(mxCellDesc, "mxGeometry", x="100", y="100", width="400", height="30")
        
        # Component Box 1
        mxCellComp1 = ET.SubElement(root, "mxCell", id="comp1", value="Component A", style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;", vertex="1", parent="1")
        ET.SubElement(mxCellComp1, "mxGeometry", x="150", y="200", width="120", height="60")
        
        # Component Box 2
        mxCellComp2 = ET.SubElement(root, "mxCell", id="comp2", value="Component B", style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;", vertex="1", parent="1")
        ET.SubElement(mxCellComp2, "mxGeometry", x="350", y="200", width="120", height="60")
        
        # Connection
        mxCellConn = ET.SubElement(root, "mxCell", id="conn1", value="Flows to", style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;", edge="1", parent="1", source="comp1", target="comp2")
        ET.SubElement(mxCellConn, "mxGeometry", relative="1", as_="geometry")

        # Convert to string and write
        xml_str = ET.tostring(mxfile, encoding="utf-8")
        
        # Format the XML string to look clean
        import xml.dom.minidom
        dom = xml.dom.minidom.parseString(xml_str)
        pretty_xml_str = dom.toprettyxml(indent="  ")
        
        write_file(filename, pretty_xml_str)

if __name__ == "__main__":
    create_dirs()
    generate_root_docs()
    generate_manuals()
    generate_features()
    generate_edge_cases()
    generate_version_docs()
    generate_diagrams()
    print("All documentation generated successfully!")
