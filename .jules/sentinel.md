## 2024-05-24 - Exposed Secrets in Git
**Vulnerability:** `.env.local` and `frontend/.env.local` files containing VERCEL_OIDC_TOKEN secrets were tracked in Git.
**Learning:** Automatically generated environment files by tools like Vercel CLI can accidentally be committed if `.gitignore` is not updated to exclude them.
**Prevention:** Always add `*.local` or specifically `.env.local` to `.gitignore` when setting up projects, and verify git status before committing.
