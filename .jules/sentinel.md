## 2024-05-24 - Parameter Injection in API Connectors
**Vulnerability:** API connectors (Binance and Bybit) build query strings using manual string concatenation or custom dict joining, leading to parameter injection risks.
**Learning:** Using manual string concatenation to construct URL query strings allows attackers to inject or manipulate parameters if input is unvalidated.
**Prevention:** Always use `urllib.parse.urlencode` (or equivalent library functions) to build query strings for signature generation and HTTP requests.
