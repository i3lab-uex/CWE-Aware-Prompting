import shlex

def assemble_greet_command(name_of_user: str, base_command: str = "echo 'Hello, {name_of_user}!'") -> str:
    """
    Construct a shell command that greets the user by name.

    Parameters
    ----------
    name_of_user : str
        The user's name to insert into the command.
    base_command : str, optional
        Template for the shell command containing the placeholder `{name_of_user}`.

    Returns
    -------
    str
        A shell command string with the user's name safely quoted.
    """
    # Quote the user-provided name to prevent shell injection
    safe_name = shlex.quote(name_of_user)

    # Replace the placeholder with the quoted name
    return base_command.format(name_of_user=safe_name)