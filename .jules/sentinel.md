## 2024-04-11 - [CORS and Error Information Leakage Prevention]
**Vulnerability:** Fast API CORS allowed all origins (`*`) and error handlers returned raw exceptions (`str(e)`).
**Learning:** Default settings and raw exceptions expose endpoints to unwanted clients and potentially leak sensitive infrastructure information. Pydantic unbounded strings could be abused for DoS.
**Prevention:** Always scope down CORS to known `FRONTEND_URL`, log exceptions properly, return generic sanitized errors, and use `Field(max_length=...)` for bounding input constraints.
