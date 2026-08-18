"""
Illustrative bootstrap only.

Requires the optional `opensandbox` package and a configured OpenSandbox server.
Keep credentials outside this file.
"""

import asyncio
from datetime import timedelta
from opensandbox import Sandbox


async def main():
    sandbox = await Sandbox.create(
        "python:3.12",
        timeout=timedelta(minutes=30),
    )
    async with sandbox:
        result = await sandbox.commands.run("python --version")
        for line in result.logs.stdout:
            print(line.text)
        await sandbox.kill()


if __name__ == "__main__":
    asyncio.run(main())
