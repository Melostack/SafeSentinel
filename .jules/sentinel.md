## 2024-05-24 - [CORS & Info Leakage]
**Vulnerability:** Overly permissive CORS (`allow_origins=["*"]`) and exposed exception details (`str(e)`) in `api/server.py`.
**Learning:** Using `*` for CORS allows any domain to access the API, risking cross-origin attacks. Raw exception strings leak internal server state to end users.
**Prevention:** Use environment variables (e.g., `FRONTEND_URL`) to restrict CORS origins and use a generic error message while logging the actual traceback internally with `exc_info=True`.
