
## 2024-05-31 - Parameter Injection in Signature Generation
**Vulnerability:** API connectors generated HMAC signatures and query strings using unsafe manual string concatenation instead of `urllib.parse.urlencode`.
**Learning:** Manual concatenation of query parameters allows for parameter injection attacks, potentially bypassing authentication or altering requests.
**Prevention:** Always use `urllib.parse.urlencode` to construct query strings for signature generation and API requests.
