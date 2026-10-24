## 2024-10-24 - API Connectors Parameter Injection
**Vulnerability:** The Binance and Bybit API connectors were manually building URL query strings for their HMAC signatures, creating a parameter injection vulnerability.
**Learning:** Using string concatenation (`f"{k}={v}"` or `params = f"coin={asset}"`) for API request payloads can allow an attacker to inject additional parameters into the signed request if the input is not sanitized, bypassing the signature protection.
**Prevention:** Always use standard library functions like `urllib.parse.urlencode` to construct query strings for API requests and signature generation to ensure proper URL encoding and parameter separation.
