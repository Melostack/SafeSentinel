## 2024-11-05 - [CRITICAL] Untracking Environment Files
**Vulnerability:** Environment files (`.env.local`) containing sensitive tokens (`VERCEL_OIDC_TOKEN`) were accidentally tracked in Git.
**Learning:** Even though `.env` may be ignored in `.gitignore`, other `.env.*` files (like `.env.local`) might not be unless explicitly specified.
**Prevention:** Ensure wildcard or explicit ignore rules are in place in `.gitignore` for all environment files containing secrets (e.g. `.env.local`, `.env.*`).
