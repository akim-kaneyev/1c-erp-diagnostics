# Roadmap

## 0.1.x — public foundation

- complete clean-session plugin smoke tests;
- publish the source repository when the release checklist is green;
- validate `@one-c-erp-diagnostics` from an independent ChatGPT chat;
- collect sanitized failure cases for regression testing.

## 0.2.x — evidence tooling

- improve XLSX structural comparison;
- [x] add deterministic synthetic eval manifests, machine-readable result validation and a strict clean-session runtime gate;
- evaluate safe MXL conversion adapters only when a format/tool is verified;
- [x] add regression coverage for principal ERP domains, insufficient evidence, unavailable capabilities, Gate 7 and scoped `R3 / NO-GO`;

## 0.3.x — local static analysis and optional isolated execution

- [x] add the optional `sonarqube-bsl-local` Gate 0/Gate 5 adapter with safe provenance and fallback;
- [x] classify local scan, SonarQube administration and remote upload under `R1–R3` controls;
- [x] require factual loopback/scanner discovery instead of inferring SonarQube availability from named-tool inventory;
- formalize OpenSandbox recipes for parser/tool testing;
- add reproducible environment definitions and egress controls;
- keep sandbox optional and data-minimized.

## Future — controlled integrations

Consider a custom MCP/server only when a concrete server-side capability is required and privacy/authentication implications are fully specified. The core diagnostic method should remain usable without a custom backend.
