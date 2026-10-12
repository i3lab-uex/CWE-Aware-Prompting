import shlex

# Base command template with a placeholder for the person's name.
BASE_COMMAND = "echo 'Hello, {person_name}!'"

def create_greeting_command(person_name: str) -> str:
    """
    Construct a shell command that greets the user.

    Parameters
    ----------
    person_name : str
        The name supplied by the user.  It is quoted with ``shlex.quote`` to
        prevent shell injection attacks and to handle any special characters.

    Returns
    -------
    str
        A safe shell command string with the user's name inserted.
    """
    # Escape the user supplied name for safe inclusion in a shell command.
    safe_name = shlex.quote(person_name)

    # Replace the placeholder with the quoted name.
    command = BASE_COMMAND.format(person_name=safe_name)

    return command