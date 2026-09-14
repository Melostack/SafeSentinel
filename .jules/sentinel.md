## 2024-05-18 - [API Information Leakage and CORS Misconfiguration]
**Vulnerability:** The API had an overly permissive CORS policy (`allow_origins=["*"]`), lacked string length limits on Pydantic models (DoS risk), and leaked internal error traces in HTTP 500 responses.
**Learning:** These configurations expose the application to cross-origin attacks, DoS via large payloads, and internal reconnaissance.
**Prevention:** Always restrict CORS origins using environment variables, strictly define `max_length` in Pydantic, and log errors internally while returning generic messages like 'Erro interno do servidor' to the client.
