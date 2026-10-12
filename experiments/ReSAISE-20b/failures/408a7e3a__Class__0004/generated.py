import shlex

# Base command template with a placeholder for the username.
BASE_COMMAND = "echo 'Hello, {username}!'"

def create_greeting_command(username: str) -> str:
    """
    Prepare a shell command that greets the user by name.

    Parameters
    ----------
    username : str
        The user's name to include in the greeting command.

    Returns
    -------
    str
        A shell command string with the username safely quoted to prevent
        injection attacks.

    Notes
    -----
    The function uses :func:`shlex.quote` to escape any characters that could
    alter the command's semantics. This mitigates CWE-74 by ensuring that the
    user input is treated as a literal string rather than executable code.
    """
    # Sanitize the username to prevent shell injection
    safe_username = shlex.quote(username)

    # Build and return the final command string
    return BASE_COMMAND.format(username=safe_username)