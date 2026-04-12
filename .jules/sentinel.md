## 2024-05-18 - [CRITICAL] Parameter Injection in API Connectors
**Vulnerability:** API connectors (Binance, Bybit) constructed URL query strings manually using string concatenation or f-strings for cryptographic signatures and API requests. This allows untrusted user input to inject malicious parameters into signed requests.
**Learning:** Manual URL parameter construction is a recurring anti-pattern in the codebase and can bypass signature verification if attackers inject arbitrary data.
**Prevention:** Always use `urllib.parse.urlencode` to securely encode query strings instead of manual string formatting to prevent parameter injection attacks.
