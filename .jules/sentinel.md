## 2023-10-11 - Parameter Injection and Timestamp Race Conditions in API Connectors
**Vulnerability:** API connectors (Binance, Bybit) built query strings using manual string concatenation, creating a risk for parameter injection. Additionally, Bybit's timestamp generation for signatures could drift between signature creation and header assignment, causing authentication failures.
**Learning:** Using `urllib.parse.urlencode` safely escapes query parameters, preventing injection. Always passing a pre-computed timestamp to signature generators guarantees consistency with HTTP headers, resolving race conditions.
**Prevention:** Enforce `urllib.parse.urlencode` for all API URL query constructions and centralize timestamp variables when building HMAC payloads and headers.
