## 2024-05-24 - [CORS Wildcard Configuration in FastAPI]
**Vulnerability:** The FastAPI server explicitly configured CORS `allow_origins=["*"]`, opening up the API to cross-origin requests from any domain, which bypasses Same-Origin Policy protections.
**Learning:** Default templates or quick-start examples for FastAPI often use wildcard CORS to get things working fast, but these configurations are routinely deployed to production, increasing the attack surface.
**Prevention:** Always restrict CORS `allow_origins` to a dynamically loaded list of trusted domains from environment variables (e.g., `os.environ.get("FRONTEND_URL")`) rather than hardcoding a wildcard.
