# Feature 20: Integration Webhooks

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
