import shlex

# Base command template that expects a user placeholder.
BASE_COMMAND = "echo 'Hello, {user}!'"

def prepare_greet_command(user: str) -> str:
    """
    Prepare a shell command that greets the specified user.

    The function safely escapes the user-provided name to prevent
    command injection attacks.  It uses :func:`shlex.quote` which
    wraps the string in single quotes and escapes any embedded
    single quotes appropriately.

    Parameters
    ----------
    user : str
        The name of the user to greet.

    Returns
    -------
    str
        A shell command string with the escaped user name inserted.
    """
    # Ensure the input is a string
    if not isinstance(user, str):
        raise TypeError("user must be a string")

    # Escape the user input
    safe_user = shlex.quote(user)

    # Insert into the command template
    return BASE_COMMAND.format(user=safe_user)