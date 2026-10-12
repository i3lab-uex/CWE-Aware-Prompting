import shlex

def build_greeting_command(nickname: str, base_command: str = "echo 'Hello, {nickname}!'") -> str:
    """
    Build a shell command that greets the user by name.

    Parameters
    ----------
    nickname : str
        The user's name to be inserted into the command.
    base_command : str, optional
        A template string containing a '{nickname}' placeholder. Defaults to
        "echo 'Hello, {nickname}!'".

    Returns
    -------
    str
        A shell command with the nickname safely escaped to avoid command
        injection vulnerabilities.
    """
    # Escape the user-provided nickname so that it is treated as a single
    # argument by the shell.
    safe_nickname = shlex.quote(nickname)

    # Substitute the escaped nickname into the template.
    return base_command.format(nickname=safe_nickname)