# Upstream methodology references

Pinned review date: 2026-08-17.

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
