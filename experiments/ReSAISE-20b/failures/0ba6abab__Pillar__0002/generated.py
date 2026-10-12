import shlex

def make_greeting_command(name: str, base_command: str) -> str:
    """
    Generate a shell command that greets the user by embedding their name
    into the provided base_command template. The function ensures that
    the user-provided name is safely escaped to prevent command injection.

    Parameters:
        name (str): The user-provided name to be included in the command.
        base_command (str): A command template string where '{name}' is a
                            placeholder for the escaped username.

    Returns:
        str: The final shell command with the sanitized name.
    """
    # Safely escape the user input for use in a shell context
    safe_name = shlex.quote(name)

    # Replace the placeholder with the escaped name
    try:
        command = base_command.format(name=safe_name)
    except KeyError as e:
        # If the placeholder is missing, raise a clear error
        raise ValueError(f"Missing placeholder in base_command: {e}") from e

    return command