import shlex

def build_greeting_script(user_fullname: str, base_command: str = "echo 'Hello, {user_fullname}! Welcome!'") -> str:
    """
    Build a shell command that greets the user by name.

    Parameters
    ----------
    user_fullname : str
        The user's full name to be inserted into the command.
    base_command : str, optional
        Command template containing the placeholder `{user_fullname}`.

    Returns
    -------
    str
        A shell command string with the user's name safely quoted to prevent injection.

    Notes
    -----
    This function uses :func:`shlex.quote` to escape any characters that could be
    interpreted by the shell.  It is safe for use with most Unix‑like shells.
    """
    # Sanitize the user input to avoid shell injection
    safe_name = shlex.quote(user_fullname)

    # Replace the placeholder with the quoted name
    return base_command.format(user_fullname=safe_name)