# Contributing

Contributions are welcome when they improve diagnostic rigor, reproducibility, safety or usability.

## Evidence-first requirement

A contribution must not teach the agent to present a hypothesis as a proven case-specific fact. New diagnostic logic should preserve the distinction between:

- established fact;
- interpretation;
- hypothesis;
- missing evidence;
- verified conclusion.

Root-cause workflows should retain an independent verification step before final `УСТАНОВЛЕНО`.

## 1C metadata rule

Do not hard-code or assert 1C metadata object names as universal truth unless the contribution is explicitly about a documented standard object and the scope/version is clear. Case conclusions still require evidence that the object is present/relevant in that case.

## Data policy

Do not contribute customer/company databases, production `.dt`, backups, credentials, real primary documents or confidential exports. Examples must be synthetic or sanitized.

## Pull requests

Keep PRs focused. Explain:

1. the problem;
2. the proposed change;
3. how it was validated;
4. what could falsify or break the new behavior;
5. any new privacy/security surface.

## Style

Prefer concise domain language, explicit stop conditions, reproducible checks and reversible actions over generic advice.
