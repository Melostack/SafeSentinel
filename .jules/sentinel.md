
## 2024-05-24 - Fix Information Leakage, CORS, and DoS
**Vulnerability:** The API leaked raw exception details `str(e)` to clients, used overly permissive CORS `allow_origins=["*"]`, and lacked input length validation on Pydantic models.
**Learning:** These patterns expose internal system details, allow arbitrary cross-origin requests, and expose the server to DoS attacks via unbounded input.
**Prevention:** Always log exceptions internally using `exc_info=True` returning generic errors to clients, restrict CORS to trusted origins, and enforce `max_length` using Pydantic's `Field` on all string inputs.
