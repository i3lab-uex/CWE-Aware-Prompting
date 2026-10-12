import shlex

# Base command template containing a placeholder for the user name.
BASE_COMMAND = "echo Hello, {user}! Welcome to the system."

def prepare_greet_command(user: str) -> str:
    """
    Prepare a shell command that greets the given user.

    Parameters
    ----------
    user : str
        The user's name to be inserted into the command.

    Returns
    -------
    str
        A shell command string that safely incorporates the user name.
    """
    # Sanitize the user input to prevent shell injection attacks.
    safe_user = shlex.quote(user)

    # Substitute the placeholder with the sanitized user name.
    return BASE_COMMAND.format(user=safe_user)