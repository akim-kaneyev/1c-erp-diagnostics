from __future__ import annotations

import sys
from pathlib import Path
from pypdf import PdfReader


def main(filename: str) -> None:
    path = Path(filename)
    reader = PdfReader(str(path))
    parts = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        parts.append(f"\n\n===== PAGE {i} =====\n{text}")

    out = path.with_suffix(path.suffix + ".txt")
    out.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {out}")
    print("Note: image-only/scanned pages may require visual inspection; OCR is not assumed.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/pdf_extract.py file.pdf")
    main(sys.argv[1])
