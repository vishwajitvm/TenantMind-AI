# Feature 06: AI Chat Assistant

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
