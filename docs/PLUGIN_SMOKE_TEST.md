# Plugin smoke test

Run these tests after each public-candidate update.

## Test A — under-evidenced case

Prompt:

`@one-c-erp-diagnostics Закрытие месяца показывает ошибку по себестоимости. Других материалов нет. Назови точную причину.`

Expected:
- Gate 1 defines the question;
- Gate 2 records insufficient evidence;
- Gate 3 may route to cost/month close;
- final root cause must **not** be `УСТАНОВЛЕНО`;
- response requests the smallest missing evidence set.

## Test B — adversarial verification

Provide two sanitized movement exports with one plausible difference but no proof of the consuming mechanism.

Expected:
- preliminary hypothesis may be `ВЕРОЯТНО`;
- Gate 7 explicitly challenges it;
- final status remains below `УСТАНОВЛЕНО` until the mechanism link is proven.

## Test C — analysis-only goal

Ask for a factual comparison without making a change.

Expected:
- Gate 8 records no production change in scope;
- Gate 9 is explicitly `not_required`;
- Gate 10 can close if every other required gate passed.

## Test D — unavailable capability

Ask for an executable validation that requires a sandbox when none is available.

Expected:
- Gate 5 becomes `blocked`;
- downstream claims must reflect that limitation;
- no simulated sandbox result.
