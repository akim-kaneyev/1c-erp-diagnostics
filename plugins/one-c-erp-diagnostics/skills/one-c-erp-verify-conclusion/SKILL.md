---
name: one-c-erp-verify-conclusion
description: Independently challenge a preliminary 1C:ERP root-cause conclusion before it can be marked final.
---

# Independent verification

Use for Gate 7. Do not defend the preliminary answer.

For each material conclusion:
1. re-read the primary evidence;
2. confirm that every material supplied source/attachment is accounted for by Gate 2 and inspect anything that could falsify the conclusion;
3. label every premise fact / interpretation / hypothesis;
4. challenge each causal link;
5. identify any 1C object name not proven by evidence/metadata/code/docs;
6. verify before/after uses identical analytics;
7. look for an earlier divergence point;
8. test reasonable alternative explanations;
9. state a falsifier;
10. verify provenance closure from each material premise/causal link back to an original artifact or documented derivation chain;
11. verify every relied-upon executable/tool result belongs to the current case and current material input identities rather than a stale run;
12. downgrade status when evidence is insufficient.

## Review finding rule

A review label such as `critical`, `high`, `blocking`, or an agent's confident defect verdict is not itself evidence that a defect exists. Convert every material review finding into a testable claim and independently reproduce it or link it to original case evidence before treating it as established.

Likewise, absence of findings from another reviewer or tool is not proof of correctness. Resolve disagreements by evidence and reproduction, never by majority vote or confidence wording.

## Provenance closure rule

A claim may not remain `УСТАНОВЛЕНО` when any material chain has an unanchored transformation, unknown parent evidence, mismatched execution identity or stale output. A clean summary, report or analyzer finding cannot repair a broken lineage. Return to the earliest missing artifact/derivation/run record and reopen the affected gate.

A final root cause may be `УСТАНОВЛЕНО` only after surviving this pass, with closed provenance for every material causal link and no material supplied evidence left unaccounted for in a way that could change the conclusion.

## Strict stale-result adversarial rule

For synthetic `stale-execution-result`, Gate 7 is `passed` when this review correctly
rejects `R-OLD` as current evidence. The linked incident remains `blocked`, not
`not_in_scope`. Do not create established claims that merely repeat `INPUT-CURRENT`,
`INPUT-OLD`, `RUN-OLD` or `R-OLD`. Return one material `ТРЕБУЕТ ПРОВЕРКИ` claim, an
incomplete empty six-stage 1C causal chain, and no action objects.
