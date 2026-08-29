## 2024-05-24 - Fix CORS and Exception Handling Vulnerabilities
**Vulnerability:** The API had an overly permissive CORS configuration (`allow_origins=["*"]`) and exposed raw exception details in HTTP 500 responses (`detail=str(e)`), risking information leakage.
**Learning:** Using `*` for CORS opens the API to cross-origin attacks from any domain. Returning raw error strings to the client can leak stack traces or internal system state.
**Prevention:** Always restrict CORS origins using environment variables (e.g., `FRONTEND_URL.split(',')`). Log errors internally using standard `logging` with `exc_info=True` and return generic error messages (e.g., "Erro interno do servidor") to the client.
