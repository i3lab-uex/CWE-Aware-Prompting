import shlex

# Base command template with a placeholder for the user's name.
BASE_COMMAND = "echo 'Hello, {name_of_user}! Welcome to the system.'"

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
        A shell command string with the user's name safely quoted.
    """
    # Ensure the input is a string; if not, convert to str.
    name_str = str(name_of_user)

    # Quote the user-provided string to avoid shell injection.
    safe_name = shlex.quote(name_str)

    # Replace the placeholder with the quoted name.
    command = BASE_COMMAND.format(name_of_user=safe_name)

    return command