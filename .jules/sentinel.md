## 2024-06-17 - [API Endpoint Security Gap]
**Vulnerability:** Fast API implementation used wildcard CORS, lacked input bounds (DoS risk), and exposed stack traces/internal error messages.
**Learning:** Default Fast API configurations can lead to data leakage or unhandled resource allocation if string limits and error handlers are not explicitly defined.
**Prevention:** Always restrict CORS to frontend domains via env vars, use Pydantic `Field(..., max_length=X)` to limit input sizes, and log errors internally while returning generic 500 messages to the user.
