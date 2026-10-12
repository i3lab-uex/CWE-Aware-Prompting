import shlex

def create_greeting_command(person_name: str, base_command: str = "echo 'Hello, {person_name}!'") -> str:
    """
    Construct a shell command that greets the user by name.

    Parameters
    ----------
    person_name : str
        The name supplied by the user.  It is sanitized to prevent shell injection.
    base_command : str, optional
        A template containing the placeholder '{person_name}'.  The default uses a simple echo.

    Returns
    -------
    str
        A shell command string with the user name safely quoted.
    """
    # Use shlex.quote to escape any characters that could be interpreted by the shell
    safe_name = shlex.quote(person_name)
    # Replace placeholder with the quoted name
    return base_command.format(person_name=safe_name)