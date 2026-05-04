## 2024-05-04 - Missing Timeout in External API Calls (DoS Risk)
**Vulnerability:** The `requests.post` call to the external Perplexity API in `core/sourcing_agent.py` was missing an explicit `timeout` parameter.
**Learning:** This is a Denial of Service (DoS) vulnerability pattern. External APIs can hang indefinitely. If the backend orchestrating these calls does not enforce timeouts, connection threads can become saturated waiting for responses, bringing the entire application down.
**Prevention:** Always enforce a strict `timeout` (e.g., `timeout=15`) on all external synchronous HTTP requests (like those using `requests`).
