## 2025-05-24 - API Key Authentication added to external-facing APIs
**Vulnerability:** Unauthenticated internal APIs orchestrating paid external services.
**Learning:** Endpoints like `/check` and `/extract` in `api/server.py` were not authenticated, allowing anyone to send requests and consume API quotas of the backend services like OpenRouter.
**Prevention:** All internal endpoints that use external APIs should require authentication by default to prevent Denial of Service via quota depletion.
