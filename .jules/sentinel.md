## 2024-10-24 - Overly Permissive CORS Configuration
**Vulnerability:** The FastAPI application used allow_origins=["*"] in its CORSMiddleware configuration. Additionally, stack traces were exposed in HTTP 500 errors.
**Learning:** Defaulting to wildcard CORS and exposing internal exceptions are common shortcuts but create significant attack surfaces in production environments.
**Prevention:** Always restrict allow_origins to explicitly trusted domains using environment variables, and always catch exceptions and return generic error messages while logging the actual trace internally.
