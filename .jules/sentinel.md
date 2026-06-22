## 2024-05-18 - Prevent Parameter Injection in Connector URL Encoding
**Vulnerability:** String concatenation of URL params inside API connectors was used, leading to potential parameter injection vulnerabilities.
**Learning:** For API connections relying on HMAC hashing with concatenated strings, it is crucial to use standard library URL parameter encoding (like `urllib.parse.urlencode`) instead of `&.join` to avoid incorrect encoding of special characters that allow bypassing authentication or parameter injection.
**Prevention:** Enforce usage of `urllib.parse.urlencode` for any dictionary parameters intended for URLs or HMAC generation.
