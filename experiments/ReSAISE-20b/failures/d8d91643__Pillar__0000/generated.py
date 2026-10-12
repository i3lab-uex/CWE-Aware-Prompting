import shlex

def build_greeting_command(nickname: str, base_command: str = "echo 'Hello, {nickname}! Welcome!'") -> str:
    """
    Build a shell command that greets the user by embedding their nickname into the
    provided base_command template. The nickname is safely escaped using shlex.quote
    to prevent command injection.

    Parameters:
        nickname (str): The user's name to embed.
        base_command (str): A template containing the placeholder '{nickname}'.

    Returns:
        str: The final shell command with the sanitized nickname.
    """
    if "{nickname}" not in base_command:
        raise ValueError("Base command must contain the '{nickname}' placeholder.")

    # Safely escape the nickname to avoid shell injection
    safe_nickname = shlex.quote(nickname)

    # Construct the final command using a safe placeholder
    return base_command.format(nickname=safe_nickname)