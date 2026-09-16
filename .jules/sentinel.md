## 2024-05-24 - [Overly permissive CORS, DoS, and Info Leakage in API]
**Vulnerability:** The API used allow_origins=["*"], lacked input length limits on Pydantic models, and exposed raw exception strings in error responses.
**Learning:** These defaults allow unauthorized domains to make cross-origin requests, leave endpoints vulnerable to DoS via large inputs, and expose system internals on errors.
**Prevention:** Always restrict CORS to trusted domains via env variables, enforce max_length on all API string inputs, and catch exceptions to log internally while returning generic user-facing messages.
