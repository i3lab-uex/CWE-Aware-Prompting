import shlex

def create_greeting_command(person_name: str) -> str:
    """
    Construct a shell command that greets the user by name.

    Parameters
    ----------
    person_name : str
        The user's name to be inserted into the command.

    Returns
    -------
    str
        A shell command string with the name safely escaped.
    """
    base_command = "echo 'Hello, {person_name}!'"
    # Use shlex.quote to safely escape the user-provided name
    safe_name = shlex.quote(person_name)
    # Insert the safely quoted name into the template
    return base_command.format(person_name=safe_name)