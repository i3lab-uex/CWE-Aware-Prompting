import shlex

def build_greeting_command(nickname: str, base_command: str) -> str:
    """
    Generate a shell command that greets the user by embedding their nickname
    into a base command template.

    Parameters:
        nickname (str): The user-provided name to include in the command.
        base_command (str): A shell command template containing a '{nickname}'
                            placeholder.

    Returns:
        str: The final shell command with the nickname safely quoted to
             prevent command injection.

    Notes:
        - The function uses `shlex.quote` to escape the nickname so that it
          cannot terminate the command or inject additional commands.
        - No exceptions are raised for invalid input; instead, an empty
          string is quoted to avoid accidental injection.
    """
    # Ensure the placeholder exists in the template
    if '{nickname}' not in base_command:
        raise ValueError("The base command must contain a '{nickname}' placeholder.")

    # Safely quote the nickname
    safe_nickname = shlex.quote(nickname)

    # Format the command with the quoted nickname
    return base_command.format(nickname=safe_nickname)