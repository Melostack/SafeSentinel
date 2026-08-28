## 2024-08-28 - [Fix Error Leakage & CORS]
**Vulnerability:** CORS allowed all origins (`*`), Pydantic models lacked length limits (DoS risk), and the `/check` endpoint leaked raw exception details in 500 errors.
**Learning:** Returning `str(e)` in HTTP exceptions directly exposes internal stack traces or database errors to the client.
**Prevention:** Always log exceptions internally using `logging.error(..., exc_info=True)` and return a generic error message like 'Erro interno do servidor'. Use `FRONTEND_URL` for CORS and limit string lengths in Pydantic models.
