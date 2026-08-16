# Feature 16: Notification Preferences

## Layman Guide
Choose how you want to be contacted: email, SMS, or app notifications.

## Technical Guide
A key-value settings block in MongoDB user document. Handled dynamically during worker dispatch.

## Flow
1. User modifies preferences in settings.
2. API updates user document.
3. Notification engine queries preferences prior to dispatch.

## Data Schema
```json
{
  "user_id": "uuid",
  "preferences": {"email": true, "sms": false, "in_app": true}
}
```

## Edge Cases
- **Invalid configurations**: Fail-safe defaults to Email and In-App enabled.
