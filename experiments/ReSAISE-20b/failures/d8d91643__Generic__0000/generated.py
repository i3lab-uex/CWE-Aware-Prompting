import shlex

def build_greeting_command(nickname: str, base_command: str) -> str:
    """
    Build a shell command that greets the user by embedding their nickname
    into the provided base_command template.

    Parameters
    ----------
    nickname : str
        The user-provided name to be inserted into the command.
    base_command : str
        A shell command template containing the placeholder '{nickname}'.

    Returns
    -------
    str
        The final shell command with the nickname safely escaped.
    """
    # Use shlex.quote to escape any potentially dangerous characters
    safe_nickname = shlex.quote(nickname)
    # Replace the placeholder with the quoted nickname
    return base_command.format(nickname=safe_nickname)