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

## Vulnerability reporting

Do not post secrets or exploit details in a public issue. If GitHub private vulnerability reporting is enabled, use it. Otherwise open a minimal issue stating that you need a private security contact, without including sensitive details.

## Public examples

Any example committed to `cases/` must be synthetic or irreversibly sanitized. Real customer/company data is out of scope for the public repository.
