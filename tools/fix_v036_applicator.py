#!/usr/bin/env python3
from pathlib import Path

path = Path(__file__).with_name("apply_v036_hotfix.py")
text = path.read_text(encoding="utf-8")
old = "One non-established `{id,status,text,evidence_ids,falsifier}` claim."
new = "One non-established `{{id,status,text,evidence_ids,falsifier}}` claim."
if old not in text:
    raise SystemExit("Expected applicator brace token not found")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("Fixed v0.3.6 applicator literal braces")
