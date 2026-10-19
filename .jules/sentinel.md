## 2023-10-19 - Removed tracked local environment files
**Vulnerability:** The Vercel OIDC token in .env.local was being tracked in the Git repository because the file was not explicitly added to .gitignore, exposing a hardcoded secret.
**Learning:** Development-specific environment files, especially those containing OIDC tokens or API credentials, must be strictly untracked. Default ignores might miss specific variants like .env.local.
**Prevention:** Explicitly ignore .env.local and frontend/.env.local in .gitignore and verify no secrets are currently tracked by using git ls-files.