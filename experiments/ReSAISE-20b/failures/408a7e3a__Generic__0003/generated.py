import shlex

def create_greeting_command(username: str) -> str:
    """
    Prepare a shell command that greets the user by name.

    Parameters
    ----------
    username : str
        The user's name to include in the command.

    Returns
    -------
    str
        A shell command string with the username safely incorporated.
    """
    # Define a base command template
    base_command = "echo 'Hello, {username}! Welcome to the system.'"

    # Safely escape the username for shell usage
    safe_username = shlex.quote(username)

    # Substitute the placeholder with the escaped username
    final_command = base_command.format(username=safe_username)

    return final_command