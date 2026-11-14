# v0.3.11 — Local test-contour evidence

Static XML/CFE checks cannot show what a test base actually returned. This candidate adds an optional read-only HTTP evidence adapter and offline verifier, inspired by the reviewed Test Bridge article and protocol. It supports Health, Metadata, Describe and Query in an explicitly identified loopback test contour, records raw hashes and case context, and refuses to call a bounded query a complete accounting export.

The package contains 34 skills. The five-plugin marketplace, pinned companions, strict `EVAL_RESULT_JSON` contract, 26-case suite and approved Velis artwork remain intact. No upstream code or CFE is bundled; redistribution is deferred because the reviewed msrv-tech snapshot has no verified license grant. Report/print-form rendering is documented as separately authorized external-code execution with output and business assertions.

Unchanged companion pins:

| Companion | Immutable commit |
|---|---|
| Unica 0.12.3 | `c02e38d44a7dc238310172b9d790487f81aa4fb4` |
| 1C Skills PowerShell | `8cb7868145281d8e353831512cc1ffa72f1b5c89` |
| 1C Skills Python | `c1f79f5ac9f31c620b8508f75464f8c42c559ae4` |
| Jev 0.1.0 | `cf7e76607d4ec70592b24becadd0296dcda8177a` |

Validation: synthetic loopback HTTP tests exercise UTF-8, contour mismatch, allowlisted commands, proxy/redirect isolation, invalid JSON/counts, response limits, offline context checks and file tampering. Repository checks must pass before publication. These fixtures are not live 1C acceptance.

Protected PR CI and CodeQL, exact installed v0.3.11 clean-session acceptance, and an actual identified test-contour smoke remain separate gates. No production base, external publication or global Plugin Directory release is changed by this candidate. The 0.3.8 acceptance does not transfer. Rollback is reverting this candidate/plugin version; the adapter never mutates 1C or publication settings.
