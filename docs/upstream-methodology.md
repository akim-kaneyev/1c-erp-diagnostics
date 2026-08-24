# Upstream methodology references

Pinned review date: 2026-08-24.

## OpenAI define-goal

Source reviewed:
`openai/skills/skills/.curated/define-goal/SKILL.md`

Reviewed blob SHA:
`87f111bd700e0d993465f7ac741847b5daee57d6`

What we adopt:
- define a concrete observable outcome;
- include verification evidence in the goal contract;
- define scope boundaries when ambiguity matters;
- define a stop condition instead of endless investigation;
- quantify success only when the domain supports honest quantitative validation;
- do not force goal creation for ordinary implementation work.

What we do NOT copy as-is:
- upstream goal-tool state management, because this repository must also work where the goal tool is unavailable;
- its prohibition on durable state artifacts applies to that specific skill, not to our diagnostic orchestrator. Our `STATE.md` exists specifically to support resumable investigations.

Before materially changing our goal contract rules, re-check the current upstream file and compare its blob SHA.

## OpenSandbox

Source reviewed:
`opensandbox-group/OpenSandbox`
and its Codex CLI example.

Codex example blob SHA reviewed:
`8a0a97049add204e373f337da92186906cfcb04c`

What we adopt:
- isolated command/code execution;
- running Codex CLI inside a sandbox when useful;
- explicit environment-based credentials;
- disposable case execution environments;
- file/command based validation.

Our additional controls:
- OpenSandbox is optional, never the source of truth for 1C methodology;
- sandbox output remains evidence requiring interpretation;
- production `.dt`, plaintext secrets and unnecessary confidential data are prohibited;
- inputs, commands, tool/model versions and outputs must be recorded when sandbox execution is used as verification evidence.

Before changing the sandbox integration, re-check the current upstream README/examples because installation and runtime behavior may evolve.

## Earendil — What is a Harness?

Source reviewed on 2026-08-24:
`https://earendil.com/posts/what-is-a-harness/`

Article date: 2026-08-20.

What we adopt:
- treat the useful agent as `model + harness`, not as the model alone;
- keep instructions, tools, the agentic loop and model/provider translation as separate responsibilities;
- make the loop explicit: inspect → hypothesize → test → compare → retry/reopen when evidence disagrees;
- keep domain correctness rules provider-neutral so a model swap does not silently change acceptance criteria;
- record model/provider/tool identity as provenance rather than treating brand or confidence as evidence.

What we do NOT copy as-is:
- provider-specific UX/session behavior;
- unrestricted autonomous looping without stop conditions, risk gates and evidence-based closure;
- any assumption that the availability of more tools improves correctness by itself.

Our stricter addition is that the harness has deterministic Gate 0–10 acceptance rules and a separate adversarial verifier; tool output or model confidence cannot pass those gates by declaration.

## Infostart — seven-agent 1C delivery pipeline

Source reviewed on 2026-08-24:
`https://infostart.ru/1c/articles/2767171/`

Article date: 2026-08-19.

What we adopt:
- every supplied task artifact must be accounted for instead of assuming the main technical task text contains everything important;
- separate implementation/diagnosis from independent validation and preserve repeatable check results;
- use a QA/validation ladder that distinguishes syntax/static checks from real 1C runtime, functional and business/accounting verification;
- treat reviewer severity labels and confident agent verdicts as hypotheses until reproduced or tied to evidence;
- feed escaped defects and missed findings back into the earliest failed control, regression eval or checklist;
- keep a human approval boundary for production-impacting work.

What we do NOT copy as-is:
- a mandatory fixed topology of seven agents for every task;
- majority voting or role count as evidence of correctness;
- treating successful code review, syntax, static analysis or build as proof that a 1C business process is correct;
- duplicating roles when the bounded dynamic graph can prove the same claim with fewer independent nodes.

Our implementation keeps one primary domain, at most two justified secondary domains and normally no more than four active specialist nodes, while preserving independence at Gate 7 and at the required validation level.
