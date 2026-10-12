import shlex

def make_greeting_command(name: str, base_command: str = "echo 'Hello, {name}!'") -> str:
    """
    Generate a shell command that greets the user by name.

    Parameters
    ----------
    name : str
        The user-provided name to embed in the command.
    base_command : str, optional
        A template containing a '{name}' placeholder.  Defaults to a simple
        echo greeting.

    Returns
    -------
    str
        The final shell command with the name safely quoted.
    """
    # Quote the user input to prevent shell injection
    safe_name = shlex.quote(name)
    return base_command.format(name=safe_name)