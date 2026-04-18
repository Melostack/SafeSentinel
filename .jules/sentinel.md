## 2024-05-24 - Restrict Overly Permissive CORS Configuration
**Vulnerability:** The FastAPI server used `allow_origins=["*"]` in its `CORSMiddleware` configuration. This permitted any origin to access the API endpoints, exposing the application to potential cross-site attacks and data leakage.
**Learning:** Hardcoding wildcard origins in middleware can silently undermine the security boundary of an API server. It is crucial to enforce strict origin limits, particularly for backends serving authenticated or sensitive frontends.
**Prevention:** Dynamically load allowed origins from an environment variable (e.g., `FRONTEND_URL`), and ensure the configuration defaults to an empty list (fail securely) if the variable is not set.
