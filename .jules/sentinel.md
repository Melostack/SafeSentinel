## 2023-10-09 - Parameter Injection in HMAC Signatures
**Vulnerability:** API query strings for HMAC signature generation were being constructed using string concatenation instead of standard encoding functions, making them susceptible to parameter injection attacks.
**Learning:** Building URL parameters manually by appending strings introduces risk when generating authentication payloads, as inputs can inject arbitrary query parameters and bypass validation.
**Prevention:** Always use `urllib.parse.urlencode()` or robust HTTP client libraries to correctly escape and assemble query parameters and signature payloads.
