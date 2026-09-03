## 2024-05-01 - [Vulnerabilidades do Sentinel]
**Vulnerabilidade:** Configuração insegura de CORS
**Learning:** O CORS deve estar configurado para permitir origens específicas, em vez de `["*"]`, para prevenir ataques CSRF.
**Prevention:** Configurar `allow_origins` com variáveis de ambiente ou origens confiáveis.

## 2024-05-01 - [CORS, Data Leakage and Injection Fixes]
**Vulnerability:** Permissive CORS (`["*"]`), stack trace leakage on 500 errors, DoS via unconstrained payload sizes, and parameter injection via string concatenation in Binance and Bybit API connectors.
**Learning:** Exposing full stack traces in API errors and allowing unresticted input lengths are critical security risks. String concatenation for query parameters should always be avoided in favor of proper URL encoding.
**Prevention:** Always restrict CORS to known origins, mask internal error details returning generic messages, enforce field length limits using Pydantic, and use `urllib.parse.urlencode` for secure parameter formatting.
