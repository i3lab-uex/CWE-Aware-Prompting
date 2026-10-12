import shlex

# Base command template with a placeholder for the username.
BASE_COMMAND = "echo 'Hello, {username}!'"


def create_greeting_command(username: str) -> str:
    """
    Prepare a shell command that greets the user safely.

    Parameters
    ----------
    username : str
        The name of the user to greet. It may contain characters that need escaping.

    Returns
    -------
    str
        The final shell command with the username safely quoted.
    """
    # Quote the username so that it is safe to embed in a shell command.
    safe_username = shlex.quote(username)

    # Format the base command with the quoted username.
    return BASE_COMMAND.format(username=safe_username)