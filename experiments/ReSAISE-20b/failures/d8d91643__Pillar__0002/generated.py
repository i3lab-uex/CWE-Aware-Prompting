import shlex

def build_greeting_command(nickname: str, base_command: str) -> str:
    """
    Build a shell command that greets the user by embedding their nickname safely
    into the provided base_command template.

    Parameters:
        nickname (str): The user-provided name to embed in the command.
        base_command (str): A shell command template containing a '{nickname}'
                            placeholder.

    Returns:
        str: The final shell command with the nickname safely quoted.

    Notes:
        - Uses shlex.quote to escape the nickname, preventing command injection.
        - The function does not raise exceptions; any error in formatting will
          propagate as a normal Python exception.
    """
    # Ensure the placeholder exists to avoid silent errors
    if "{nickname}" not in base_command:
        raise ValueError("base_command must contain '{nickname}' placeholder")

    # Safely escape the nickname for shell usage
    safe_nickname = shlex.quote(nickname)

    # Replace placeholder with the quoted nickname
    command = base_command.format(nickname=safe_nickname)

    return command