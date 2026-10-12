from typing import Optional, Iterable

# Define the set of trusted commands.  Use a frozenset for immutability.
ALLOWED_COMMANDS: Iterable[str] = {
    "ls",
    "cat",
    "echo",
    "date",
    # Add other safe commands here
}
ALLOWED_COMMANDS = frozenset(ALLOWED_COMMANDS)


def authorize_and_run_cmd(command: str) -> Optional[str]:
    """
    Validate a user-provided command against a whitelist of allowed commands.

    Parameters
    ----------
    command : str
        The command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command if it is in ``ALLOWED_COMMANDS``; otherwise ``None``.

    Notes
    -----
    - The comparison is case-sensitive and exact.  No shell expansion or
      wildcard matching is performed.
    - The function does not execute the command; it only performs validation.
      Execution should be handled by a separate, trusted routine.
    """
    # Strip leading/trailing whitespace to avoid accidental mismatches
    cleaned = command.strip()

    if cleaned in ALLOWED_COMMANDS:
        return cleaned

    # Command not allowed
    return None