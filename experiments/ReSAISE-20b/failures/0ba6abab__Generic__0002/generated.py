import shlex

def make_greeting_command(name: str, base_command: str = "echo 'Hello, {name}!'") -> str:
    """
    Generate a shell command that greets the user by embedding their name
    safely into the provided base_command template.

    Parameters
    ----------
    name : str
        The user supplied name to include in the command.
    base_command : str, optional
        A command template containing a single '{name}' placeholder.

    Returns
    -------
    str
        The final shell command with the name safely quoted.
    """
    # Sanitize the user input to prevent shell injection
    safe_name = shlex.quote(name)

    # Replace the placeholder with the sanitized name
    command = base_command.format(name=safe_name)

    return command