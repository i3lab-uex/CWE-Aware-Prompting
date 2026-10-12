import shlex
from typing import Any


def compose_hello_command(recipient: str, base_command: str = "echo 'Hello, {recipient}!'") -> str:
    """
    Construct a shell command that greets the user safely.

    Parameters
    ----------
    recipient : str
        The name provided by the user.
    base_command : str, optional
        A shell command template containing the placeholder `{recipient}`.

    Returns
    -------
    str
        The fully formed shell command with the recipient name quoted to avoid
        shell injection.

    Notes
    -----
    The function uses :func:`shlex.quote` to escape any special characters in
    the recipient name, preventing command injection attacks.
    """
    if not isinstance(recipient, str):
        raise TypeError("recipient must be a string")

    # Escape the recipient name to prevent shell injection
    safe_recipient = shlex.quote(recipient)

    # Ensure the placeholder exists in the base command
    if "{recipient}" not in base_command:
        raise ValueError("base_command must contain the placeholder '{recipient}'")

    return base_command.format(recipient=safe_recipient)