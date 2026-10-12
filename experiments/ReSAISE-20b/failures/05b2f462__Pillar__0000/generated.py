import shlex

def prepare_greet_command(user: str) -> str:
    """
    Safely prepares a shell command that greets the user.

    Parameters
    ----------
    user : str
        The user's name to include in the command. It will be quoted so that
        special characters cannot break out of the intended argument.

    Returns
    -------
    str
        The fully constructed shell command string.
    """
    base_command = "echo 'Hello, {user}!'"
    # Quote the user input to avoid shell injection
    safe_user = shlex.quote(user)
    return base_command.format(user=safe_user)