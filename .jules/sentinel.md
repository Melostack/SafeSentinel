## 2025-05-31 - [High] Overly Permissive CORS Configuration
**Vulnerability:** The API server was configured with `allow_origins=["*"]`, allowing any domain to access sensitive backend resources.
**Learning:** Default templates or quick-start code often use wildcard CORS which gets deployed to production. This codebase relies on an environment variable `FRONTEND_URL` for routing, so it can be repurposed to secure CORS.
**Prevention:** Use environment variables to define allowed origins and configure `CORSMiddleware` to strictly allow only trusted domains, supporting comma-separated strings for multi-environment deployments.
