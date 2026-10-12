import shlex

def create_greeting_command(person_name: str) -> str:
    """
    Construct a safe shell command that greets the user.

    Parameters
    ----------
    person_name : str
        The name provided by the user. It will be quoted to prevent shell injection.

    Returns
    -------
    str
        A shell command string that greets the user, e.g.
        'echo "Hello, Alice!"'.
    """
    # Base command template with a placeholder for the person's name.
    base_command = 'echo "Hello, {person_name}!"'

    # Sanitize the user input to avoid shell injection.
    safe_name = shlex.quote(person_name)

    # Insert the sanitized name into the template.
    command = base_command.format(person_name=safe_name)

    return command