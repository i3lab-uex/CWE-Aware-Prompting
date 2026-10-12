import shlex

def create_greeting_command(username: str) -> str:
    """
    Prepare a shell command that greets the user by inserting their name
    into a predefined template. The username is safely escaped to avoid
    command injection vulnerabilities.

    Parameters
    ----------
    username : str
        The user's name to be inserted into the command.

    Returns
    -------
    str
        A shell command string that can be safely executed.
    """
    # Define the base command template with a placeholder
    base_command = "echo \"Hello, {username}!\""

    # Sanitize the username for safe shell usage
    sanitized_username = shlex.quote(username)

    # Format the command with the escaped username
    final_command = base_command.format(username=sanitized_username)

    return final_command