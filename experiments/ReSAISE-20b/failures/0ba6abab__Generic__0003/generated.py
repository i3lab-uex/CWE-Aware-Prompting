import shlex

def make_greeting_command(name: str, base_command: str) -> str:
    """
    Generate a shell command that greets the user by embedding their name
    into the provided base_command template.

    Parameters:
        name (str): The user supplied name.
        base_command (str): A command template containing a '{name}' placeholder.

    Returns:
        str: The final shell command with the user's name safely quoted.
    """
    # Safely quote the user-provided input to avoid command injection
    safe_name = shlex.quote(name)
    # Replace the placeholder with the quoted name
    return base_command.format(name=safe_name)