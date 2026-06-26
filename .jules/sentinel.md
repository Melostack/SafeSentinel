## 2026-06-26 - [CRITICAL] Fix CORS, input limits, and error info leakage
**Vulnerability:** The API server had multiple vulnerabilities including an overly permissive CORS setup (`allow_origins=["*"]`), missing length bounds on user inputs for Pydantic requests (causing DoS risks), and detail leakage in the generic `Exception` handler which previously returned the full exception traceback as `detail=str(e)`.
**Learning:** In fast-paced prototyping, security basics such as CORS configuration, strict schema validation (limiting string lengths in models), and secure error handling are often overlooked. Exposing stack traces (`str(e)`) leaks critical internal context that attackers can leverage, while unrestricted payloads via Pydantic make applications susceptible to resource exhaustion attacks.
**Prevention:**
- Explicitly split trusted URLs for `allow_origins`.
- Make it standard practice to enforce `max_length` using Pydantic's `Field`.
- Avoid direct string exposure of exceptions into user-facing responses; use a robust logger to securely stash the `exc_info` and return a generic error.
