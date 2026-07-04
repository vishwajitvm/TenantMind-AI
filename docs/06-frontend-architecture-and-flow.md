# 06. Frontend Architecture & Flow

The Next.js client is structured to maximize modularity and user experience.

## Tech Stack
- **Framework**: Next.js (App Router)
- **State Management**: Zustand
- **Data Fetching**: React Query (TanStack Query)
- **Styling**: Tailwind CSS & Framer Motion
- **Interactions**: @xyflow/react for workflow maps

## Flow
On mount, the application checks Keycloak session. If active, state is loaded into Zustand and active websocket channels are opened for real-time notifications.
