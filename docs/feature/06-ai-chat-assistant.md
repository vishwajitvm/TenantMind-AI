# Feature 06: AI Chat Assistant

## 1. Layman Guide
The Tenant Portal features a 24/7 conversational assistant. Tenants can ask questions about rent deadlines, request repairs, check building announcements, or get help draft request emails.

---

## 2. Technical Guide
* **WebSocket Gateway**: Manages stateful client connections `/api/ws/chat`.
* **State Store**: Redis caches the current conversation history.
* **Integrations**: Uses LangChain pipelines to format conversations and connect to the Model Gateway.

---

## 3. Step-by-Step Flow
1. **Send**: Tenant posts a message over the active WebSocket channel.
2. **Fetch**: The system retrieves previous message history from Redis.
3. **Execute**: Passes the dialogue history and new input to `ModelGateway.generate()`.
4. **Stream**: Streams the generated text chunks back to the client interface.

---

## 4. Data Schema
```json
{
  "session_id": "string (UUID)",
  "user_id": "string (UUID)",
  "history": [
    { "role": "user", "content": "Hello" },
    { "role": "assistant", "content": "Hi there!" }
  ]
}
```

---

## 5. Edge Cases & Mitigations
* **WebSocket disconnection**: If the connection breaks mid-stream, Redis retains the message log cache, allowing the frontend to reload history upon reconnection.
