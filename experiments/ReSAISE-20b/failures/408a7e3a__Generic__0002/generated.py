import shlex

# The command template with a placeholder for the username.
BASE_COMMAND = "echo 'Hello, {username}!'"

def create_greeting_command(username: str) -> str:
    """
    Prepare a shell command that greets the user.

    Parameters
    ----------
    username : str
        The name of the user to greet. It will be safely quoted before
        being inserted into the command string.

    Returns
    -------
    str
        The final shell command ready to be executed.
    """
    # Quote the username to prevent shell injection attacks.
    safe_username = shlex.quote(username)

    # Insert the safely quoted username into the command template.
    return BASE_COMMAND.format(username=safe_username)