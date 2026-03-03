## 2026-03-03 - [Missing API Authentication]
**Vulnerability:** Missing authentication on the `/extract` and `/check` endpoints in `api/server.py` exposed sensitive functionality to unauthorized users, causing potential API quota drains (e.g., via OpenRouter/LLM endpoints).
**Learning:** Endpoints making calls to external LLMs must be protected. Standard FastAPI dependency injection with `Security(APIKeyHeader)` is the preferred method for managing internal API keys between services. String comparison of API keys can lead to timing attacks.
**Prevention:** Use `secrets.compare_digest` when verifying API keys to mitigate timing attacks. Ensure that all API services accessed by internal or external consumers enforce proper authentication logic using dependency injection.
