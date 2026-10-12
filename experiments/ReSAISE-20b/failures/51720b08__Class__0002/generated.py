import shlex

def compose_hello_command(recipient: str, base_command: str) -> str:
    """
    Construct a shell command that greets the user by name.

    Parameters
    ----------
    recipient : str
        The name provided by the user that will be inserted into the command.
    base_command : str
        A predefined shell command template containing the placeholder '{recipient}'.

    Returns
    -------
    str
        A safely constructed shell command with the user's name quoted to prevent injection.

    Notes
    -----
    The function uses :func:`shlex.quote` to escape any shell metacharacters in the
    recipient string.  This mitigates CWE-74 (Improper Neutralization of Special Elements in Output Used by a Downstream Component).
    """
    # Ensure the recipient is safely escaped for shell usage
    safe_recipient = shlex.quote(recipient)

    # Replace the placeholder with the safely quoted name
    command = base_command.format(recipient=safe_recipient)

    return command