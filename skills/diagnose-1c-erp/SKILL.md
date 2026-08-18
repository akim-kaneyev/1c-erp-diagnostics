---
name: diagnose-1c-erp
description: Evidence-first diagnosis of 1C:ERP accounting and movement incidents from user-provided exports, reports, registers, postings, screenshots and code.
user-invocable: true
argument-hint: "[case-directory-or-question]"
---

# Diagnose 1C ERP

## Goal

Determine whether the root cause of a 1C:ERP incident is proven and identify the smallest safe next action.

## Step 0 — route the case

Read `AGENTS.md`, then `playbooks/router.md`.
Choose one primary playbook from `playbooks/`. Add a second only when a concrete cross-domain link is visible in evidence.

## Step 1 — evidence inventory

For each source record:
- filename/source;
- represented document/report;
- period;
- organization if present;
- key identifiers;
- what question it can answer;
- limitations.

## Step 2 — fact table

Separate every material statement into:
- established fact;
- interpretation;
- hypothesis;
- missing evidence.

Never invent metadata object names.

## Step 3 — comparison

When good/bad or before/after examples exist, compare only dimensions actually present in evidence: dates, organization, warehouse, item, series, purpose/assignment, quantity, amount, registrar, movement type, activity, accounts, subaccounts, expense analytics, order/realization/production linkage and other confirmed fields.

## Step 4 — causal chain

Trace:
`document → movement → register/record → calculation or business mechanism → accounting/stock result → observed symptom`.

A root-cause claim must answer:
1. What exact record differs?
2. Which mechanism consumes it?
3. Why does that mechanism create the result?
4. What evidence connects it to the symptom?
5. Does a controlled correction change the result in the expected direction?

## Step 5 — domain playbook

Execute all mandatory checks and stop rules from the selected playbook. Domain playbooks refine the general method; they do not override evidence requirements.

## Step 6 — conclusion

Use only:
- `УСТАНОВЛЕНО`;
- `ВЕРОЯТНО`;
- `ТРЕБУЕТ ПРОВЕРКИ`.

Root cause is `УСТАНОВЛЕНО` only when the symptom, concrete difference, consuming mechanism, causal link and reasonable alternatives are sufficiently verified.

## Step 7 — safe action

Give the smallest reversible next action. Prefer verification and standard 1C mechanisms before manual accounting corrections, opening closed periods, broad rights, mass reposting or configuration changes.

## Mandatory self-review

Before final answer check:
- no invented 1C objects;
- source exists for every material fact;
- fact and hypothesis are separated;
- causality is actually shown;
- before/after is compared on the same analytics;
- selected playbook matches the evidence;
- the proposed action is minimal and reversible.
