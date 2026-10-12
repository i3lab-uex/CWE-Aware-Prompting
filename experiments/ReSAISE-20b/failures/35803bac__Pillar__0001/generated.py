import shlex

def create_greeting_command(person_name: str) -> str:
    """
    Construct a shell command that greets the user by name.

    Parameters
    ----------
    person_name : str
        The name to insert into the command.  It is escaped using shlex.quote
        to prevent shell injection attacks.

    Returns
    -------
    str
        The fully-formed command string with the name safely quoted.
    """
    # Predefined shell command template
    base_command = "echo 'Hello, {person_name}! Welcome!'"

    # Safely escape the user-provided name
    safe_name = shlex.quote(person_name)

    # Substitute the placeholder with the escaped name
    command = base_command.format(person_name=safe_name)

    return command