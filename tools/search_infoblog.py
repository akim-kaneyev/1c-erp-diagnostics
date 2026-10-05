from __future__ import annotations

import runpy
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "plugins"
    / "one-c-erp-diagnostics"
    / "skills"
    / "one-c-erp-incident-search"
    / "scripts"
    / "search_infoblog.py"
)


if __name__ == "__main__":
    runpy.run_path(str(SCRIPT), run_name="__main__")
