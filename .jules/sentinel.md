## $(date +%Y-%m-%d) - [HIGH] Fix overly permissive CORS configuration
**Vulnerability:** The FastAPI `CORSMiddleware` used `allow_origins=["*"]`, allowing any website to make cross-origin requests to the API.
**Learning:** Found overly permissive CORS in the API initialization logic. This is a common pattern in fast prototyping but creates a CSRF/security risk in production as it bypasses the same-origin policy.
**Prevention:** Always restrict CORS allowed origins to trusted domains (like reading `FRONTEND_URL` from the environment), and fail closed (empty list) if the variable is not set.
