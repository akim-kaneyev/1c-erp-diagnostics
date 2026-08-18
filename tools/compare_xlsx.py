from __future__ import annotations

import json
import sys
from pathlib import Path
from openpyxl import load_workbook


def snapshot(path: Path) -> dict:
    wb = load_workbook(path, read_only=True, data_only=False)
    data = {}
    for ws in wb.worksheets:
        sheet = {}
        for row in ws.iter_rows():
            for cell in row:
                if cell.value not in (None, ""):
                    sheet[cell.coordinate] = cell.value
        data[ws.title] = sheet
    wb.close()
    return data


def main(a_name: str, b_name: str) -> None:
    a_path, b_path = Path(a_name), Path(b_name)
    a, b = snapshot(a_path), snapshot(b_path)
    all_sheets = sorted(set(a) | set(b))
    diff = {"left": a_path.name, "right": b_path.name, "sheets": {}}

    for s in all_sheets:
        sa, sb = a.get(s, {}), b.get(s, {})
        coords = sorted(set(sa) | set(sb))
        changes = []
        for c in coords:
            va, vb = sa.get(c), sb.get(c)
            if va != vb:
                changes.append({"cell": c, "left": va, "right": vb})
        if changes:
            diff["sheets"][s] = changes

    out = Path(f"{a_path.stem}__vs__{b_path.stem}.diff.json")
    out.write_text(json.dumps(diff, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python tools/compare_xlsx.py left.xlsx right.xlsx")
    main(sys.argv[1], sys.argv[2])
