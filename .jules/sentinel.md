## 2024-05-15 - [API Info Leakage and Overly Permissive CORS]
**Vulnerability:** The FastAPI application used `allow_origins=["*"]` for CORS, and error handlers returned `detail=str(e)` directly, potentially leaking stack traces or sensitive internal API failure details to end users.
**Learning:** Returning unhandled exceptions directly to API responses can expose infrastructure specifics, and `allow_origins=["*"]` allows malicious sites to make cross-origin requests.
**Prevention:** Always log full exceptions internally using `logging.error(..., exc_info=True)` and return generic `HTTPException` messages to the client. Restrict CORS origins using environment variables (e.g., `FRONTEND_URL`) instead of wildcards.
