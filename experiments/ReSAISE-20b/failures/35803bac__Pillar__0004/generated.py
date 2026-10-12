import shlex

def create_greeting_command(person_name: str, base_command: str = "echo 'Hello, {person_name}!'" ) -> str:
    """
    Construct a shell command that greets the user by name.

    Parameters
    ----------
    person_name : str
        The user's name to be inserted into the command.
    base_command : str, optional
        A template containing a single placeholder `{person_name}`.

    Returns
    -------
    str
        The shell command with the user's name safely quoted.
    """
    # Ensure that the placeholder exists in the template
    if "{person_name}" not in base_command:
        raise ValueError("The base command must contain the placeholder '{person_name}'.")

    # Use shlex.quote to escape the name for safe shell usage
    quoted_name = shlex.quote(person_name)

    # Safely substitute the placeholder with the escaped name
    command = base_command.replace("{person_name}", quoted_name)

    return command