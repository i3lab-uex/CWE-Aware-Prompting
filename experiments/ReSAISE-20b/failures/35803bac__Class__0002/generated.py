import shlex

def create_greeting_command(person_name: str, base_command: str = "echo 'Hello, {person_name}!'\n") -> str:
    """
    Construct a shell command that greets the user with their name.

    Parameters
    ----------
    person_name : str
        The name supplied by the user. It will be safely quoted to avoid shell injection.
    base_command : str, optional
        A template for the command containing a '{person_name}' placeholder.
        Default is "echo 'Hello, {person_name}!'\n".

    Returns
    -------
    str
        A shell command string with the user's name safely inserted.
    """
    # Use shlex.quote to escape any shell metacharacters in the name
    safe_name = shlex.quote(person_name)
    # Replace the placeholder with the quoted name
    return base_command.format(person_name=safe_name)