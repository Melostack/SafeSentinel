
## 2026-03-11 - [Missing Authentication on Internal APIs]
**Vulnerability:** The internal API endpoints (`/extract` and `/check`) were exposed without any authentication, allowing unauthorized users to hit them directly. This is a severe risk since these endpoints orchestrate external rate-limited or paid services (like OpenRouter, Gemini, CMC).
**Learning:** Internal APIs that consume external quota/resources must be authenticated by default, otherwise attackers can easily cause API quota depletion (DoS) and financial impact.
**Prevention:** Always enforce API Key authentication using framework-native mechanisms (e.g., FastAPI `APIKeyHeader` and `secrets.compare_digest`) for internal endpoints before deploying.
