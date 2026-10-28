## 2024-05-30 - Fix Parameter Injection in API Connectors
**Vulnerability:** API Connectors used manual string concatenation (`&.join(...)` and `f"coin={asset.upper()}"`) for query string signature generation, opening up risk of parameter injection.
**Learning:** URL query parameters must be properly URL encoded especially when used as a payload for signing and authenticating API requests.
**Prevention:** Always use standard libraries like `urllib.parse.urlencode` to serialize query parameters instead of manual string concatenation.
