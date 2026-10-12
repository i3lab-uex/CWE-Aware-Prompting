import shlex

def build_greeting_command(nickname: str, base_command: str) -> str:
    """
    Build a shell command that greets the user by embedding their nickname into
    the provided base_command template. The nickname is safely escaped using
    shlex.quote to prevent command injection.

    Parameters:
        nickname (str): The user-provided name.
        base_command (str): A command template containing the placeholder
                            '{nickname}' where the escaped name should be inserted.

    Returns:
        str: The fully constructed shell command.
    """
    # Escape the nickname so that it cannot terminate or modify the command
    safe_nickname = shlex.quote(nickname)

    # Replace the placeholder with the safely escaped nickname
    return base_command.format(nickname=safe_nickname)