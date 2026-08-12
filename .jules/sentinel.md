## 2024-05-24 - [Fix overly permissive CORS and insecure error handling]
**Vulnerability:** CORS was set to allow all origins ('*'), unhandled exceptions were exposing stack traces to clients, and Pydantic models lacked string limits.
**Learning:** Using 'allow_origins=["*"]', 'str(e)' in HTTP responses, and unbounded strings can lead to security risks like unauthorized cross-origin requests, information leakage, and DoS attacks.
**Prevention:** Use environment variables for allowed origins, return generic error messages while logging exceptions internally, and enforce string lengths on Pydantic models.
