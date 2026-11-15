"""Build the first-party CFE in a new, isolated file infobase (never a supplied base)."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "plugins/one-c-erp-diagnostics/bridge/src"


def build(platform: Path, destination: Path) -> dict:
    if not platform.is_file() or platform.name.lower() != "1cv8.exe":
        raise ValueError("explicit_designer_executable_required")
    destination.mkdir(parents=True, exist_ok=False)
    database = destination / "ib"
    logs = destination / "logs"
    logs.mkdir()
    output = destination / "VelisReadOnlyBridge.cfe"

    def run(name, args):
        log = logs / (name + ".log")
        process = subprocess.run([str(platform), *args, "/DisableStartupDialogs", "/DisableStartupMessages", "/Out", str(log)],
                                 capture_output=True, timeout=300, check=False)
        if process.returncode:
            raise RuntimeError(f"designer_{name}_failed: see {log}")

    run("create", ["CREATEINFOBASE", f"File={database};"])
    base = ["DESIGNER", "/F", str(database)]
    run("load", [*base, "/LoadConfigFromFiles", str(SOURCE), "-Extension", "VelisReadOnlyBridge"])
    run("check", [*base, "/CheckConfig", "-Server", "-ExternalConnection", "-ExtendedModulesCheck", "-Extension", "VelisReadOnlyBridge"])
    run("dump", [*base, "/DumpCfg", str(output), "-Extension", "VelisReadOnlyBridge"])
    if not output.is_file() or output.stat().st_size < 1000:
        raise RuntimeError("cfe_not_created")
    result = {"schema_version": 1, "extension": "VelisReadOnlyBridge", "version": "0.1.0",
              "artifact_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
              "source_sha256": {str(path.relative_to(SOURCE)).replace("\\", "/"): hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in sorted(SOURCE.rglob("*")) if path.is_file()},
              "platform_path": str(platform), "checks": ["isolated_file_infobase", "native_load", "native_server_check", "native_cfe_dump"]}
    (destination / "build.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.platform.resolve(), args.output.resolve()), ensure_ascii=True))
