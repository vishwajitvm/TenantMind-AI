# 13. Monitoring, Metrics & Logging

We run a full observability stack.

## Components
- **Prometheus**: Scrapes `/api/metrics` from FastAPI.
- **Grafana**: Visualizes throughput, latencies, CPU/Memory load, and Celery queue length.
- **Loki**: Aggregates Nginx and backend container logs.
