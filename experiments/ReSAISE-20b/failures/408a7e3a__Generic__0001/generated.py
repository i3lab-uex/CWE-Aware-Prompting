import shlex

# Base command template containing a placeholder for the username.
BASE_COMMAND = "echo 'Hello, {username}!'"

def create_greeting_command(username: str) -> str:
    """
    Safely prepares a shell command that greets the user.

    Parameters
    ----------
    username : str
        The user's name to be inserted into the command.

    Returns
    -------
    str
        A shell command string with the username safely quoted.
    """
    # Quote the user-provided name to prevent shell injection
    safe_username = shlex.quote(username)
    # Format the base command with the quoted username
    return BASE_COMMAND.format(username=safe_username)