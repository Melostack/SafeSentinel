## 2024-05-24 - Restrict CORS Configuration
**Vulnerability:** Overly permissive CORS configuration (`allow_origins=["*"]`) in `api/server.py`.
**Learning:** Found FastAPI server accepting requests from any origin, which is a significant security risk for production environments as it allows cross-origin requests from malicious sites.
**Prevention:** Use environment variables (like `FRONTEND_URL`) to restrict CORS origins to trusted domains, falling back to localhost for development.
