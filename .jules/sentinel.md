## 2024-05-24 - Parameter Injection in API Connectors
**Vulnerability:** HMAC signature generation and API request query strings in BinanceConnector and BybitConnector used string formatting/concatenation, allowing parameter injection vulnerabilities. Additionally, there was a timestamp race condition in BybitConnector.
**Learning:** Manual string construction for query strings creates injection risks. Time-based signatures face race conditions if timestamps aren't shared between headers and payload.
**Prevention:** Always use `urllib.parse.urlencode` for query parameters and pass explicitly evaluated timestamps to HMAC generation functions to ensure consistency with headers.
