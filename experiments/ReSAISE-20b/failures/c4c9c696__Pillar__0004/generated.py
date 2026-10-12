# -*- coding: utf-8 -*-
"""
Utility module for safe command execution.

The `check_and_run_command` function verifies that a user-provided
command is present in a pre-defined whitelist (`ALLOWED_COMMANDS`)
before returning it for execution.  This protects against
arbitrary command injection and satisfies the security requirements
for CWE‑707 (Improper Neutralization).

The function performs a constant-time membership check using a set,
trims surrounding whitespace, and normalizes the command string
to avoid variations that could bypass the whitelist.
"""

from __future__ import annotations

import re
from typing import Optional, Set


# --------------------------------------------------------------------------- #
# 1. Whitelist of allowed commands
# --------------------------------------------------------------------------- #

# Example whitelist – modify as needed for your application.
ALLOWED_COMMANDS: Set[str] = {
    "list",
    "status",
    "restart",
    "shutdown",
    "update",
}

# --------------------------------------------------------------------------- #
# 2. Helper utilities
# --------------------------------------------------------------------------- #

def _normalize_command(cmd: str) -> str:
    """
    Normalise the command string to a canonical form.

    - Strip leading/trailing whitespace.
    - Collapse internal whitespace to single spaces.
    - Convert to lower case (if commands are intended to be case‑insensitive).

    Args:
        cmd: Raw user input.

    Returns:
        Normalised command string.
    """
    # Remove leading/trailing whitespace
    cmd = cmd.strip()
    # Collapse multiple spaces/tabs/newlines into a single space
    cmd = re.sub(r"\s+", " ", cmd)
    # Convert to lower case for case‑insensitive comparison
    return cmd.lower()


# --------------------------------------------------------------------------- #
# 3. Public API
# --------------------------------------------------------------------------- #

def check_and_run_command(user_input: str) -> Optional[str]:
    """
    Validate a user command against the allowed list.

    The function performs a constant‑time lookup in `ALLOWED_COMMANDS`
    after normalising the input.  If the command is present, it
    returns the canonical string; otherwise `None` is returned.

    Args:
        user_input: The raw command entered by the user.

    Returns:
        The normalised command string if it is permitted, else None.
    """
    # Normalise the input
    normalized = _normalize_command(user_input)

    # Constant‑time membership test (set lookup is O(1) average)
    if normalized in ALLOWED_COMMANDS:
        return normalized

    # Not allowed
    return None


# --------------------------------------------------------------------------- #
# Example usage (uncomment for testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Sample inputs
    tests = [
        "  LIST ",
        "StaTus",
        "reStart",
        "shutdown\n",
        "unknown",
        "list; rm -rf /",  # malicious attempt
    ]

    for inp in tests:
        cmd = check_and_run_command(inp)
        print(f"Input: {inp!r} -> {'Allowed' if cmd else 'Blocked'}")