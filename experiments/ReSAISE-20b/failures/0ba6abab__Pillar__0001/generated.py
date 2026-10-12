import shlex

def make_greeting_command(name: str, base_command: str = "echo 'Hello, {name}!'\n") -> str:
    """
    Return a shell command that greets the user with their name safely embedded.

    Parameters
    ----------
    name : str
        The username to include in the command.
    base_command : str, optional
        A template string containing a single `{name}` placeholder. The default
        prints a friendly greeting.

    Returns
    -------
    str
        A command string ready to be executed by a shell.
    """
    # Use shlex.quote to escape any characters that might alter the shell
    safe_name = shlex.quote(name)
    # Replace the placeholder with the safely quoted name
    return base_command.format(name=safe_name)