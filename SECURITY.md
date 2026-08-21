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

## SonarQube BSL adapter

SonarQube is an optional evidence source, not a trusted decision engine. The safe default is a user-managed instance bound to a loopback address. SonarQube stores analyzed source and derived analysis data, so sanitize the source before scanning and treat the SonarQube instance as a data destination.

Risk boundaries are explicit:

- reading an existing report without changing server state is R0;
- scanning sanitized source on a loopback-only local instance is R1 because it creates or updates local analysis records;
- creating or deleting a project or token, or changing a quality profile, is R2 and requires explicit confirmation at action time;
- remote source upload or an external SonarQube write is R3, requires a separately reviewed workflow and exact approval for that transmission/write, and must use HTTPS. Reading an approved existing remote report can be R0 through a separate read capability; it never makes the local adapter available.

The adapter must not automatically create or delete projects or tokens, or change quality profiles. Because the scanner has no general auto-create disable switch, preflight must prove the exact existing project and project-scoped analysis token before invocation. Scanner and API tokens must never be committed, stored in project files, pasted into chat, placed in command-line arguments or printed in logs. Supply the scanner token only to the scanner child process through `SONAR_TOKEN`. Use a separate least-privilege API token as an `Authorization: Bearer` value, injected from an approved secret source only for the API child process.

Set the scanner working directory to a new adapter-owned disposable directory beneath its own temporary root. Never point it at a user-owned or pre-existing directory: the scanner may delete and recreate its working directory.

Record sanitized provenance without credentials: server, scanner and BSL analyzer versions; project and revision identifiers; source manifest or hashes; scanner configuration; `report-task.txt` fields; Compute Engine task identifier and terminal status; analysis identifier; quality-gate result; and every issues page with its page number, page size and reported total. A static finding remains a hypothesis until it is linked to the relevant ERP document, movement, register, posting or report evidence and survives Gate 7 adversarial review.

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
