#!/usr/bin/env python3
"""Validate a no-tools Codex runtime log and exact primary-plugin mention."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

COMMAND_MARKER = re.compile(r"\s-(?:NoProfile\s+)?Command\s+", re.IGNORECASE)
TOOL_PREFIX = re.compile(
    r"^(?:web search|mcp|browser|image generation):",
    re.IGNORECASE | re.MULTILINE,
)
CODEX_HEADER = re.compile(r"^OpenAI Codex v\S+\s*$", re.MULTILINE)
WORKDIR = re.compile(r"^workdir:\s+(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
SESSION_ID = re.compile(
    r"^session id:\s+([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\s*$",
    re.IGNORECASE | re.MULTILINE,
)
USER_MARKER = re.compile(r"^user\s*$", re.MULTILINE)
CODEX_MARKER = re.compile(r"^codex\s*$", re.MULTILINE)
TOKENS_USED = re.compile(r"^tokens used\s*$", re.MULTILINE)
PLUGIN_MENTION = (
    "[@one-c-erp-diagnostics]"
    "(plugin://one-c-erp-diagnostics@one-c-erp-diagnostics-marketplace)"
)


def add(errors: list[str], location: str, message: str) -> None:
    errors.append(f"{location}: {message}")


def configure_utf8_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")


def command_lines(text: str) -> list[tuple[int, str]]:
    return [
        (number, line)
        for number, line in enumerate(text.splitlines(), start=1)
        if COMMAND_MARKER.search(line)
    ]


def inspect_runtime_log(
    path: Path, expected_case_id: str | None = None
) -> tuple[list[str], dict[str, str], dict[str, Any] | None]:
    errors: list[str] = []
    metadata: dict[str, str] = {}
    assistant_result: dict[str, Any] | None = None
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001 - validator reports malformed evidence
        add(errors, str(path), f"cannot read UTF-8 runtime log: {exc}")
        return errors, metadata, assistant_result

    if not CODEX_HEADER.search(text):
        add(errors, str(path), "Codex CLI header is missing")

    workdirs = WORKDIR.findall(text)
    if len(workdirs) != 1:
        add(errors, str(path), f"expected exactly one workdir header, found {len(workdirs)}")
    else:
        metadata["workdir"] = workdirs[0].strip()

    session_ids = SESSION_ID.findall(text)
    if len(session_ids) != 1:
        add(
            errors,
            str(path),
            f"expected exactly one clean-session id, found {len(session_ids)}",
        )
    else:
        metadata["session_id"] = session_ids[0].lower()

    users = list(USER_MARKER.finditer(text))
    codex_messages = list(CODEX_MARKER.finditer(text))
    if len(users) != 1:
        add(errors, str(path), f"expected exactly one user message, found {len(users)}")
    if len(codex_messages) != 1:
        add(
            errors,
            str(path),
            f"expected exactly one final Codex message, found {len(codex_messages)}",
        )

    if len(users) == 1 and len(codex_messages) == 1:
        user_start = users[0].end()
        codex_start = codex_messages[0].start()
        user_prompt = text[user_start:codex_start].lstrip("\r\n")
        if not user_prompt.startswith(PLUGIN_MENTION + "\n") and not user_prompt.startswith(
            PLUGIN_MENTION + "\r\n"
        ):
            add(errors, str(path), "user prompt does not start with the exact primary-plugin mention")
        if expected_case_id is not None:
            case_marker = f"Синтетический регрессионный кейс `{expected_case_id}`."
            if case_marker not in user_prompt:
                add(errors, str(path), f"rendered prompt for case {expected_case_id!r} is missing")

        response_text = text[codex_messages[0].end() :].lstrip("\r\n")
        try:
            value, _ = json.JSONDecoder().raw_decode(response_text)
        except json.JSONDecodeError as exc:
            add(errors, str(path), f"final Codex message is not a JSON object: {exc}")
        else:
            if not isinstance(value, dict):
                add(errors, str(path), "final Codex message JSON root must be an object")
            else:
                assistant_result = value

    if len(TOKENS_USED.findall(text)) != 1:
        add(errors, str(path), "complete log must contain exactly one tokens-used trailer")

    tool_events = TOOL_PREFIX.findall(text)
    if tool_events:
        names = ", ".join(sorted({name.casefold() for name in tool_events}))
        add(errors, str(path), f"model tool call used under no-tools policy: {names}")

    commands = command_lines(text)
    for line_number, command in commands:
        location = f"{path}:{line_number}"
        add(errors, location, f"shell command used under no-tools policy: {command[:160]}")
    return errors, metadata, assistant_result


def validate_runtime_log(path: Path, expected_case_id: str | None = None) -> list[str]:
    errors, _, _ = inspect_runtime_log(path, expected_case_id)
    return errors


def main() -> int:
    configure_utf8_output()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logs", type=Path, nargs="+", help="Codex runtime log files")
    args = parser.parse_args()

    errors: list[str] = []
    for path in args.logs:
        errors.extend(validate_runtime_log(path.resolve()))
    if errors:
        print("RUNTIME LOG VALIDATION: BLOCKED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("RUNTIME LOG VALIDATION: PASS")
    print(f"Validated logs: {len(args.logs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
