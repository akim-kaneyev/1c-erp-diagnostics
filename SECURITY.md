# Security and confidentiality

## Never commit or publish

- production `.dt` information bases;
- full database backups;
- 1C/ITS credentials;
- API tokens, private keys or connection strings;
- unnecessary personal data;
- primary documents or register exports containing confidential business data beyond what is required for a reproducible sanitized example.

## Before giving evidence to an AI agent

1. Keep only what is needed to answer the case question.
2. Remove or pseudonymize names, phones, emails, banking details and secrets.
3. Remove hidden spreadsheet sheets when they are irrelevant.
4. Review file properties and metadata.
5. Prefer stable pseudonyms so relationships can still be traced without exposing identities.

## OpenSandbox / isolated execution

Use a separate disposable environment per case when isolation is needed. Restrict egress where practical, inject secrets through a supported vault/environment mechanism, record commands and versions, and treat sandbox output as evidence rather than truth.

## Repository controls

The public repository uses:

- a protected `main` branch with Pull Request, CI and CodeQL requirements;
- no force-push or branch deletion;
- private vulnerability reporting;
- dependency graph, Dependabot alerts and security updates;
- CodeQL analysis for GitHub Actions and Python;
- secret scanning and push protection.

These controls reduce repository and supply-chain risk but do not make confidential 1C data safe to publish.

## Vulnerability reporting

Do not post secrets, exploit details or affected customer/company data in a public issue. Use GitHub **Private vulnerability reporting** for security findings. Public Issues are appropriate only for non-sensitive bugs, feature requests and sanitized reproductions.

## Public examples

Any example committed to `cases/` must be synthetic or irreversibly sanitized. Real customer/company data is out of scope for the public repository.
