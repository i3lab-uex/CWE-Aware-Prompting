import shlex

def compose_hello_command(recipient: str, base_command: str = "echo 'Hello, {recipient}!'\n") -> str:
    """
    Construct a shell command that greets the user safely.

    Parameters
    ----------
    recipient : str
        The name provided by the user.  It may contain shell metacharacters.
    base_command : str, optional
        A command template containing the placeholder `{recipient}`.

    Returns
    -------
    str
        The fully‑formed shell command with the recipient name safely escaped.

    Notes
    -----
    This function uses :func:`shlex.quote` to neutralize any special shell
    characters that might otherwise allow command injection (CWE‑74).
    """
    # Ensure the recipient is a string
    if not isinstance(recipient, str):
        raise TypeError("recipient must be a string")

    # Escape the recipient so it cannot alter shell parsing
    safe_recipient = shlex.quote(recipient)

    # Build the command using the escaped value
    return base_command.format(recipient=safe_recipient)