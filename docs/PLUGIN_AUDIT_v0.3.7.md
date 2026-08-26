# Plugin self-audit — v0.3.7

## Scope

Read-only self-audit of the v0.3.7 release candidate after reproducing the installed
v0.3.6 `under-evidenced-cost` output.

## Confirmed correction

- Gate 2 completion is separated from expected-but-missing evidence.
- Gate 4 remains blocked when an exact cause lacks registrar/movement/register/mechanism evidence.
- Gate 7 passes when it rejects the unsupported exact cause.
- Gate 10 remains blocked while the exact-cause goal is unresolved.
- Strict claims use `id`, `status`, `text`, `evidence_ids`, `falsifier`.
- The user-reported symptom is not promoted to an established root-cause claim.
- Requested evidence is string-only and evidence requests are not pseudo-actions.
- The exact v0.3.6 response is an executable rejected regression.

## Preserved invariants

- 32 packaged skills.
- Stable marketplace identity and four-plugin order.
- Immutable companion pins.
- Velis assets and independent-project trademark boundary.
- SonarQube safety, artifact provenance, execution identity and full-history checks.
- Runtime acceptance remains distinct from repository CI.

## Gate assessment

No known critical control failure remains in the repository contract after the hotfix.
This statement does not claim runtime acceptance. A new installed v0.3.7 clean-session
run and the complete hashed 16-case acceptance are still required.
