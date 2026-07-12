## 2024-07-12 - Sentinel Fixes: Overly Permissive CORS and Error Information Leakage
**Vulnerability:** Overly permissive CORS (`allow_origins=["*"]`) and leaking stack traces/error strings directly to the client via 500 HTTP response.
**Learning:** Hardcoding wildcard CORS and directly passing exception messages to the client are common insecure defaults.
**Prevention:** Always restrict CORS to known/trusted origins, ideally driven by environment configurations. Unhandled exceptions should be logged securely on the server with `exc_info=True`, and a generic error message returned to the client to avoid leaking internal mechanics.
