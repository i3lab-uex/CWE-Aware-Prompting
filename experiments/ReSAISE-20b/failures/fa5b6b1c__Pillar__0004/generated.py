import re
from typing import Optional

# A whitelist of commands considered safe to execute.
ALLOWED_COMMANDS = {
    "ls",
    "pwd",
    "whoami",
    "echo",
    "date",
}

def _is_valid_command(cmd: str) -> bool:
    """
    Validate that the command is a simple, non‑shell injected string
    consisting only of alphanumeric characters and underscores.
    This prevents accidental execution of shell metacharacters.
    """
    return bool(re.fullmatch(r"[A-Za-z0-9_]+", cmd))

def authorize_and_run_cmd(command: str) -> Optional[str]:
    """
    Validate the user supplied command against a whitelist.

    Parameters
    ----------
    command : str
        The raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command if it is present in ALLOWED_COMMANDS,
        otherwise None.
    """
    # Normalise whitespace and strip surrounding spaces
    cmd = command.strip()

    # Basic structural validation to mitigate CWE‑707 risks.
    if not _is_valid_command(cmd):
        return None

    # Membership check using a set for O(1) lookup.
    if cmd in ALLOWED_COMMANDS:
        return cmd
    return None

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    for test_cmd in ["ls", "rm -rf /", "echo", "cat /etc/passwd"]:
        result = authorize_and_run_cmd(test_cmd)
        print(f"Command: {test_cmd!r} -> {result}")