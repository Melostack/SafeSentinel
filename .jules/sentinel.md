## 2023-10-20 - Prevent Tracking of Local Environment Files
**Vulnerability:** Local environment files (`.env.local`) containing hardcoded secrets like VERCEL_OIDC_TOKEN were tracked in the Git repository.
**Learning:** Missing exclusions in `.gitignore` lead to accidental exposure of sensitive environment credentials.
**Prevention:** Explicitly include `.env.local` and similar credential files in `.gitignore` before committing code.
