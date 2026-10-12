import shlex

def create_greeting_command(username: str) -> str:
    """
    Prepare a shell command that greets the user by name.

    Parameters
    ----------
    username : str
        The user's name to include in the command. Must be safely escaped.

    Returns
    -------
    str
        A shell command string that greets the user.
    """
    # Base command template with a placeholder for the username
    base_command = "echo 'Hello, {username}! Welcome!'"

    # Use shlex.quote to escape any special shell characters in the username
    safe_username = shlex.quote(username)

    # Replace the placeholder with the escaped username
    final_command = base_command.format(username=safe_username)

    return final_command