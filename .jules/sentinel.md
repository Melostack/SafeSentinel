## 2024-05-24 - Parameter Injection in API Connectors
**Vulnerability:** API Connectors built query parameters using string formatting and string concatenation (e.g., `f"coin={asset.upper()}"` and `'&'.join([f"{k}={v}" ...])`), making them vulnerable to parameter injection and signature bypassing if asset names contain special characters.
**Learning:** Using manual string concatenation for URL parameters in signature generation functions can lead to parameter injection. Also, race conditions can occur if timestamps are generated independently for headers and signatures.
**Prevention:** Always use `urllib.parse.urlencode` to construct query parameters safely, ensuring correct escaping. Pass a single timestamp instance to both headers and signature generation to prevent race conditions.
