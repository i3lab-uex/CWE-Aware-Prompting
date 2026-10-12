# -*- coding: utf-8 -*-
"""
Safe command validator.

This module defines a single function, :func:`run_command_if_safe`, that checks
whether a user supplied command is in the set of allowed commands.  If the
command is permitted, it returns the original string; otherwise ``None`` is
returned.  No exceptions are raised for invalid commands, keeping the API
simple and avoiding leakage of internal state.

The implementation is deliberately straightforward to avoid common pitfalls
such as:

* **Command injection** – by only allowing exact matches from a pre‑defined set.
* **Whitespace or case handling** – the check is performed on the raw string
  provided by the caller.  If normalization is required it should be done
  *before* calling this function.
"""

from __future__ import annotations

# A set of commands that are considered safe for execution.
ALLOWED_COMMANDS = {
    "list_files",
    "show_status",
    "restart_service",
    "shutdown_system",
    # Add more safe commands here as needed.
}

def run_command_if_safe(user_command: str) -> str | None:
    """
    Validate a user supplied command against the list of allowed commands.

    Parameters
    ----------
    user_command : str
        The command string supplied by the user.

    Returns
    -------
    str | None
        The original command if it is in :data:`ALLOWED_COMMANDS`,
        otherwise ``None`` to indicate the command is not authorized.

    Notes
    -----
    * The comparison is case sensitive and does **not** strip leading/trailing
      whitespace.  If the calling code requires normalization, it should be
      performed before invoking this function.
    * No exception is raised for disallowed commands; callers should check
      the return value to decide how to handle an unauthorized command.
    """
    # Direct membership test is O(1) for a set.
    if user_command in ALLOWED_COMMANDS:
        return user_command
    return None

# Example usage (commented out to avoid accidental execution):
# if __name__ == "__main__":
#     cmd = input("Enter command: ")
#     safe_cmd = run_command_if_safe(cmd)
#     if safe_cmd is not None:
#         print(f"Executing: {safe_cmd}")
#     else:
#         print("Unauthorized command.")