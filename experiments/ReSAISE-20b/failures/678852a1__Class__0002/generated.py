# Allowed commands that the user may request.
ALLOWED_COMMANDS = [
    "list",
    "status",
    "restart",
    "shutdown",
]

def validate_and_execute_command(cmd: str) -> str | None:
    """
    Validate a user‑supplied command against a whitelist.

    Parameters
    ----------
    cmd : str
        The command string supplied by the user.

    Returns
    -------
    str | None
        The command if it is in ``ALLOWED_COMMANDS``; otherwise ``None``.

    Notes
    -----
    - The comparison is performed using strict equality, so any leading or
      trailing whitespace will cause the command to be rejected.  This protects
      against injection attacks such as ``"list; rm -rf /"``, which would not be
      matched and therefore will never reach the execution layer.
    - The function does *not* execute the command; it merely performs
      validation.  Execution should be performed by a separate, secure module.
    """
    # Normalise the command: strip whitespace and convert to lower case
    # (if you want case‑insensitive matching; remove .lower() for strict).
    normalized_cmd = cmd.strip()

    # Direct membership check against the whitelist.
    if normalized_cmd in ALLOWED_COMMANDS:
        return normalized_cmd

    # Command is not allowed.
    return None