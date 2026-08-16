# 13. Monitoring, Metrics & Logging

We run a full observability stack.

## Components
- **LangSmith**: Scrapes `/api/traces` from FastAPI.
- **LangSmith**: Visualizes throughput, latencies, CPU/Memory load, and Celery queue length.
- **LangSmith**: Aggregates Nginx and backend container logs.
