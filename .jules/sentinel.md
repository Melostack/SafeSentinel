## 2024-04-02 - Prevent Information Leakage in API Exception Handlers
**Vulnerability:** The `/check` endpoint in `api/server.py` caught raw exceptions and returned them directly to the client via `detail=str(e)`, exposing internal stack details and potential configuration data.
**Learning:** Returning raw exception strings in FastAPI's `HTTPException` creates an information leakage vulnerability. This is particularly dangerous for endpoints handling complex external integrations where errors may reveal internal state or API secrets.
**Prevention:** Exception handlers must log the exact error internally with `exc_info=True` for debugging, and return generic, non-sensitive error messages to API consumers.
