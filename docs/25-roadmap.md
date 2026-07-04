# 25. Roadmap

This roadmap outlines the planned development path for TenantMind AI.

## Phase 1: Baseline Prototype (v0.1.0 - Current)
- [x] Multi-container Docker Compose setup.
- [x] FastAPI skeleton backend with Keycloak OIDC integration.
- [x] Next.js frontend with basic dashboard, chat interface, and Zustand.
- [x] Local RAG retrieval flow using Qdrant and Sentence Transformers.
- [x] Model fallback logic (Gemini -> Groq -> OpenRouter -> Ollama).
- [x] TraceNest request tracking and telemetry logging middleware.

## Phase 2: Core Enhancements (v0.2.0)
- [ ] Stripe ACH and credit card live gateway integration.
- [ ] Plaid bank verification workflow.
- [ ] Next-generation PDF processing using OCR (LayoutLM) to preserve formatting.
- [ ] Automated SMS notification integration using Twilio.
- [ ] Comprehensive offline form support in the Next.js PWA.

## Phase 3: Enterprise Integration (v0.3.0)
- [ ] Smart IoT integrations (e.g. self-guided tour smart lock code dispatch).
- [ ] Vendor billing automation and direct ledger transfers.
- [ ] Multi-region database replication setup on AWS (DocumentDB & RDS).
- [ ] Advanced chatbot capabilities supporting multiple languages and voice calls.
