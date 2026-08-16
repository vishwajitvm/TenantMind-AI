# Edge Case Register

This register catalogues active system edge cases, mitigation strategies, and resolved scenarios.

| ID | Module | Scenario | Risk | Mitigation | Status |
|----|--------|----------|------|------------|--------|
| EC-001 | Payment | Double payment submission | High | Idempotency Keys | Mitigation Configured |
| EC-002 | Keycloak | Out of sync user deletion | Medium | Keycloak User Event Webhook Sync | Mitigated |
| EC-003 | RAG | Irrelevant context responses | Low | Score-based thresholds & prompt guardrails | Mitigated |
