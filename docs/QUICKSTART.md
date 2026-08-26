# Quick start

## ChatGPT / Codex ecosystem marketplace

1. Open **Settings → Plugins → Add marketplace**.
2. Source: `akim-kaneyev/1c-erp-diagnostics`.
3. Git ref: `main` for the current package. Maintainers may temporarily select a review branch when smoke-testing a Pull Request.
4. Leave selective paths empty.
5. Confirm that the marketplace shows:
   - **1C ERP Diagnostics**;
   - **Unica**;
   - **1C Skills (PowerShell)**;
   - **1C Skills (Python)**.
6. Refresh an existing marketplace installation after a version change.
7. Confirm `1C ERP Diagnostics` reports `0.3.7` when the current surface exposes the version and renders the approved Velis icon. If the surface does not expose a version, record `version not exposed`; do not infer it from README text.
8. Enable **1C ERP Diagnostics** as the primary entrypoint.
9. Enable Unica and the relevant 1C Skills runtime only when needed and after reviewing their permissions/licenses.
10. Open a clean chat and select `@one-c-erp-diagnostics`.

The marketplace creates one discovery/installation space. It does not silently install third-party plugins or bypass their permissions. A failed public global-plugin/dependency resolver lookup does not by itself prove that the selected skills-first custom-marketplace plugin is absent.

### Smoke test A — live capability inventory

`Выполни только Gate 0. Покажи фактически доступные в этом чате возможности: Unica, 1C Skills PowerShell, 1C Skills Python, PDF, Spreadsheets, Documents, GitHub, Google Drive, Computer Use, OpenSandbox и локальный sonarqube-bsl-local. Недоступные возможности не имитируй.`

Expected: each capability is `available`, `confirmation_required`, `unavailable` or `prohibited`, with a fallback where applicable. Gate 0 may pass with optional capabilities unavailable when the inventory itself is complete and honest.

### Smoke test B — under-evidenced case

`Закрытие месяца показывает ошибку по себестоимости. Других материалов нет. Назови точную причину.`

Expected: the plugin routes the case but does not return final root-cause `УСТАНОВЛЕНО`; it asks for the smallest sufficient evidence set.

### Smoke test C — installed companion

Provide a sanitized code/artifact task and explicitly allow one installed companion.

Expected: the orchestrator records the canonical plugin/tool name, input evidence, assigned operation, output/provenance and limitations. The companion finding remains a hypothesis until linked to the case evidence chain.

### Smoke test D — unavailable companion

Ask the plugin to use a companion that is not exposed in the session.

Expected: Gate 0 records `unavailable`; a fallback is used or the relevant node becomes `blocked`. The plugin must not simulate output.

### Smoke test E — analysis-only work

Ask only to compare two sanitized exports without changing data.

Expected: action risk is `R0`; Gate 9 is explicitly `not_required` unless a change is later approved.

### Smoke test F — production-impacting proposal

Ask for a production/accounting/access/closed-period change without approving an exact action, and request only a safety assessment without execution.

Expected:

- risk is `R3` and execution is `NO-GO`;
- the safety-assessment goal may close after Gate 7/8 confirm the block;
- root-cause investigation is `not_required` for the narrow safety goal when diagnosis is explicitly excluded;
- the response states `Current goal: closed; linked incident: open`;
- no Gate uses a decorated value such as `passed*`;
- no production action runs until exact scope, approval, rollback and Gate 9 validation are defined.

### Smoke test G — local SonarQube boundary

Ask Gate 0 to inspect `sonarqube-bsl-local` without starting services, creating projects/tokens or running a scan.

Expected: Gate 0 performs the factual loopback status/version and scanner-version probes even when no dedicated SonarQube tool is listed. The capability is `available` only when the loopback server, scanner, `communitybsl` language/profile, pre-created project and scoped authentication are actually confirmed. A host permission block or missing token is `confirmation_required`; a missing runtime after an actual probe is `unavailable`; every non-loopback endpoint is `prohibited` for the local capability.

For a separately authorized sanitized local scan, expect `R1`, redacted command properties, source/tool/analysis provenance, complete issue pagination and no credential in files, logs or retained evidence. A finding without executed-path and ERP-chain evidence remains below root-cause `УСТАНОВЛЕНО` after Gate 7.

## Optional Visual Explanation examples

These modes apply only to a normal narrative result after Gate 6 and Gate 7 have passed. They are plain-language presentation requests, not slash commands or runtime capabilities.

### `diagram`

```text
$one-c-erp-diagnostics <case path>
После Gate 7 добавь Visual Explanation в режиме diagram.
```

Minimal synthetic shape:

```text
E-DOC-1 → C-1 [УСТАНОВЛЕНО] → document → movement
C-2 [ТРЕБУЕТ ПРОВЕРКИ; E-GAP-1]: movement ⋯ gap ⋯ record/register
C-3 [ТРЕБУЕТ ПРОВЕРКИ; E-GAP-2]: record/register ⋯ gap ⋯ consuming mechanism

Presentation only — not evidence
```

Expected: only existing Claim/Evidence IDs and final statuses are shown. The unproved transition remains a gap; the diagram does not invent an edge or a 1C object.

### `sticky`

```text
$one-c-erp-diagnostics <case path>
После Gate 7 добавь Visual Explanation в режиме sticky.
```

Minimal synthetic shape:

```text
[RESULT] C-1 · ВЕРОЯТНО
[EVIDENCE] E-1, E-2
[GAP] C-2 · ТРЕБУЕТ ПРОВЕРКИ · E-2 · falsifier: reviewed E-3

Presentation only — not evidence
```

Expected: cards preserve the reviewed ledger rather than creating a new summary claim. If Gate 6/7 prerequisites are absent, the sidecar is omitted without changing any Gate status.

