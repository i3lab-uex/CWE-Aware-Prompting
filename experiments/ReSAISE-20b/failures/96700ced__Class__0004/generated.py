import shlex

def assemble_greet_command(name_of_user: str) -> str:
    """
    Construct a shell command that greets the user by inserting their name into
    a predefined template. The user's input is safely escaped to prevent shell
    injection (CWE-74).

    Parameters
    ----------
    name_of_user : str
        The user-provided name to include in the command.

    Returns
    -------
    str
        A shell command string with the user's name safely quoted.
    """
    # Predefined base command template
    base_command = "echo 'Hello, {name_of_user}!'"

    # Safely escape the user-provided name for shell usage
    safe_name = shlex.quote(name_of_user)

    # Replace the placeholder with the quoted name
    command = base_command.format(name_of_user=safe_name)

    return command