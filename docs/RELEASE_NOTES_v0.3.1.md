# 1C ERP Diagnostics v0.3.1 — Factual SonarQube Discovery

## Overview

Version 0.3.1 fixes the Gate 0 classification path reported after installing v0.3.0 in another Codex project. The orchestrator was active and routed the 1C:ERP case correctly, but it treated the absence of a dedicated SonarQube tool name as proof that the local SonarQube adapter was unavailable. That inference skipped the documented loopback and scanner preflight.

## Fixed behavior

- a dedicated SonarQube MCP server, app or named tool is no longer required for discovery;
- when local process execution and loopback HTTP are available, Gate 0 must actually request the local server status/version and invoke the scanner version command;
- a host permission block becomes `confirmation_required / host_execution_confirmation_required`;
- an authenticated endpoint returning `401/403` preserves already observed server/scanner facts and becomes `confirmation_required / authentication_required`;
- `unavailable` requires a missing component or endpoint after a factual probe;
- no service is started, no default credential is tried and no project, token or profile is created during discovery.

The correction does not make a scan automatic. A sanitized local scan remains `R1`; SonarQube project/token/profile administration remains `R2`; remote source transfer remains outside the local capability and requires a separate `R3` workflow.

## Unchanged safety and ecosystem

- static findings remain hypotheses until runtime and the `document → movement → register/record → mechanism → result → symptom` chain are proven and challenged at Gate 7;
- scanner/API credentials remain prohibited in commands, properties, files, logs, state, Git and chat;
- the approved Velis assets are unchanged;
- the stable marketplace ID remains `one-c-erp-diagnostics-marketplace` with exactly four entries;
- companion pins remain unchanged: Unica `aefc880f9bab606a5c55ed11af563b740054a549`, 1C Skills PowerShell `8cb7868145281d8e353831512cc1ffa72f1b5c89`, and 1C Skills Python `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`.

## Release validation

Before publication, the patch must pass the public-package and ecosystem validators, the 14-case eval suite, the regression tests on Python 3.10/3.12 and CodeQL on the protected release Pull Request. Exact-version clean-session acceptance remains pending until the installed v0.3.1 package reproduces factual Gate 0 discovery without exposing a credential.

## Upgrade

Refresh the existing marketplace installation after v0.3.1 is published, ensure only the marketplace copy of `one-c-erp-diagnostics` is enabled, and start a new task so Codex loads the updated skill inventory.
