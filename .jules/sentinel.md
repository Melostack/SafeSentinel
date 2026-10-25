## 2024-05-24 - Parameter Injection Vulnerability in API Connectors
**Vulnerability:** API connectors (Binance, Bybit) constructed HTTP query strings and HMAC signature payloads using manual string concatenation, allowing attackers to inject arbitrary parameters by supplying malicious asset names containing '&' or '=' characters.
**Learning:** Manual string construction for URL parameters or signature payloads bypasses proper URL encoding, making the application susceptible to parameter injection, which could lead to unauthorized API actions or signature validation failures.
**Prevention:** Always use standard library functions like `urllib.parse.urlencode` to securely encode query strings and signature parameters.
