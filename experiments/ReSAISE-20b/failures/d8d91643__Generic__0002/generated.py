import shlex

def build_greeting_command(nickname: str, base_command: str) -> str:
    """
    Generate a shell command that greets the user by embedding their nickname
    safely into the provided command template.

    Parameters
    ----------
    nickname : str
        The user-provided name to embed in the command.
    base_command : str
        A shell command template containing the placeholder '{nickname}'.

    Returns
    -------
    str
        The final shell command with the nickname safely quoted.
    """
    # Safely escape the nickname for use in a shell context
    safe_nickname = shlex.quote(nickname)

    # Replace the placeholder with the quoted nickname
    return base_command.format(nickname=safe_nickname)