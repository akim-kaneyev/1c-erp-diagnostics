# 1C binary artifacts and BSL checklist

## Before extraction

- record filename, size and SHA-256;
- confirm sanitization and absence of secrets;
- do not load the artifact into a working/test information base merely to read it;
- do not execute untrusted BSL;
- stop on an unsupported or damaged format.

## CF/CFE/EPF extraction

- use `tools/unpack_1c_artifact.py` with the pinned optional dependency;
- use a new empty output directory;
- preserve `_extraction_manifest.json`;
- verify that extracted BSL/JSON count is non-zero when expected;
- do not use rebuild mode in diagnostic work.

## Static analysis

- for local SonarQube, apply `checklists/sonarqube-bsl.md` and route through `one-c-erp-local-static-analysis`;
- record analyzer/server/scanner versions, sanitized configuration, redacted command, source manifest and report hash;
- distinguish syntax/style findings from an accounting cause;
- link the code path to an actual event, movement, register record or calculation;
- test reasonable alternatives.

## Stop conditions

- encryption/corruption;
- version differs from the reviewed pin;
- evidence requires executing unknown code;
- no link between code and the factual case chain.
- token isolation, loopback ownership or the scanner working-directory boundary cannot be verified.
