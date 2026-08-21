# 1C ERP Diagnostics v0.3.0 — Optional SonarQube BSL Evidence

## Overview

Version 0.3.0 adds an optional local SonarQube capability for reproducible static analysis of 1C BSL source. SonarQube output is treated as one evidence source inside the existing Gate 0–10 workflow, not as an automatic diagnosis or permission to change code.

The marketplace remains upgrade-compatible: its internal ID is unchanged and it still contains exactly four plugins. The primary plugin now packages 32 skills.

## Included

- optional capability identifier `sonarqube-bsl-local`;
- one packaged skill for SonarQube BSL analysis and evidence capture;
- verified local reference baseline:
  - SonarQube Community Build `26.8.0.126808`;
  - SonarScanner CLI `8.0.1.6346`;
  - communitybsl plugin `1.20.0`;
  - communitybsl SHA-256 `595F741AFD49BC7F1869B3F82F623821D519CECB399C56F154E55EA83DC7057B`;
- provenance requirements for server, scanner and language-plugin versions, analysis identifiers and result location;
- environment-only token handling;
- executable evaluation and runtime-acceptance gates in the public-release contract.
- unchanged approved Velis assets and trademark boundary.

The reference versions document the verified baseline. The plugin does not bundle SonarQube, the scanner, Java or communitybsl, and it must not invent their runtime availability. Gate 0 discovers the capability for each case.

The release-candidate read-only preflight confirmed the local server as `UP`, the scanner version and the reviewed BSL JAR digest. Authenticated plugin/language/profile/project discovery returned `401` without a scoped token; no token or project was created and no scan was simulated. The full local scan path therefore remains `confirmation_required` until its separately authorized runtime smoke test.

## Safety and authorization boundary

SonarQube operations use the following risk classes:

| Operation | Risk | Required control |
|---|---:|---|
| Analyze local sanitized source on an already configured local instance | `R1` | State exact scope and record derived artifacts. |
| Create or change a SonarQube project, user token or administrative setting | `R2` | Obtain explicit approval for the exact administrative change. |
| Upload source to a remote SonarQube instance | `R3` | Outside `sonarqube-bsl-local`; requires a separately reviewed workflow, exact destination/data-scope approval and HTTPS. |

Tokens must be supplied through an environment variable at execution time. They must not be written to scanner properties, repository files, reports, logs, case state or chat transcripts. Logs and evidence exports must be checked for accidental credential exposure before retention.

## Diagnostic evidence contract

A SonarQube issue is a static-analysis finding and therefore a hypothesis. It cannot by itself establish the runtime cause of an ERP symptom. A final `УСТАНОВЛЕНО` still requires the evidence chain:

`document → movement → register/record → consuming mechanism → accounting/stock/access result → symptom`

The analysis record must preserve the source scope and identity, tool versions, project or analysis identifier, relevant rule and location, result artifact identity, and any limitations. Gate 7 must challenge the proposed causal link and plausible alternatives before final acceptance.

Automatic code correction, issue acceptance, quality-gate override, SonarQube administration and GitHub writes are outside analysis-only authorization.

## Marketplace compatibility

The stable marketplace installation ID remains:

```text
one-c-erp-diagnostics-marketplace
```

The marketplace still contains exactly four entries, in the established order:

1. 1C ERP Diagnostics;
2. Unica;
3. 1C Skills PowerShell;
4. 1C Skills Python.

The existing immutable companion source pins are unchanged. SonarQube is a dynamically discovered external capability, not a fifth marketplace plugin or a hard installation dependency.

Verified companion refs retained by this release:

- Unica: `aefc880f9bab606a5c55ed11af563b740054a549`;
- 1C Skills PowerShell: `8cb7868145281d8e353831512cc1ffa72f1b5c89`;
- 1C Skills Python: `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`.

## Release and runtime acceptance

The executable evaluation suite and runtime-acceptance contract remain part of the release gate. Before publication, the candidate must pass local validators and tests, then GitHub CI and CodeQL on the release Pull Request. A clean-session runtime run must verify Gate 0 discovery, safe under-evidenced behavior, the scoped `R3 / NO-GO` path, and the SonarQube capability's available and unavailable paths without exposing a credential.

The assembled local candidate passed the public-package, ecosystem, 14-case eval and 31-test regression checks. GitHub CI, the release Pull Request, tag, GitHub release and clean-session runtime acceptance for `0.3.0` remain pending. These notes do not assert that the version has been published.

## Upgrade guidance

After `0.3.0` is published, refresh the existing marketplace installation so the host receives the new packaged skill and updated contracts. No marketplace uninstall or ID migration is intended.
