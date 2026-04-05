## 2024-05-24 - Missing API Authentication on Sensitive Endpoints
**Vulnerability:** The `/extract` and `/check` endpoints in `api/server.py` lacked authentication, allowing unauthorized users to trigger AI logic and external RPC calls, risking API quota depletion and DoS.
**Learning:** Even internal endpoints meant for a Telegram bot must have explicit authentication. Unauthenticated endpoints orchestrating external services are a critical risk.
**Prevention:** Always secure internal APIs that perform sensitive or costly operations with authentication like `APIKeyHeader` out of the box.
