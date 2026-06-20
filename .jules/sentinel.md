## 2024-05-19 - FastAPI Missing Security Safeguards (CORS, DoS, Info Leak)
**Vulnerability:** The FastAPI application suffered from three severe security vulnerabilities:
1. `allow_origins=["*"]` on `CORSMiddleware`, exposing the API to Cross-Origin Resource Sharing attacks from any domain.
2. Pydantic models (`CheckRequest`, `IntentRequest`) lacked string length limits, making the API susceptible to Denial of Service (DoS) attacks via memory exhaustion from enormous payloads.
3. The main exception handler in `/check` returned the raw exception string to the client (`detail=str(e)`), potentially leaking sensitive internal system details or stack traces, and did not securely log the exception internally.
**Learning:** Default FastAPI setups do not inherently secure external endpoints. Pydantic models require explicit constraints (`max_length`). Broad CORS configurations are dangerous. Raw exception details must never reach the client.
**Prevention:**
1. Always restrict CORS origins using environment variables (e.g., `FRONTEND_URL`).
2. Always apply `Field(..., max_length=X)` constraints on string inputs in Pydantic models.
3. Use `logging.error("...", exc_info=True)` for internal logging and return generic user-facing messages (e.g., "Internal Server Error").
