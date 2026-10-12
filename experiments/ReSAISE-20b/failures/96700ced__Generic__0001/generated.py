import shlex

# Predefined shell command template with a placeholder for the user name.
BASE_COMMAND_TEMPLATE = "echo 'Hello, {name_of_user}!'"


def assemble_greet_command(name_of_user: str) -> str:
    """
    Construct a shell command that greets the user safely.

    Parameters
    ----------
    name_of_user : str
        The name supplied by the user.  It will be escaped to avoid shell injection.

    Returns
    -------
    str
        A fully formed shell command string with the user's name safely inserted.
    """
    # Escape the user-provided value so it cannot break out of the string literal
    safe_name = shlex.quote(name_of_user)

    # Insert the escaped name into the command template
    return BASE_COMMAND_TEMPLATE.format(name_of_user=safe_name)