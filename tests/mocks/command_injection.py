"""Intentionally insecure code used only as a Bandit test fixture."""

import subprocess


def run_command(command: str) -> None:
    subprocess.run(command, shell=True)
