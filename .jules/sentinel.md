## 2024-05-05 - Avoid Exposing Raw Exception Details in API Responses
**Vulnerability:** The API endpoint `/check` was returning raw exception strings (`str(e)`) to unauthenticated users via HTTP 500 responses.
**Learning:** Returning unhandled exception strings can inadvertently expose sensitive internal state, stack traces, configurations, or external API response details (e.g., failed downstream API requests with tokens in URL or headers) to the client, leading to critical information leakage.
**Prevention:** Always log the full exception internally (using `logging.error(e, exc_info=True)`) to maintain observability, while returning generic, non-sensitive error messages (like "Internal server error") to the client.
