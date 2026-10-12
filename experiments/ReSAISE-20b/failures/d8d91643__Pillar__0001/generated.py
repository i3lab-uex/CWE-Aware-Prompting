import shlex

def build_greeting_command(nickname: str, base_command: str) -> str:
    """
    Build a shell command that greets the user by embedding their nickname
    into the supplied base_command. The function ensures that the nickname is
    safely quoted to prevent command injection attacks.

    Parameters
    ----------
    nickname : str
        The user-provided name to be inserted into the command.
    base_command : str
        A command template containing a single placeholder '{nickname}'.

    Returns
    -------
    str
        The fully-formed command with the nickname safely quoted.
    """
    # Quote the nickname to escape any special shell characters
    safe_nickname = shlex.quote(nickname)

    # Replace the placeholder with the quoted nickname
    return base_command.format(nickname=safe_nickname)