import shlex

def create_greeting_command(username: str) -> str:
    """
    Construct a shell command that greets the user by name.

    Parameters
    ----------
    username : str
        The user's name to embed in the command. It will be safely escaped.

    Returns
    -------
    str
        The final shell command ready for execution.
    """
    # Base command template with a placeholder for the username
    base_command = "echo 'Hello, {username}! Welcome to the system.'"

    # Safely escape the username to prevent command injection
    safe_username = shlex.quote(username)

    # Substitute the escaped username into the template
    return base_command.format(username=safe_username)