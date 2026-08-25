## 2024-05-24 - Parameter Injection in API Signature Generation
**Vulnerability:** Manual string concatenation for query strings in API connectors allows parameter injection, which could manipulate API requests or invalidate HMAC signatures.
**Learning:** Hardcoding query strings without proper URL encoding exposes the system to parameter injection attacks.
**Prevention:** Always use safe URL encoding libraries like `urllib.parse.urlencode` when constructing HTTP query strings from user-supplied data.
