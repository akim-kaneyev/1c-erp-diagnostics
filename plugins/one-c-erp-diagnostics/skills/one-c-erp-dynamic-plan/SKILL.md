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
8. success, stop and falsification conditions.

Rules:

- one primary domain, at most two secondary domains;
- no more than four active specialist nodes without an explicit reason;
- parallelize only independent read-only nodes;
- serialize any nodes that mutate shared files or environments;
- the verifier cannot depend only on the synthesis node: it must have access to original evidence;
- blocked required nodes block downstream certainty;
- new evidence reopens the earliest affected node/gate.

Prefer the smallest graph that can prove or disprove the user's claim.
