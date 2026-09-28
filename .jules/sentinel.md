## 2024-09-28 - [Multiple Vulnerabilities in FastAPI Server]
**Vulnerability:** The FastAPI server in `api/server.py` had multiple security issues:
1. CORS was configured with `allow_origins=["*"]`, allowing any domain to make requests.
2. Pydantic models (`CheckRequest` and `IntentRequest`) lacked string length limits, posing a DoS risk.
3. Unhandled exceptions in the `/check` endpoint were leaking stack traces/internal errors to the client (`detail=str(e)`).
**Learning:** The default configuration and simple exception handling exposed the application to multiple security risks.
**Prevention:** Use environment variables for CORS, enforce strict input validation, and log errors internally while returning generic messages to clients.
