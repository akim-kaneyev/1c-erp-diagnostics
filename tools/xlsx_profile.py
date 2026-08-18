from __future__ import annotations

import json
import sys
from pathlib import Path
from openpyxl import load_workbook


def profile(path: Path) -> dict:
    wb = load_workbook(path, read_only=True, data_only=False)
    result = {"file": path.name, "sheets": []}

    for ws in wb.worksheets:
        nonempty = 0
        formulas = 0
        samples = []
        for row_idx, row in enumerate(ws.iter_rows(), start=1):
            row_values = []
            row_nonempty = False
            for c in row:
                v = c.value
                if v not in (None, ""):
                    nonempty += 1
                    row_nonempty = True
                    if isinstance(v, str) and v.startswith("="):
                        formulas += 1
                row_values.append(v)
            if row_nonempty and len(samples) < 10:
                samples.append({"row": row_idx, "values": row_values[:30]})

        result["sheets"].append({
            "title": ws.title,
            "max_row": ws.max_row,
            "max_column": ws.max_column,
            "nonempty_cells": nonempty,
            "formula_cells": formulas,
            "sample_nonempty_rows": samples,
        })

    wb.close()
    return result


def main(filename: str) -> None:
    path = Path(filename)
    data = profile(path)
    out = path.with_suffix(path.suffix + ".profile.json")
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/xlsx_profile.py file.xlsx")
    main(sys.argv[1])
