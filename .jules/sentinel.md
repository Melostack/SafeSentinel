## 2026-09-15 - Prevent Parameter Injection and Race Conditions in API Connectors
**Vulnerability:** API connectors were vulnerable to parameter injection due to manual string concatenation of query parameters, and Bybit had a race condition in signature generation using different timestamps.
**Learning:** Manual string concatenation for URL parameters creates injection vectors. Generating timestamps inside signature methods separate from request headers causes authentication failures due to mismatched timestamps.
**Prevention:** Always use `urllib.parse.urlencode` for HMAC query strings and pass pre-generated timestamps to signature generators.
