## 2024-05-30 - Fix API Information Leakage and CORS
**Vulnerability:** Information leakage via unhandled exception details (`str(e)`) and overly permissive CORS configuration (`allow_origins=["*"]`). Missing input length limits on Pydantic models also created a DoS risk.
**Learning:** Returning raw error objects in the API response can inadvertently expose internal system logic or tracebacks. Allowing all origins via CORS leaves the API open to unauthorized cross-origin requests.
**Prevention:** Always use internal logging for exception details (`exc_info=True`) and return a generic message to the client. Validate and restrict CORS configurations strictly using environment variables. Add length constraints (`max_length`) to Pydantic strings to limit payload sizes.
