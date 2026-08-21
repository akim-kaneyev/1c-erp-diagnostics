# SonarQube BSL evidence checklist

## Gate 0: availability and boundary

- verify that the SonarQube endpoint, scanner and BSL analyzer are actually available;
- never infer `unavailable` merely because no dedicated SonarQube MCP/app/tool name is listed; when local execution and loopback HTTP exist, perform the factual endpoint and scanner probes;
- if host permission blocks those read-only probes, record `confirmation_required` with reason `host_execution_confirmation_required` instead of inventing an unavailable runtime;
- default to a user-managed loopback-only endpoint;
- confirm that the source is sanitized and minimized before scanning, because SonarQube stores analyzed source and derived analysis data;
- classify an existing-report read as R0 and a sanitized loopback-local scan as R1;
- classify project or token creation/deletion and quality-profile changes as R2, require action-time confirmation, and never perform them automatically;
- keep every non-loopback endpoint `prohibited` for `sonarqube-bsl-local`; remote source upload/external write would be R3 and requires a separate reviewed workflow, exact transmission approval and HTTPS;
- treat an approved read of an already existing remote report as a separate R0 capability, not as availability of the local adapter;
- stop if the endpoint, ownership, transport or data boundary cannot be verified.

## Credentials

- never store or paste scanner or API tokens in chat, source, configuration, reports, logs or command-line arguments;
- pass the scanner token only to the scanner child process in `SONAR_TOKEN`;
- use a separate least-privilege API token, injected only for the API child process and sent as `Authorization: Bearer`;
- redact authorization headers and token-bearing environment variables from all captured evidence;
- stop if token isolation or log redaction cannot be guaranteed.

## Scanner workspace

- create a new adapter-owned disposable working directory beneath an adapter-owned temporary root;
- set the scanner working-directory option explicitly to that directory;
- use a dedicated empty leaf, resolve root/leaf immediately before invocation and cleanup, reject reparse/symlink targets and prove containment;
- never reuse a user-owned, repository-owned or pre-existing directory, because the scanner may delete and recreate its working leaf;
- preserve only sanitized evidence artifacts needed for provenance, then remove the disposable working directory through the approved cleanup path.

## Provenance and completion

- record the SonarQube server, scanner and BSL analyzer names and versions;
- record sanitized project, revision and configuration identifiers plus a manifest or hashes of scanned inputs;
- preflight the exact existing project with a project analysis token and abort before scanner invocation if it is absent or mismatched; do not claim a nonexistent scanner auto-create toggle;
- preserve the sanitized fields from `report-task.txt`, including after a non-zero scanner exit, and same-origin validate the Compute Engine URL/identifier;
- wait for terminal Compute Engine `SUCCESS`, `FAILED` or `CANCELED`; require `SUCCESS` plus `analysisId` before requesting the quality gate, and keep scanner/CE/quality-gate states separate;
- mark a timeout `submitted`/incomplete and do not automatically submit a duplicate analysis;
- retrieve issues with fixed project/language filters; record query, page number/size, returned count and total, deduplicate issue keys, and require a stable total equal to unique collected keys before `complete=true`;
- mark pagination incomplete on errors, repeated/missing pages, changing totals, duplicate conflicts or server result-window limits;
- keep API payloads or normalized reports only after credential and confidential-data review.

## Diagnostic interpretation

- distinguish syntax, reliability, security and maintainability findings from an ERP accounting cause;
- link every relied-on finding to the actual document, movement, register, posting, calculation or report chain;
- mark unmatched or unreachable findings as hypotheses, not established causes;
- apply Gate 7 adversarial review to the proposed causal chain and test reasonable alternatives;
- do not auto-fix BSL, change a quality profile, accept an issue, or write to GitHub as part of diagnostic analysis.
