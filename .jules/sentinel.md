## 2024-05-24 - [Fix FastAPI Security Defaults]
**Vulnerability:** The FastAPI application used `allow_origins=["*"]` which enables any domain to make cross-origin requests, Pydantic inputs had no string length limits enabling DoS attacks, and error traces were leaked via the API responses.
**Learning:** Default unconstrained implementations often lead to subtle information leakage and resource exhaustion if not explicitly limited, particularly in Python web APIs parsing JSON natively via Pydantic.
**Prevention:** Always restrict CORS origins using environment variables, set explicit `max_length` attributes on `Field` for all Pydantic strings, and use generic detail messages paired with internal `exc_info=True` logging for default exception handlers.
