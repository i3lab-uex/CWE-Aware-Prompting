import shlex

def build_greeting_command(nickname: str, base_command: str) -> str:
    """
    Build a shell command that greets the user by embedding their nickname into
    `base_command`. The nickname is safely escaped using shlex.quote to avoid
    shell injection (CWE-74).

    Parameters
    ----------
    nickname : str
        The user supplied name.
    base_command : str
        A command template containing the placeholder '{nickname}'.

    Returns
    -------
    str
        The fully formed shell command with the nickname safely quoted.
    """
    # Quote the user input so that any special characters are treated literally
    safe_nickname = shlex.quote(nickname)

    # Format the command with the quoted nickname
    return base_command.format(nickname=safe_nickname)