import shlex

def create_greeting_command(person_name: str) -> str:
    """
    Construct a shell command that greets the user safely.

    Parameters
    ----------
    person_name : str
        The name provided by the user to be inserted into the command.

    Returns
    -------
    str
        A shell command string that greets the user, with the name safely quoted.
    """
    # Define the base command template. The placeholder '{person_name}'
    # will be replaced by the user-provided name.
    base_command = "echo 'Hello, {person_name}!'"

    # Use shlex.quote to escape any shell-special characters in the name,
    # preventing command injection (CWE-74).
    safe_name = shlex.quote(person_name)

    # Insert the safely quoted name into the template.
    command = base_command.format(person_name=safe_name)

    return command