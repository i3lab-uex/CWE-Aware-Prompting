import shlex

def generate_greeting_command(user_name: str, base_command: str) -> str:
    """
    Generate a shell command that greets the user by name.

    Parameters
    ----------
    user_name : str
        The user-provided name to be embedded into the command.
    base_command : str
        A template string for the shell command with placeholder `{user_name}`.

    Returns
    -------
    str
        The generated shell command incorporating the user-provided name.
    
    Notes
    -----
    - The function uses ``shlex.quote`` to escape the user name, mitigating
      command injection risks. However, if ``base_command`` itself contains
      untrusted input or is constructed elsewhere, additional sanitization may be needed.
    """
    # Safely escape the user name for shell usage
    safe_name = shlex.quote(user_name)
    
    # Replace the placeholder with the escaped name
    command = base_command.format(user_name=safe_name)
    
    return command