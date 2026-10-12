import shlex

def assemble_greet_command(name_of_user: str, base_command: str = "echo 'Hello, {name_of_user}!'" ) -> str:
    """
    Construct a shell command that greets the user by name.

    Parameters
    ----------
    name_of_user : str
        The user's name to be inserted into the command.
    base_command : str, optional
        A template for the shell command that must contain the placeholder
        '{name_of_user}'.  The default value is a simple echo greeting.

    Returns
    -------
    str
        A shell command string with the user's name safely quoted to avoid
        shell injection.

    Notes
    -----
    This function uses :func:`shlex.quote` to escape the user supplied name.
    That mitigates command injection attacks (CWE-78).  The function still
    relies on the caller to provide a sane ``base_command``; if the template
    contains additional shell syntax that is not properly escaped, a
    vulnerability may still exist.
    """
    # Ensure the placeholder exists in the template
    if "{name_of_user}" not in base_command:
        raise ValueError("base_command must contain the placeholder '{name_of_user}'")

    # Safely escape the user input for shell usage
    safe_name = shlex.quote(name_of_user)

    # Replace the placeholder with the escaped name
    command = base_command.replace("{name_of_user}", safe_name)

    return command