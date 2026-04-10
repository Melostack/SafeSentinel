## 2024-05-18 - [HIGH] API Information Exposure and Permissive CORS
**Vulnerability:**
1. The `/check` endpoint exception handler returned raw error strings to unauthenticated clients (`detail=str(e)`). This could expose sensitive internal structure, stack traces, or dependencies directly to end users or bots.
2. The FastAPI `CORSMiddleware` was configured with `allow_origins=["*"]`, enabling any third-party domain to make cross-origin requests to the API.

**Learning:**
1. Defaulting to string casting for exceptions in FastAPI `HTTPException` creates a silent and passive information leakage vector.
2. Hardcoding `allow_origins=["*"]` during development can easily leak into production if not tied to an environment variable. Security components should fail closed rather than open.

**Prevention:**
1. Never return raw `Exception` text to the frontend. Always use generic error strings like "Internal server error" and log the actual error internally using `logging.error(..., exc_info=True)`.
2. Restrict CORS origins via dynamically loaded environment variables (e.g., `FRONTEND_URL`), and ensure they default to an empty list `[]` so that cross-origin access fails closed if the configuration is missing.
