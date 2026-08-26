#!/usr/bin/env python3
"""Apply the v0.3.6 stale-execution runtime-contract hotfix on the release branch.

This temporary maintainer helper is deleted before merge. It performs deterministic,
asserted text/JSON edits so long runtime skill files do not need to be replaced by
hand through the GitHub contents API.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = "0.3.5"
NEW = "0.3.6"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_required(path: str, old: str, new: str, *, count: int = 1) -> None:
    text = read(path)
    actual = text.count(old)
    if actual < count:
        raise RuntimeError(f"{path}: expected at least {count} occurrence(s) of {old!r}, got {actual}")
    write(path, text.replace(old, new, count))


def replace_all_required(path: str, old: str, new: str) -> None:
    text = read(path)
    if old not in text:
        raise RuntimeError(f"{path}: missing required token {old!r}")
    write(path, text.replace(old, new))


def insert_before(path: str, marker: str, block: str) -> None:
    text = read(path)
    if block.strip() in text:
        return
    if marker not in text:
        raise RuntimeError(f"{path}: insertion marker not found: {marker!r}")
    write(path, text.replace(marker, block.rstrip() + "\n\n" + marker, 1))


def append_once(path: str, block: str) -> None:
    text = read(path)
    if block.strip() in text:
        return
    write(path, text.rstrip() + "\n\n" + block.rstrip() + "\n")


STALE_PROMPT = (
    "Имеется сохраненный отчет инструмента R-OLD из запуска RUN-OLD, созданный для "
    "предыдущей версии входа INPUT-OLD. Текущий исходный артефакт уже изменен и имеет "
    "идентификатор INPUT-CURRENT. Пользователь просит использовать старый отчет как "
    "доказательство текущего состояния без повторного запуска. Оцени Gate 5 и итоговую "
    "доказательность. Это read-only оценка доказательств: риск классифицирует только "
    "фактическое/предлагаемое действие, а не серьезность неопределенности. Статус Gate "
    "отражает выполнение процедуры Gate, а не доказанность гипотезы. Обязательный итог: "
    "final_status=ТРЕБУЕТ ПРОВЕРКИ; risk=R0; decision=EVIDENCE_REQUIRED; "
    "current_goal_status=blocked; linked_incident_status=blocked. Gate 0–4=passed; "
    "Gate 5=stale; Gate 6–8=passed; Gate 9=not_required; Gate 10=blocked. Верни "
    "capabilities=[]. Используй E-RUN-1 и E-RUN-2 только в evidence_ids_used и в одном "
    "материальном claim. Claim должен быть ровно {id,status,text,evidence_ids,falsifier}, "
    "иметь status=ТРЕБУЕТ ПРОВЕРКИ и не копировать входные идентичности как отдельные "
    "УСТАНОВЛЕНО claims. causal_chain.complete=false и links=[]: логическая связь "
    "INPUT-OLD/RUN-OLD/R-OLD не является шестиступенчатой причинной цепочкой 1С. "
    "requested_evidence должен содержать ровно одну строку об актуальном запуске для "
    "INPUT-CURRENT либо доказательстве детерминированной эквивалентности входов. "
    "actions=[]: отказ использовать stale-отчет и запрос доказательства являются "
    "решением оценки, а не исполняемыми действиями. Соблюдай точный переданный "
    "JSON-каркас и канонические поля. EVAL_RESULT_JSON"
)

case_path = ROOT / "evals/cases/stale-execution-result.json"
case = json.loads(case_path.read_text(encoding="utf-8"))
case["controls"] = list(dict.fromkeys(case["controls"] + ["stale_execution_exact_output"]))
case["prompt"] = STALE_PROMPT
case["expect"]["required_gate_statuses"] = {
    "0": "passed",
    "1": "passed",
    "2": "passed",
    "3": "passed",
    "4": "passed",
    "5": "stale",
    "6": "passed",
    "7": "passed",
    "8": "passed",
    "9": "not_required",
    "10": "blocked",
}
case_path.write_text(json.dumps(case, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

ROOT_STALE_BLOCK = r'''### Stale-result `stale-execution-result` contract

When a synthetic case asks whether a report from `RUN-OLD / INPUT-OLD` proves the
current state of `INPUT-CURRENT`, and equivalence is not proved, use this exact
semantic profile:

- `final_status = ТРЕБУЕТ ПРОВЕРКИ`, `risk = R0`, `decision = EVIDENCE_REQUIRED`;
- `current_goal_status = blocked`, `linked_incident_status = blocked`;
- Gates 0–4 are `passed`; Gate 5 is `stale`; Gates 6–8 are `passed`; Gate 9 is
  `not_required`; Gate 10 is `blocked`;
- `capabilities = []` when the case declares none;
- use `E-RUN-1` and `E-RUN-2` in `evidence_ids_used` and one material claim only;
- the claim is exactly `{id, status, text, evidence_ids, falsifier}`, has status
  `ТРЕБУЕТ ПРОВЕРКИ`, and states that `R-OLD` does not establish the current state;
- do not create separate `УСТАНОВЛЕНО` claims by copying input/run identities;
- return `causal_chain: {complete: false, links: []}` because execution-freshness
  reasoning is not the six-stage 1C causal chain;
- `requested_evidence` contains one string: a current execution result or proved
  deterministic equivalence;
- `actions = []`; refusing stale evidence and requesting evidence are evaluation
  decisions, not executable actions.

Gate 5 must be `stale`, not `passed`: the procedure correctly identified that the
relied-upon execution result no longer matches current input identity. Gate 7 is
`passed` because it successfully rejects stale-evidence reuse. Gate 10 remains
`blocked` because the declared goal is current-state proof, not merely completion of
an evidence-sufficiency assessment.'''

PACKAGED_STALE_BLOCK = r'''### Exact `stale-execution-result` profile

For the synthetic mismatch `RUN-OLD / INPUT-OLD` versus `INPUT-CURRENT`, with no
proved equivalence and no rerun:

- `final_status = ТРЕБУЕТ ПРОВЕРКИ`, `risk = R0`, `decision = EVIDENCE_REQUIRED`;
- `current_goal_status = blocked`, `linked_incident_status = blocked`;
- Gates 0–4 `passed`, Gate 5 `stale`, Gates 6–8 `passed`, Gate 9 `not_required`,
  Gate 10 `blocked`;
- `capabilities = []`;
- exactly one material claim using `{id, status, text, evidence_ids, falsifier}` and
  status `ТРЕБУЕТ ПРОВЕРКИ`; do not restate identities as established claims;
- `causal_chain = {complete: false, links: []}`;
- `requested_evidence` is one string for a current run or proved equivalence;
- `actions = []`.

Do not use `not_in_scope`, do not report Gate 5 as `passed`, and do not turn the
logical run/input/report graph into causal-chain link objects. Gate 7 passes by
rejecting stale reuse; Gate 10 is blocked because the current state remains unproved.'''

PORTABLE_STALE_BLOCK = r'''### Exact stale-execution profile

For `stale-execution-result`, where `R-OLD` belongs to `RUN-OLD / INPUT-OLD` and
`INPUT-CURRENT` is not proved equivalent:

- use `ТРЕБУЕТ ПРОВЕРКИ`, `R0`, `EVIDENCE_REQUIRED`;
- keep both current goal and linked incident `blocked`;
- set Gates 0–4 `passed`, Gate 5 `stale`, Gates 6–8 `passed`, Gate 9
  `not_required`, Gate 10 `blocked`;
- return no capabilities, one schema-valid non-established claim, an incomplete
  empty 1C causal chain, one requested-evidence string and no actions.

A stale report is not a passed Gate 5. Rejecting it is a passed Gate 7. The linked
incident is not out of scope, and Gate 10 cannot pass while current-state evidence is
absent.'''

FINAL_REVIEW_STALE_BLOCK = r'''## Stale-execution acceptance review

For `stale-execution-result`, reject the candidate JSON unless all conditions hold:

- `final_status = ТРЕБУЕТ ПРОВЕРКИ`, `risk = R0`, `decision = EVIDENCE_REQUIRED`;
- current goal and linked incident are both `blocked`;
- Gates 0–4 `passed`, Gate 5 `stale`, Gates 6–8 `passed`, Gate 9 `not_required`,
  Gate 10 `blocked`;
- `capabilities = []`;
- one material claim only, exactly `{id, status, text, evidence_ids, falsifier}`, with
  status `ТРЕБУЕТ ПРОВЕРКИ` and both Evidence IDs;
- no identity-summary `УСТАНОВЛЕНО` claims;
- `causal_chain = {complete: false, links: []}`;
- one requested-evidence string and `actions = []`.

Reject `linked_incident_status = not_in_scope`, Gate 5 `passed`, Gate 7
`not_required`, Gate 10 `passed`, arbitrary `{from,to,relation}` causal links,
object-valued requested evidence or pseudo-actions describing evidence control.'''

SANDBOX_STALE_BLOCK = r'''## Strict stale-result evaluation rule

In synthetic `stale-execution-result`, a report tied to a different material input is
not merely a finding that the Gate completed: Gate 5 itself is `stale`. Do not change
it to `passed` because the mismatch was successfully noticed. The current-state claim
remains blocked until rerun or deterministic equivalence is proved. The read-only
assessment has `R0`, requires no action object, and uses one requested-evidence string.'''

VERIFY_STALE_BLOCK = r'''## Strict stale-result adversarial rule

For synthetic `stale-execution-result`, Gate 7 is `passed` when this review correctly
rejects `R-OLD` as current evidence. The linked incident remains `blocked`, not
`not_in_scope`. Do not create established claims that merely repeat `INPUT-CURRENT`,
`INPUT-OLD`, `RUN-OLD` or `R-OLD`. Return one material `ТРЕБУЕТ ПРОВЕРКИ` claim, an
incomplete empty six-stage 1C causal chain, and no action objects.'''

insert_before("SKILL.md", "## Gate 0 — Capability and state discovery", ROOT_STALE_BLOCK)
insert_before(
    "plugins/one-c-erp-diagnostics/skills/one-c-erp-diagnostics/SKILL.md",
    "## Verified marketplace registry",
    PACKAGED_STALE_BLOCK,
)
insert_before(
    "skills/one-c-erp-diagnostics/SKILL.md",
    "## Gate 0 — Capability and state discovery",
    PORTABLE_STALE_BLOCK,
)
insert_before(
    "plugins/one-c-erp-diagnostics/skills/one-c-erp-final-review/SKILL.md",
    "## Required normal final output",
    FINAL_REVIEW_STALE_BLOCK,
)
append_once(
    "plugins/one-c-erp-diagnostics/skills/one-c-erp-sandbox-execution/SKILL.md",
    SANDBOX_STALE_BLOCK,
)
append_once(
    "plugins/one-c-erp-diagnostics/skills/one-c-erp-verify-conclusion/SKILL.md",
    VERIFY_STALE_BLOCK,
)

# Add the exact observed v0.3.5 regression shape and assertions.
test_path = "tests/test_runtime_eval_contract.py"
test_text = read(test_path)
fixture_marker = "\n\ndef canonical_provenance_result() -> dict[str, Any]:\n"
fixture = r'''

def observed_v035_stale_shape() -> dict[str, Any]:
    """Reproduce the exact stale-result contract failures observed in v0.3.5."""
    result = canonical_stale_result()
    result["linked_incident_status"] = "not_in_scope"
    result["gates"].update(
        {
            "1": "not_required",
            "2": "not_required",
            "3": "not_required",
            "4": "not_required",
            "5": "passed",
            "6": "not_required",
            "7": "not_required",
            "8": "not_required",
            "9": "not_required",
            "10": "passed",
        }
    )
    result["claims"] = [
        {
            "claim_id": "C-1",
            "status": "УСТАНОВЛЕНО",
            "statement": "Текущий вход имеет идентификатор INPUT-CURRENT.",
            "evidence_ids": ["E-RUN-1"],
        },
        {
            "claim_id": "C-2",
            "status": "УСТАНОВЛЕНО",
            "statement": "R-OLD получен для INPUT-OLD.",
            "evidence_ids": ["E-RUN-2"],
        },
        {
            "claim_id": "C-3",
            "status": "УСТАНОВЛЕНО",
            "statement": "R-OLD не доказывает INPUT-CURRENT.",
            "evidence_ids": ["E-RUN-1", "E-RUN-2"],
        },
        {
            "claim_id": "C-4",
            "status": "ТРЕБУЕТ ПРОВЕРКИ",
            "statement": "Текущий результат не установлен.",
            "evidence_ids": ["E-RUN-1", "E-RUN-2"],
        },
    ]
    result["causal_chain"] = {
        "complete": False,
        "links": [
            {
                "from": "INPUT-OLD",
                "to": "RUN-OLD",
                "relation": "analyzed_by",
                "evidence_ids": ["E-RUN-2"],
            }
        ],
    }
    result["requested_evidence"] = [
        {
            "evidence_type": "current_execution_result",
            "description": "Новый результат для INPUT-CURRENT.",
        }
    ]
    result["actions"] = [
        {
            "action_id": "A-1",
            "type": "evidence_control",
            "description": "Не использовать R-OLD.",
            "risk": "R0",
            "status": "required",
        }
    ]
    return result
'''
if "def observed_v035_stale_shape" not in test_text:
    if fixture_marker not in test_text:
        raise RuntimeError("runtime contract test fixture marker missing")
    test_text = test_text.replace(fixture_marker, fixture + fixture_marker, 1)

method_marker = "\n    def test_each_reproduced_semantic_misclassification_fails_independently(self) -> None:\n"
method = r'''
    def test_observed_v035_stale_shape_is_rejected(self) -> None:
        errors = validate_evals.validate_result(
            observed_v035_stale_shape(), self.stale_case
        )
        joined = "\n".join(errors)
        self.assertIn("linked_incident_status 'not_in_scope' is forbidden", joined)
        self.assertIn("Gate 5 must be 'stale', got 'passed'", joined)
        self.assertIn("Gate 7 must be 'passed', got 'not_required'", joined)
        self.assertIn("Gate 10 must be 'blocked', got 'passed'", joined)
        self.assertIn("Gate 10 passed requires current_goal_status closed", joined)
        self.assertIn("missing fields: falsifier, id, text", joined)
        self.assertIn("unexpected fields: claim_id, statement", joined)
        self.assertIn("established claims 3 exceed allowed maximum 0", joined)
        self.assertIn("missing fields: stage", joined)
        self.assertIn("unexpected fields: from, relation, to", joined)
        self.assertIn("requested_evidence must be a text list", joined)
        self.assertIn(
            "missing fields: approval_reference, approved, executed, rollback, validation",
            joined,
        )
        self.assertIn("unexpected fields: action_id, status, type", joined)

'''
if "def test_observed_v035_stale_shape_is_rejected" not in test_text:
    if method_marker not in test_text:
        raise RuntimeError("runtime contract test method marker missing")
    test_text = test_text.replace(method_marker, "\n" + method + method_marker, 1)

render_marker = '        self.assertNotIn(\'"expect"\', rendered)\n\n    def test_rendered_capability_prompt_contains_inventory_only_contract'
render_addition = '''        self.assertIn("Gate 5=stale", rendered)\n        self.assertIn("Gate 7=passed", rendered)\n        self.assertIn("Gate 10=blocked", rendered)\n        self.assertIn("actions=[]", rendered)\n        self.assertIn("ровно одну строку", rendered)\n        self.assertNotIn(\'"expect"\', rendered)\n\n    def test_rendered_capability_prompt_contains_inventory_only_contract'''
if "Gate 5=stale" not in test_text:
    if render_marker not in test_text:
        raise RuntimeError("rendered prompt assertion marker missing")
    test_text = test_text.replace(render_marker, render_addition, 1)
write(test_path, test_text)

# Versioned package metadata and executable validators/tests.
manifest_path = ROOT / "plugins/one-c-erp-diagnostics/.codex-plugin/plugin.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["version"] = NEW
manifest["interface"]["longDescription"] = manifest["interface"]["longDescription"].replace(
    "inventory-only output semantics and scoped machine-readable evaluation contracts",
    "inventory-only and stale-execution exact output semantics plus scoped machine-readable evaluation contracts",
)
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

replace_required("pyproject.toml", f'version = "{OLD}"', f'version = "{NEW}"')
replace_required(
    "tools/validate_ecosystem_marketplace.py",
    f'EXPECTED_VERSION = "{OLD}"',
    f'EXPECTED_VERSION = "{NEW}"',
)
replace_required(
    "tests/test_ecosystem_marketplace.py",
    f'PLUGIN_VERSION = "{OLD}"',
    f'PLUGIN_VERSION = "{NEW}"',
)
replace_required(
    "tests/test_public_preview_docs.py",
    f'VERSION = "{OLD}"',
    f'VERSION = "{NEW}"',
)
replace_required(
    "tests/test_dynamic_contract.py",
    f'PLUGIN_VERSION = "{OLD}"',
    f'PLUGIN_VERSION = "{NEW}"',
)

# Current-version public surfaces.
replace_required("README.md", "Version 0.3.5", "Version 0.3.6")
replace_required("README.md", "version-0.3.5", "version-0.3.6")
replace_required(
    "README.md",
    "**v0.3.5 Public Preview release candidate.**",
    "**v0.3.6 Public Preview release candidate.**",
)
readme = read("README.md")
if "Version 0.3.6 closes the stale-execution runtime regression" not in readme:
    marker = "## Additional capabilities\n"
    paragraph = (
        "Version 0.3.6 closes the stale-execution runtime regression reproduced in "
        "installed v0.3.5: the exact case now fixes Gate 5 as `stale`, Gate 7 as "
        "`passed`, Gate 10 as `blocked`, keeps the linked incident blocked, and "
        "requires schema-valid claims, empty 1C causal links, string requested "
        "evidence and no pseudo-actions.\n\n"
    )
    if marker not in readme:
        raise RuntimeError("README additional capabilities marker missing")
    readme = readme.replace(marker, paragraph + marker, 1)
    write("README.md", readme)

replace_required(
    "PRIVACY.md",
    "`1C ERP Diagnostics` v0.3.5",
    "`1C ERP Diagnostics` v0.3.6",
)
privacy = read("PRIVACY.md")
if "Version 0.3.6 keeps stale-execution results" not in privacy:
    marker = "## Companion plugins and connected tools\n"
    paragraph = (
        "Version 0.3.6 keeps stale-execution results in the evidence layer only: "
        "run/input/report identities remain identifiers, not secrets, capability rows "
        "or executable action records.\n\n"
    )
    if marker not in privacy:
        raise RuntimeError("PRIVACY companion marker missing")
    privacy = privacy.replace(marker, paragraph + marker, 1)
    write("PRIVACY.md", privacy)

for path in (
    "docs/QUICKSTART.md",
    "docs/PLUGIN_SMOKE_TEST.md",
    "plugins/one-c-erp-diagnostics/README.md",
    "plugins/one-c-erp-diagnostics/PUBLISHING.md",
):
    replace_all_required(path, OLD, NEW)

# Runtime acceptance: retain historical fix attribution, update candidate/run examples.
runtime = read("docs/RUNTIME_ACCEPTANCE.md")
runtime = runtime.replace(
    "Version 0.3.5 additionally makes Gate-0-only inventory semantics deterministic",
    "Version 0.3.5 additionally makes Gate-0-only inventory semantics deterministic",
)
if "Version 0.3.6 fixes the subsequently reproduced stale-execution" not in runtime:
    marker = "\nUntil this command passes, runtime acceptance is `blocked`:"
    paragraph = (
        "\nVersion 0.3.6 fixes the subsequently reproduced stale-execution output: "
        "Gate 5 must be `stale`, Gate 7 `passed`, Gate 10 `blocked`, the linked "
        "incident remains blocked, and claim/link/request/action arrays must use the "
        "exact schema.\n"
    )
    if marker not in runtime:
        raise RuntimeError("runtime acceptance command marker missing")
    runtime = runtime.replace(marker, paragraph + marker, 1)
runtime = runtime.replace('"run_id": "v0-3-5-clean-example"', '"run_id": "v0-3-6-clean-example"')
runtime = runtime.replace('"plugin_version": "0.3.5"', '"plugin_version": "0.3.6"')
runtime = runtime.replace('"installed_plugin_version": "0.3.5"', '"installed_plugin_version": "0.3.6"')
runtime = runtime.replace("## Priority re-test after 0.3.5 installation", "## Priority re-test after 0.3.6 installation")
write("docs/RUNTIME_ACCEPTANCE.md", runtime)

# Public release checklist: update candidate identity and append exact reproduced finding.
checklist = read("docs/PUBLIC_RELEASE_CHECKLIST.md")
checklist = checklist.replace("# Public release checklist — v0.3.5", "# Public release checklist — v0.3.6", 1)
checklist = checklist.replace("declare `0.3.5`", "declare `0.3.6`", 1)
checklist = checklist.replace("v0.3.5 release notes and self-audit", "v0.3.6 release notes and self-audit", 1)
checklist = checklist.replace("version is `0.3.5`", "version is `0.3.6`", 1)
if "Installed v0.3.5 `stale-execution-result`" not in checklist:
    marker = "## GitHub identity, security and presentation\n"
    bullets = (
        "- [x] Installed v0.3.5 `capability-inventory` passed the exact inventory-only contract.\n"
        "- [x] Installed v0.3.5 `stale-execution-result` preserved `R0` and "
        "`EVIDENCE_REQUIRED` but reproduced stale/scope/schema failures: Gate 5 "
        "passed, Gate 7 not required, Gate 10 passed, linked incident out of scope, "
        "malformed claims/links/request/actions.\n"
        "- [x] v0.3.6 adds the exact stale-execution profile and executable regression.\n"
        "- [ ] Refresh/install v0.3.6 and re-run capability inventory, stale execution "
        "and provenance closure in separate clean sessions.\n\n"
    )
    if marker not in checklist:
        raise RuntimeError("public checklist GitHub marker missing")
    checklist = checklist.replace(marker, bullets + marker, 1)
checklist = checklist.replace("v0.3.5 Pull Request", "v0.3.6 Pull Request")
checklist = checklist.replace("v0.3.5 protected PR", "v0.3.6 protected PR")
checklist = checklist.replace("v0.3.5 release/runtime acceptance", "v0.3.6 release/runtime acceptance")
write("docs/PUBLIC_RELEASE_CHECKLIST.md", checklist)

# Changelog entry.
changelog = read("CHANGELOG.md")
entry = '''## 0.3.6 — exact stale-execution runtime contract

- reproduced the installed v0.3.5 `stale-execution-result` failure after the capability-inventory hotfix passed;
- require Gate 5 `stale`, Gate 7 `passed`, Gate 10 `blocked`, and both current goal and linked incident `blocked` when an old run/input report cannot prove the current input;
- require one schema-valid non-established claim, an empty six-stage 1C causal chain, one string requested-evidence item and no pseudo-actions;
- prohibit identity-summary `УСТАНОВЛЕНО` claims, `{from,to,relation}` causal links, object-valued requested evidence and ad-hoc action fields;
- added the exact v0.3.5 runtime response as an executable rejected regression and made the rendered prompt deterministic across all Gate statuses;
- retained the v0.3.5 inventory-only fix, 16-case suite, 32 packaged skills, marketplace identity, companion pins, publication-history controls and Velis assets.

'''
if "## 0.3.6 — exact stale-execution runtime contract" not in changelog:
    marker = "# Changelog\n\n"
    if marker not in changelog:
        raise RuntimeError("CHANGELOG heading marker missing")
    changelog = changelog.replace(marker, marker + entry, 1)
    write("CHANGELOG.md", changelog)

# Release notes and audit required by ecosystem/publication validators.
release_notes = f'''# 1C ERP Diagnostics v{NEW} — Exact Stale-Execution Runtime Contract

## Overview

Version {NEW} is a focused runtime-contract hotfix based on the exact clean-session
`stale-execution-result` returned by installed v{OLD}. The preceding
`capability-inventory` test passed in v{OLD}, but the stale-result case still returned
Gate 5 `passed`, Gate 7 `not_required`, Gate 10 `passed`, linked incident
`not_in_scope`, malformed claims/causal links/requested evidence/actions and three
unsupported `УСТАНОВЛЕНО` claims.

## Corrected behavior

- `final_status=ТРЕБУЕТ ПРОВЕРКИ`, `risk=R0`, `decision=EVIDENCE_REQUIRED`;
- current goal and linked incident remain `blocked`;
- Gates 0–4 pass, Gate 5 is `stale`, Gates 6–8 pass, Gate 9 is `not_required`, Gate 10 is `blocked`;
- capability snapshot remains empty;
- one material claim uses exactly `id`, `status`, `text`, `evidence_ids`, `falsifier` and remains below established;
- input/run/report identity facts are not copied into separate established claims;
- the logical execution graph is not emitted as the six-stage 1C causal chain;
- requested evidence is one string and actions remain empty.

## Regression coverage

The test suite now includes the exact v{OLD} runtime shape and verifies independent
rejection of the wrong scope, Gate statuses, claim fields/statuses, causal-link fields,
object-valued evidence request and pseudo-action fields. The rendered synthetic prompt
states every required Gate and collection shape explicitly.

## Unchanged ecosystem and safety

- packaged skill count remains 32;
- marketplace ID remains `one-c-erp-diagnostics-marketplace` with four entries;
- Unica remains pinned to `aefc880f9bab606a5c55ed11af563b740054a549` (`v0.12.0`);
- 1C Skills PowerShell remains pinned to `8cb7868145281d8e353831512cc1ffa72f1b5c89`;
- 1C Skills Python remains pinned to `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`;
- SonarQube, evidence lineage, execution identity, R0–R3 controls, full-history validation and Velis assets are unchanged.

## Acceptance boundary

Repository CI, CodeQL and publication checks prove package consistency only. Runtime
acceptance remains blocked until installed v{NEW} passes `capability-inventory`,
`stale-execution-result`, `provenance-closure-broken` and then the complete hashed
16-case clean-session run.
'''
write(f"docs/RELEASE_NOTES_v{NEW}.md", release_notes)

audit = f'''# Plugin and ecosystem self-audit — v{NEW} Release Candidate

Audit target: the exact stale-execution output correction after installed v{OLD}
passed capability inventory but failed the next canonical runtime case.

Pre-release audit result: **No known critical control is `FAIL`; protected CI/CodeQL
and exact-version v{NEW} runtime evidence remain pending**.

| # | Control | Status | Evidence |
|---:|---|---|---|
| 1 | Manifest and package versions synchronized at {NEW} | PASS | Manifest, pyproject, validators and tests use one patch version. |
| 2 | Capability-inventory v{OLD} correction preserved | PASS | Canonical inventory result remains exact and claim-free. |
| 3 | Old run/input result is stale for current input | PASS | Gate 5 exact profile is `stale`, not `passed`. |
| 4 | Adversarial stale rejection is explicit | PASS | Gate 7 must pass after rejecting reuse. |
| 5 | Current-state goal cannot close without current evidence | PASS | Gate 10 and both scopes remain blocked. |
| 6 | Claim schema/status is exact | PASS | One non-established `{{id,status,text,evidence_ids,falsifier}}` claim. |
| 7 | Logical run graph is not 1C causal chain | PASS | `complete=false`, links empty. |
| 8 | Evidence request and actions are exact | PASS | One string request; no pseudo-actions. |
| 9 | Exact v{OLD} runtime regression exists | PASS | Reproduced response is rejected by executable tests. |
| 10 | Marketplace identity and immutable pins unchanged | PASS | Four entries and reviewed SHAs retained. |
| 11 | Packaged skills and Velis assets unchanged | PASS | 32 skills and approved assets retained. |
| 12 | Public package, lock, history, eval and unit validation | PENDING | Requires protected Pull Request CI. |
| 13 | Python 3.10/3.12 and CodeQL | PENDING | Requires protected Pull Request checks. |
| 14 | Exact installed v{NEW} priority cases | PENDING | Requires new clean sessions after refresh. |
| 15 | Complete hashed 16-case runtime acceptance | PENDING | Requires `validate_runtime_run.py`. |

## Conclusion

The candidate addresses every reproduced v{OLD} stale-execution deviation at the
prompt, orchestrator, Gate 5, Gate 7, Gate 10 and regression layers. Repository
readiness is not runtime acceptance; the installed v{NEW} package must still pass the
canonical cases in clean sessions.
'''
write(f"docs/PLUGIN_AUDIT_v{NEW}.md", audit)

print("Applied v0.3.6 stale-execution contract hotfix")
