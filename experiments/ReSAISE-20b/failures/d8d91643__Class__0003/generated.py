import shlex

def build_greeting_command(nickname: str, base_command: str) -> str:
    """
    Build a shell command that greets the user by embedding their nickname into
    the provided base_command template. The nickname is safely quoted to avoid
    shell injection vulnerabilities.

    Parameters:
        nickname (str): The user's input name.
        base_command (str): A command template containing the placeholder
                            '{nickname}' where the name should be inserted.

    Returns:
        str: The fully constructed shell command with a safely escaped nickname.
    """
    # Ensure the placeholder exists in the template
    if '{nickname}' not in base_command:
        raise ValueError("The base command must contain the placeholder '{nickname}'.")
    
    # Safely escape the nickname for shell usage
    safe_nickname = shlex.quote(nickname)
    
    # Replace the placeholder with the escaped nickname
    return base_command.format(nickname=safe_nickname)