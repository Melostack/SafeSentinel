## 2024-05-30 - Internal API Exposure & Information Leakage
**Vulnerability:** Internal APIs were missing explicit authentication and exception handlers exposed error tracebacks.
**Learning:** Even if an API is meant only for internal microservices, it can be exposed unintentionally. Also, relying on `detail=str(e)` in error handling leaks sensitive stack trace info and system state.
**Prevention:** All APIs, internal or external, must use explicit authentication (e.g. `X-API-Key` headers validated with `secrets.compare_digest`). Exception blocks must use `logging.error(e, exc_info=True)` internally and return generic messages to the client.
