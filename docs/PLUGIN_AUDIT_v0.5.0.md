# Plugin audit — v0.5.0

Status: release candidate, acceptance pending. No known critical control is intentionally relaxed. This is a scoped source/control inventory; it does not declare runtime acceptance before the release-specific checks pass.

- The 35 packaged skills, primary dynamic entrypoint and strict 26-case `EVAL_RESULT_JSON` contract are retained. Unica remains pinned at 0.13.0 and the five-plugin catalog is unchanged.
- The file viewer retains immutable import/export and performs no connection or case upload merely by opening a file.
- The opt-in workbench validates literal loopback endpoints, exact expected metadata names, explicit test scope, existing sign-in, short memory-only sessions, Host/Origin, CSRF, bounded bodies and a fixed API allowlist.
- Source responses and scenario inputs retain hashes and independent derived-artifact lineage. Notes do not mutate sources; Gates are never automatically passed. ZIP export verifies a file allowlist and excludes unrelated private files.
- Fixed-command first-party bridge source is separately reviewed and has no arbitrary query/BSL/write entrypoint. Compilation, installed applicability, auth and live reads require distinct evidence. Legacy bridge server capability is not misrepresented as read-only.
- UI SDK controls retain names, password redaction, confirmation markers and shared human/agent callbacks. Confirmation markers do not replace backend authorization.

Required before final release: complete Python/UI/build checks, native bridge and browser checks, CodeQL/protected PR CI, exact-candidate clean Codex acceptance, merged-tree equality and verification after local installation. Results and hashes belong in the release PR/private acceptance record, not in fabricated source claims.
