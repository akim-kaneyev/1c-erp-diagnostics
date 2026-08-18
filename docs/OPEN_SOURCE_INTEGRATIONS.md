# Reviewed open-source integrations

Review date: 2026-08-18.

This project uses open-source components only through an explicit intake process. Discovery catalogs such as OpenYellow are not treated as security or quality certification.

## OpenAI define-goal

Source: `https://github.com/openai/skills/tree/main/skills/.curated/define-goal`

Use: measurable goal-contract quality bar at Gate 1. It is a methodology reference, not a runtime dependency.

## OpenSandbox

Source: `https://github.com/opensandbox-group/OpenSandbox`

License: Apache-2.0.

Use: optional isolated execution for sanitized scripts, parsers and reproducible validation. It is not a source of 1C knowledge. Network egress and credentials must be controlled.

## v8unpack

Source: `https://github.com/saby-integration/v8unpack`

Reviewed Python package pin: `v8unpack==1.2.6` (MIT).

Use: read-only extraction of sanitized CF/CFE/EPF into BSL/JSON. Rebuild mode is excluded from the diagnostic workflow. Successful extraction does not prove that the code caused an accounting incident.

## BSL Language Server

Source: `https://github.com/1c-syntax/bsl-language-server`

Use: optional static BSL analysis after extraction. Record the exact release and command used. Its diagnostics are hypotheses until connected to the factual case chain. MCP mode is not a mandatory dependency.

## Unica and 1C Skills

These are optional host-managed companion plugins in the user's environment. Their private implementation is not copied. Portable dependency metadata was not available through the public plugin registry at review time, so the orchestrator discovers them at runtime and records availability honestly.
