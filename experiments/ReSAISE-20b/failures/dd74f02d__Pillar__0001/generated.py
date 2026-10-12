# -*- coding: utf-8 -*-
"""
Utility for validating user supplied commands against a whitelist of safe commands.

The module is intentionally minimal and self‑contained.  It demonstrates how to
securely check a command before execution, avoiding common pitfalls such as
arbitrary shell injection or improper neutralisation of input (CWE‑707).
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Whitelist of allowed commands.  In a real application this set should be
# carefully curated and kept up to date.  The values are case‑sensitive and
# must match the exact command string that will be executed.
# --------------------------------------------------------------------------- #
ALLOWED_COMMANDS = {
    "list",
    "show",
    "delete",
    "create",
    "update",
}

def run_command_if_safe(user_command: str) -> str | None:
    """
    Validate that *user_command* is present in :data:`ALLOWED_COMMANDS`.

    Parameters
    ----------
    user_command : str
        The raw command string supplied by a user.

    Returns
    -------
    str | None
        The original command if it is authorised; otherwise ``None``.

    Notes
    -----
    - Leading/trailing whitespace is ignored.
    - The check is case‑sensitive; modify the whitelist or add a normalization
      step if you require case‑insensitivity.
    - No attempt is made to parse or interpret the command; callers should
      use a safe execution mechanism (e.g. ``subprocess.run`` with a list of
      arguments) if the command is authorised.
    """
    # Strip whitespace to avoid accidental rejections of commands with
    # surrounding spaces or newlines.
    cleaned = user_command.strip()

    if not cleaned:
        return None

    # Membership test is O(1) for a set.
    if cleaned in ALLOWED_COMMANDS:
        return cleaned

    # Command not authorised
    return None


# --------------------------------------------------------------------------- #
# Example usage (commented out to avoid accidental execution):
#
# if __name__ == "__main__":
#     cmd = input("Enter command: ")
#     safe_cmd = run_command_if_safe(cmd)
#     if safe_cmd is None:
#         print("Command not authorised.")
#     else:
#         # Safe to execute, e.g. via subprocess.run([safe_cmd])
#         print(f"Executing safe command: {safe_cmd}")
# --------------------------------------------------------------------------- #