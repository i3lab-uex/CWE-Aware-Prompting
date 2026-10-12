import shlex

def compose_hello_command(recipient: str, base_command: str = "echo 'Hello, {recipient}!'" ) -> str:
    """
    Construct a shell command that greets the given recipient.

    Parameters
    ----------
    recipient : str
        The name provided by the user that will be inserted into the command.
    base_command : str, optional
        A template string containing a '{recipient}' placeholder.  Defaults to
        "echo 'Hello, {recipient}!'" which uses single quotes to avoid shell
        word splitting.

    Returns
    -------
    str
        The fully-formed command string with the recipient safely escaped.

    Notes
    -----
    The function uses :func:`shlex.quote` to escape the recipient so that any
    characters that could alter shell parsing (e.g., spaces, semicolons,
    quotes) are treated literally.  This mitigates CWE-74 (Command Injection).
    """
    # Ensure the placeholder exists to avoid a misleading command
    if "{recipient}" not in base_command:
        raise ValueError("base_command must contain a '{recipient}' placeholder")

    # Safely escape the recipient for shell usage
    safe_recipient = shlex.quote(recipient)

    # Format the command with the escaped recipient
    return base_command.format(recipient=safe_recipient)