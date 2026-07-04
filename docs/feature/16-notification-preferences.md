# Feature 16: Notification Preferences

## 1. Layman Guide
Users can choose how they want to receive notifications (e.g. rent reminders or maintenance updates), with settings to toggle email, SMS, and in-app alerts on or off.

---

## 2. Technical Guide
* **Storage**: Preferences are stored as a configuration block in the MongoDB user document.
* **Notification Routing**: The notification engine queries these settings before dispatching alerts to determine active communication channels.

---

## 3. Step-by-Step Flow
1. **Configure**: User toggles notification channels in their settings panel.
2. **Save**: The frontend updates preferences via a REST call.
3. **Write**: The backend saves these settings to the user's MongoDB document.
4. **Deliver**: Prior to dispatching alerts, Celery checks settings and routes notifications to active channels.

---

## 4. Data Schema
```json
{
  "user_id": "string (UUID)",
  "notification_channels": {
    "rent_due": { "email": true, "sms": false },
    "ticket_update": { "email": true, "sms": true }
  }
}
```

---

## 5. Edge Cases & Mitigations
* **Empty preference profiles**: If no settings are configured, the system falls back to default settings (email and in-app alerts enabled, SMS disabled) to prevent missed notifications.
