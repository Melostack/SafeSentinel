## 2024-09-26 - Fix Multiple Vulnerabilities in API Server
**Vulnerability:** The API Server had missing limits on input payload lengths, exposed error details on exceptions, and overly permissive CORS policies.
**Learning:** Pydantic models need explicit string length limits to prevent DoS attacks. Raw exceptions leak stack traces. CORS policies must be explicitly allowed.
**Prevention:** Apply `Field(..., max_length=X)` to Pydantic models. Mask exception messages. Use environment variables to handle CORS origins.
