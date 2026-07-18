## 2024-05-18 - [Fix multiple vulnerabilities in API server]
**Vulnerability:** The API server had multiple vulnerabilities, including overly permissive CORS (`allow_origins=["*"]`), missing length limits on Pydantic models (DoS risk), and an exception handler that leaked internal error details (`detail=str(e)`).
**Learning:** These are common security patterns in FastAPI applications. It is crucial to enforce strict boundaries on inputs, origins, and error outputs to prevent both targeted attacks and information leakage.
**Prevention:** Implement strict input validation, configure CORS securely using environment variables, and log exceptions internally while returning generic error messages to the client. Ensure no scratchpad files are left in the repository.
