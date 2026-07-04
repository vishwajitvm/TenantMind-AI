# 14. Monitoring, Metrics & Logging

TenantMind AI implements a complete observability stack to monitor service metrics, container states, and logging trails.

## 1. Metrics Collection (Prometheus)
FastAPI exposes instrumentation metrics at `/api/metrics` (or `/metrics`), scraped by Prometheus on a 15-second interval:
* **HTTP Requests**: Throughput, latencies, and status code counts.
* **Celery Metrics**: Active worker counts, task latency, and message queue lengths.
* **Database States**: Active connections count and read/write operation rates.

---

## 2. Visualization (Grafana)
Grafana connects to Prometheus and provides three pre-configured dashboards:
1. **System Resource Dashboard**: Tracks CPU, memory usage, and storage across all containers.
2. **AI Operations Dashboard**: Monitors LLM response times, token count consumption, API error rates, and fallback counts.
3. **Ledger & Business Dashboard**: Monitors transaction success rates, payments, and ticket resolution statistics.

---

## 3. Structured Logging (TraceNest & Loki)
The system uses the custom `tracenest` middleware to log structured events:
* **Request Tracing**: Maps incoming requests with a unique transaction ID (`X-Trace-ID`) propagated through FastAPI and Celery.
* **Log Aggregation**: Standard container logs are captured by **Loki** and queryable in Grafana.
