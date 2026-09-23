## 2024-06-25 - Parameter Injection in API Connectors
**Vulnerability:** API query strings were manually concatenated (e.g. `query_string = '&'.join([f"{k}={v}" for k, v in params.items()])` and string concatenation with timestamps), exposing the connectors to parameter injection if parameter keys or values contain unescaped characters.
**Learning:** Manual URL parameter construction circumvents safe encoding practices, allowing arbitrary query parameters to be appended or modified, potentially altering API request behavior maliciously.
**Prevention:** Always use standard library functions like `urllib.parse.urlencode` to securely encode and build query strings in API integrations.
