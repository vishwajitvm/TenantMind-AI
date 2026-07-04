# 01. TenantMind AI: Project Overview & Vision

TenantMind AI is an enterprise-grade, multi-tenant property management platform designed to leverage state-of-the-art Artificial Intelligence (AI) to automate tenant communications, lease parsing, maintenance dispatching, and rent processing. By placing Retrieval-Augmented Generation (RAG) and Model Context Protocol (MCP) tool routing at the core of its architecture, TenantMind AI bridges the gap between static databases and dynamic, secure tenant interactions.

## 1. Executive Summary & Problem Statement
Traditional property management is plagued by inefficiencies, slow response times, and manual labor. 
- **Communication Bottlenecks**: Landlords and property managers spend hours answering repetitive questions about lease clauses, utility allocations, and building rules.
- **Maintenance Delay**: Routing work orders to local plumbers, electricians, or HVAC specialists requires manual dispatch, triage, and status follow-ups.
- **Audit & Compliance Risks**: Processing paper or unformatted digital lease agreements leads to data entry errors, missing compliance checks, and a lack of standardized audit trails.
- **Security & Authorization Deficits**: Many modern property portals lack strict data segregation, exposing sensitive financial and background screening documents to unauthorized roles.

TenantMind AI resolves these challenges by introducing an intelligent, resilient microservices framework that orchestrates FastAPI, Next.js, Keycloak OIDC, Qdrant Vector search, Celery, and MongoDB.

## 2. Core Vision & System Goals
* **Automated Lease Querying**: Enable tenants to receive instant, legally grounded answers about their lease terms using RAG over signed PDF agreements.
* **Intelligent Maintenance Routing**: Triage and categorize incoming tenant maintenance requests using NLP classifier models, dispatching them to vendors without human intervention unless flagged as high-risk.
* **Multi-Tenant Data Isolation**: Enforce strict data boundaries using tenant-specific scopes verified dynamically against Keycloak OIDC tokens.
* **Human-in-the-Loop AI Control**: Incorporate Model Context Protocol (MCP) gateways to classify AI tool execution risk, securing high-risk commands behind an approval workflow.
* **Resilient Infrastructure**: Construct a multi-tier fallback architecture for large language model (LLM) calls to guarantee service availability even during API outages.

## 3. Product Scope & User Personas
The system targets three distinct user groups:
1. **Tenants**: Access the Tenant Portal to chat with the AI assistant, submit maintenance tickets, upload move-in checklists, and execute secure rent payments.
2. **Landlords / Property Managers**: Oversee properties, configure auto-approval thresholds, manage maintenance boards, examine financial dashboard analytics, and audit MCP tool executions.
3. **Vendors (Maintenance Specialists)**: Receive automated SMS/Email work orders, update job status, upload completion evidence, and submit invoices.
