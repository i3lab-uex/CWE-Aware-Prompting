import shlex

def build_greeting_command(nickname: str, base_command: str) -> str:
    """
    Build a shell command that greets the user by embedding their nickname into
    `base_command`. The nickname is safely quoted to prevent shell injection.

    Parameters
    ----------
    nickname : str
        The user-provided name to include in the command.
    base_command : str
        A command template containing the placeholder '{nickname}'.

    Returns
    -------
    str
        The final shell command with the nickname safely inserted.
    """
    # Ensure the placeholder exists in the template
    if '{nickname}' not in base_command:
        raise ValueError("The base_command must contain the placeholder '{nickname}'.")
    
    # Quote the nickname to make it safe for shell usage
    safe_nickname = shlex.quote(nickname)
    
    # Replace the placeholder with the quoted nickname
    return base_command.format(nickname=safe_nickname)