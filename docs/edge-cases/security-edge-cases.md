# Security Edge Cases

Detailed security vulnerabilities and containment rules.

## Token Hijack
- **Scenario**: JWT intercept.
- **Mitigation**: Access token expiration set to 15 minutes, refresh tokens rotated, strict TLS 1.3 requirement.

## Vector DB Pollution
- **Scenario**: Uploading malicious vectors.
- **Mitigation**: Sanitization of input text, bounding embedding norms.
