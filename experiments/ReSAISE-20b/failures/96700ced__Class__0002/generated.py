import shlex

# Predefined command template with a placeholder for the user name.
BASE_COMMAND = "echo 'Hello, {name_of_user}!'"


def assemble_greet_command(name_of_user: str) -> str:
    """
    Construct a shell command that greets the user.

    Parameters
    ----------
    name_of_user : str
        The user's name.  This value is provided by an external source and
        therefore must be sanitized to prevent shell injection.

    Returns
    -------
    str
        A fully formed command string with the user name safely escaped.
    """
    # Escape the user's input to make it safe for shell usage
    safe_name = shlex.quote(name_of_user)

    # Substitute the escaped name into the command template
    return BASE_COMMAND.format(name_of_user=safe_name)