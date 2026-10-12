import shlex

# Base command template with a placeholder for the person's name.
BASE_COMMAND = "echo 'Hello, {person_name}!'"

def create_greeting_command(person_name: str) -> str:
    """
    Construct a shell command that greets the user by name.

    Parameters
    ----------
    person_name : str
        The name supplied by the user.  It will be safely escaped before
        being inserted into the command string to prevent shell injection.

    Returns
    -------
    str
        A fully-formed shell command with the user's name safely quoted.
    """
    # Escape the user-supplied name so that it cannot break out of the
    # intended quoting context.  This mitigates CWE-74 (command injection).
    safe_name = shlex.quote(person_name)

    # Insert the escaped name into the command template.
    return BASE_COMMAND.format(person_name=safe_name)