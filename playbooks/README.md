# 1C:ERP Diagnostic Playbooks

Playbooks specialize the common evidence-first workflow for recurring 1C:ERP incident classes.

They do not define fixed metadata object names. Every object, register, field, account, analytic, document type or role used in a conclusion must be confirmed by the case materials, metadata, code or official documentation.

## Routing

Start with `router.md`, then load one primary playbook. Add a second playbook only when the incident really crosses domains.

Available playbooks:

- `cost-and-month-close.md` — себестоимость, отклонения, закрытие месяца;
- `post-item-expenses.md` — постатейные расходы и их распределение;
- `settlements.md` — взаиморасчеты, задолженность, авансы, зачеты;
- `vat.md` — НДС, книги покупок/продаж, корректировки периодов;
- `warehouse-series-assignments.md` — склад, серии, назначения, отрицательные/раздвоенные остатки;
- `production.md` — производство, этапы, материалы, возвраты, ремонт;
- `access-rights.md` — роли, профили, группы доступа, разделение полномочий.

## Universal stop rule

If the evidence cannot connect the observed symptom to a concrete record and the mechanism that consumes that record, the root cause is not established. Return `ВЕРОЯТНО` or `ТРЕБУЕТ ПРОВЕРКИ` and request the smallest missing evidence set.
