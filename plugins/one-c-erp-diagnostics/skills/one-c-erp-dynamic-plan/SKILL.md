---
name: one-c-erp-dynamic-plan
description: Convert a routed 1C:ERP case into a bounded dependency graph of specialist analyses, executable validations and review gates.
---

# Dynamic execution graph

Use at Gate 3.

Each graph node must define:

1. node ID and question;
2. specialist/domain skill;
3. input evidence IDs;
4. dependencies;
5. allowed capabilities;
6. read/write risk;
7. expected output schema;
8. success, stop and falsification conditions;
9. required validation level and acceptance evidence for every material claim or change.

## Independent validation contract

Before executing a material diagnostic or corrective node, define how its result will be checked independently of the producing specialist. The validating pass must use original evidence, reproduced output or another independently derived observation; it must not accept the producer's own summary as proof.

Use the smallest required level from this validation ladder, but never substitute a lower level for a higher one required by the claim:

1. `structural` — artifact/schema/source can be read and identifiers are real;
2. `static` — syntax/lint/static analyzer findings where applicable;
3. `metadata_runtime` — 1C metadata/build/compile/runtime behavior when the claim depends on execution;
4. `functional` — the target user/business scenario is reproduced;
5. `business_accounting` — identical analytics prove the required movements/registers/postings/balances/access outcome.

For every required validation record method, evidence source, expected result, falsifier and status. When a required level cannot be executed with available capabilities, the dependent node is `blocked`; do not promote a lower-level check into a pass.

Rules:

- one primary domain, at most two secondary domains;
- no more than four active specialist nodes without an explicit reason;
- parallelize only independent read-only nodes;
- serialize any nodes that mutate shared files or environments;
- the verifier cannot depend only on the synthesis node: it must have access to original evidence;
- blocked required nodes block downstream certainty;
- new evidence reopens the earliest affected node/gate.

Prefer the smallest graph that can prove or disprove the user's claim.
