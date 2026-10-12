from typing import Optional, List


# Example list of commands that are considered safe to run.
ALLOWED_COMMANDS: List[str] = [
    "ls",
    "pwd",
    "whoami",
    "date",
    # Add more allowed commands here.
]


def validate_and_execute_command(cmd: str) -> Optional[str]:
    """
    Validate a user‑provided command against the list of allowed commands.

    Parameters
    ----------
    cmd : str
        The user‑provided command to be validated.

    Returns
    -------
    Optional[str]
        The command string if it is in ``ALLOWED_COMMANDS``; otherwise
        ``None``.

    Notes
    -----
    - The function performs a strict equality check after stripping any
      leading/trailing whitespace.  No partial matches or argument
      expansion are allowed.
    - This function is intentionally minimal; it does not execute the
      command.  The caller should use a secure method (e.g., ``subprocess``)
      to run the command once it has been validated.
    """
    # Normalise input: strip whitespace and ensure it's a string
    if not isinstance(cmd, str):
        return None

    cmd_normalized = cmd.strip()

    # Strict membership test
    if cmd_normalized in ALLOWED_COMMANDS:
        return cmd_normalized

    return None