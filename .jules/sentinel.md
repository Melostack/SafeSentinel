## 2024-05-24 - VERCEL_OIDC_TOKEN exposure in .env.local
**Vulnerability:** The project contained tracked `.env.local` files in the root and `frontend/` directory, exposing a sensitive JWT token (`VERCEL_OIDC_TOKEN`).
**Learning:** Automatically generated environment variables like Vercel OIDC tokens should not be committed to version control. They should be generated dynamically or injected through CI/CD pipelines. This vulnerability exposed sensitive deployment tokens to the public repository.
**Prevention:** Add `.env.local` to `.gitignore` to ensure these files are never committed, and remove the existing tracked files from Git.
