import shlex

def prepare_greet_command(user: str) -> str:
    """
    Prepare a shell command that greets the user.

    Parameters
    ----------
    user : str
        The user's name to be inserted into the command.

    Returns
    -------
    str
        A shell command string that safely includes the user name.
    """
    # Base command template. Adjust as needed for your environment.
    base_command = "echo 'Hello, {user}! Welcome!'"

    # Sanitize the user input to prevent command injection.
    safe_user = shlex.quote(user)

    # Insert the sanitized user into the template.
    return base_command.format(user=safe_user)