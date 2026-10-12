import shlex

def assemble_greet_command(name_of_user: str) -> str:
    """
    Construct a shell command that greets the user.

    Parameters
    ----------
    name_of_user : str
        The user's name to be inserted into the command.

    Returns
    -------
    str
        A shell command string with the name safely quoted.
    """
    base_command = "echo 'Hello, {name_of_user}!'"
    # Quote the user-provided name to avoid shell injection.
    safe_name = shlex.quote(name_of_user)
    # Replace the placeholder with the quoted name.
    command = base_command.format(name_of_user=safe_name)
    return command