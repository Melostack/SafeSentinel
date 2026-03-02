## 2024-05-24 - Missing Authentication on Critical API Endpoints
**Vulnerability:** The `/extract` and `/check` endpoints in `api/server.py` lacked authentication, allowing unauthorized users to consume backend resources and potentially expose sensitive risk logic. Additionally, the global exception handler was leaking detailed error strings via HTTP 500 responses (`detail=str(e)`).
**Learning:** Endpoints designed for internal or specific clients (like the Telegram Bot) must be protected by default. When building fast prototypes with FastAPI, it's easy to overlook adding dependencies to the path operations. Furthermore, leaking Python exception strings directly to the client provides attackers with insight into the system's internal workings. Using `secrets.compare_digest` is crucial for preventing timing attacks during API key validation.
**Prevention:**
1. Always implement `fastapi.security.api_key.APIKeyHeader` and a `Depends(get_api_key)` function for internal APIs.
2. Use `secrets.compare_digest` for token comparisons.
3. Never return `str(e)` in an HTTPException; always log the full error internally and return a generic "Internal Server Error" message to the client.