## 2024-05-24 - API Connector Signature Vulnerability
**Vulnerability:** Manual query string concatenation in API connectors allowed parameter injection, and desynced timestamps caused race conditions in HMAC signatures.
**Learning:** Always use URL encoding libraries for parameter construction and synchronize timestamps across signature and request headers to prevent forgery and authentication errors.
**Prevention:** Enforce the use of `urllib.parse.urlencode` for query parameters and synchronize timestamp variables in API connector implementations.
