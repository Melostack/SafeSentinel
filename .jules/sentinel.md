## 2024-09-10 - Overly permissive CORS and unhandled exceptions
**Vulnerability:** CORS was set to allow all origins (`allow_origins=["*"]`) and exception handlers in `api/server.py` exposed raw exception strings (`detail=str(e)`).
**Learning:** Hardcoded wildcard CORS allows any domain to interact with the API, bypassing browser security. Returning raw error strings leaks internal implementation details to end users.
**Prevention:** Use environment variables (e.g., `FRONTEND_URL`) to dynamically set CORS origins and fall back to safe defaults like `http://localhost:3000`. Use generic error messages for end users and internal logging for debugging.