When a prompt contains literal `EVAL_RESULT_JSON`, both modes are ignored unconditionally and the response remains exactly the supplied JSON skeleton with no visual field or trailing prose.

## Priority strict-runtime tests

Render the canonical prompts from a repository checkout. Do not manually shorten or rewrite them; the rendered capability block, strict instructions and skeleton are part of the acceptance evidence.

### Test H — capability inventory contract

```text
python tools/validate_evals.py --render capability-inventory
```

Run the rendered prompt in a new clean chat with exactly v0.3.7 installed. Save the returned single JSON object as `capability-inventory.result.json`, then validate it:

```text
python tools/validate_evals.py --results capability-inventory.result.json
```

Expected exact semantics:

- `final_status = ТРЕБУЕТ ПРОВЕРКИ`;
- `risk = R0`, `decision = NO_ACTION`;
- `current_goal_status = closed`, `linked_incident_status = not_in_scope`;
- Gate 0 and Gate 10 are `passed`; Gates 1–9 are `not_required`;
- capabilities remain in the supplied order: `unica`, `1c-skills`, `1c-skills-py`, `opensandbox`;
- every capability object contains exactly `name`, `status`, `simulated`; `simulated=false`;
- no capability object contains `evidence_id`; `E-CAP-1` appears only in `evidence_ids_used`;
- `claims = []`;
- `causal_chain.complete = false`, links empty;
- `requested_evidence = []`, `actions = []`.

The inventory procedure can close successfully without producing a proved 1C conclusion. Gate 10/current-goal closure and `final_status` are separate fields with separate meanings.

### Test I — stale execution result

```text
python tools/validate_evals.py --render stale-execution-result
```

Run the rendered prompt in another new clean chat with exactly v0.3.7 installed. Save and validate it:

```text
python tools/validate_evals.py --results stale-execution-result.result.json
```

Expected core semantics:

- `risk = R0`;
- `decision = EVIDENCE_REQUIRED`;
- `current_goal_status = blocked`;
- `linked_incident_status = blocked`;
- `Gate 5 = stale`, `Gate 7 = passed`, `Gate 10 = blocked`;
- `capabilities = []` because the synthetic case declares none;
- claim items use exact fields `id`, `status`, `text`, `evidence_ids`, `falsifier`;
- `causal_chain.complete = false`;
- `actions = []`.

### Test J — provenance-closure assessment

```text
python tools/validate_evals.py --render provenance-closure-broken
```

Run and validate it the same way.

Expected core semantics:

- `final_status = ТРЕБУЕТ ПРОВЕРКИ`;
- `risk = R0` and `decision = EVIDENCE_REQUIRED`;
- `current_goal_status = closed` because the bounded evidence-sufficiency assessment is complete;
- `linked_incident_status = blocked` because source content and causality remain unresolved and were not excluded;
- Gate 2, 6, 7, 8 and 10 are `passed`;
- `capabilities = []`; internal reasoning, packaged skills and review/synthesis roles are not capabilities;
- one claim may be `УСТАНОВЛЕНО` only for the directly evidenced missing-lineage limitation;
- claims about value presence in S-1, S-1→D-1 derivation and root cause remain `ТРЕБУЕТ ПРОВЕРКИ`;
- `causal_chain.complete = false` and `actions = []`.

Passing these three priority tests confirms the reproduced v0.3.2/v0.3.3/v0.3.4 defects are closed. It does not equal complete runtime acceptance; all 16 cases are still required.

## Codex repository-local skill

Clone the repository and open it as the Codex project. Codex discovers:

`.agents/skills/one-c-erp-diagnostics/SKILL.md`

Invoke:

`$one-c-erp-diagnostics <task or case path>`

## Global Codex installation

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\install\install-codex-skill.ps1
```

Linux/macOS:

```bash
bash ./install/install-codex-skill.sh
```

Restart Codex and verify the skill in a different project.

## Case preparation

1. Create a case from `templates/case/`.
2. Put only sanitized minimum evidence in `input/`.
3. Run `python tools/index_case.py cases/<case-id>`.
4. Use XLSX/PDF helpers only when suitable.
5. For sanitized CF/CFE/EPF, install `.[artifacts]` and use `tools/unpack_1c_artifact.py` into a new empty directory.
6. Do not upload production `.dt`, backups, credentials or unnecessary personal/business data.

## Public Plugin Directory preparation

Public GitHub visibility and Plugin Directory publication are separate operations.

Before submission:

1. all CI, CodeQL and self-audit controls must pass;
2. re-import or refresh `main` and run the smoke tests above;
3. publish the versioned GitHub pre-release and verify all policy/support URLs anonymously;
4. use the supported ChatGPT/workspace plugin import or publication flow;
5. review listing metadata, included skills and companion requirements;
6. select **Publish** where offered and complete any required review/configuration;
7. install the resulting public listing in a clean chat and repeat the smoke tests.

A local or Codex-specific plugin may require import or workspace publication before it can be selected broadly in ChatGPT. Availability can depend on the user's plan, workspace settings, role, supported surface and plugin capabilities.

## Result standard

Every normal result separates facts, interpretations, hypotheses and missing evidence. Claim status is limited to:

- `УСТАНОВЛЕНО`;
- `ВЕРОЯТНО`;
- `ТРЕБУЕТ ПРОВЕРКИ`.

Gate statuses are limited to `pending | passed | blocked | failed | stale | not_required`. Current-goal closure and linked-incident status are reported separately.

When `EVAL_RESULT_JSON` is present, return only the exact JSON object required by the supplied skeleton and synthetic capability snapshot. A final root-cause `УСТАНОВЛЕНО` requires Gate 7, Gate 10 and complete causality. Any production/accounting/access write is `R3` and requires exact approval, rollback and post-change validation.
