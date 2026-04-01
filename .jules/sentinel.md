## 2024-05-24 - [Parameter Injection Vulnerability in API Connectors]
**Vulnerability:** Manual string concatenation for query string generation (e.g. `query_string = '&'.join([f"{k}={v}" for k, v in params.items()])`) allows parameter injection.
**Learning:** Manually building query strings fails to encode special characters (like `&` and `=`), allowing an attacker to inject arbitrary parameters into the request signature logic.
**Prevention:** Use `urllib.parse.urlencode(params)` to securely URL-encode query strings, ensuring special characters are escaped.
