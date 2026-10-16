## 2023-10-16 - API Parameter Injection
**Vulnerability:** Parameter injection in API connectors due to manual query string concatenation.
**Learning:** Manual string formatting (e.g. `&`.join or f-strings) for query params allows injection if input contains `&` or `=`.
**Prevention:** Always use `urllib.parse.urlencode` to securely build URL query strings.
