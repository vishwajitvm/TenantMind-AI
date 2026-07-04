# 07. Frontend Architecture & Flow

The presentation tier of TenantMind AI is built with Next.js (App Router), implementing client-side routing, state management, and real-time event updates.

## 1. Technical Stack Configuration
* **Framework**: Next.js 14+ (App Router, Server Components).
* **State Management**: **Zustand** (lightweight stores for user auth session, chat windows, notifications, and UI state).
* **Data Fetching**: **React Query (TanStack Query)** (handles caching, cache invalidation, loading states, and mutations).
* **Icons**: **Lucide Icons** (scalable vectors for status screens and menus).
* **Layouts & Transitions**: **Tailwind CSS** combined with **Framer Motion** for smooth visual feedback.
* **Canvas Workflows**: `@xyflow/react` (React Flow) for modeling system approval paths and maintenance routing hierarchies visually.

---

## 2. Store Structure (Zustand)

### Core Auth Store (`stores/useAuthStore.ts`)
Controls user context and OIDC tokens:
```typescript
interface AuthState {
  isAuthenticated: boolean;
  accessToken: string | null;
  userInfo: UserInfo | null;
  login: () => void;
  logout: () => void;
}
```

### Chat Store (`stores/useChatStore.ts`)
Manages transient dialogue structures:
```typescript
interface ChatState {
  messages: Array<{ id: string; sender: string; text: string }>;
  isStreaming: boolean;
  sendMessage: (text: string) => Promise<void>;
}
```

---

## 3. Communication Pipelines

* **REST APIs**: Used for configuration panels, property logs, payments, and approvals.
* **WebSockets**: Initiated once authenticated via Keycloak. Listens to notifications like:
  * `TICKET_UPDATE`: Pushes immediate status changes of maintenance tickets.
  * `APPROVAL_REQUIRED`: Warns landlords of a pending high-risk MCP task.
  * `PAYMENT_LEDGER_POSTED`: Signals completion of invoice transactions.
