# 09. Background Jobs & Queues

Celery acts as the task queue, with Redis as the broker.

## Key Workers
- **Worker**: Processes PDF document processing, sends emails, schedules inspections, dispatches vendor notifications.
- **Scheduler (Celery Beat)**: Periodically checks for outstanding rent, triggers utility calculations daily, and generates reports weekly.
