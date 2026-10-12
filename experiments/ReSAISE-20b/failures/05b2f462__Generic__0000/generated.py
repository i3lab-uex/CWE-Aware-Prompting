import shlex

def prepare_greet_command(user: str) -> str:
    """
    Prepare a shell command that greets the user.

    Parameters
    ----------
    user : str
        The name of the user to greet.  This value is sanitized by quoting it
        so that shell metacharacters cannot be interpreted.

    Returns
    -------
    str
        A command string that safely incorporates the user's name.
    """
    base_command = "echo 'Hello, {user}!'"

    # Quote the user string to avoid shell injection
    safe_user = shlex.quote(user)

    return base_command.format(user=safe_user)