import shlex

def make_greeting_command(name: str, base_command: str = "echo 'Hello, {name}!'" ) -> str:
    """
    Generate a shell command that greets the user with their name.

    Parameters
    ----------
    name : str
        The user's name to embed in the command.
    base_command : str, optional
        A template string containing a single `{name}` placeholder that will be
        replaced with the quoted name.  Defaults to ``"echo 'Hello, {name}!'"``.

    Returns
    -------
    str
        The fully formatted shell command with the user's name safely quoted.

    Notes
    -----
    The function uses :func:`shlex.quote` to escape the name so that any shell
    metacharacters are neutralised, preventing command injection attacks.
    """
    # Safely escape the user-provided name for shell usage
    safe_name = shlex.quote(name)

    # Substitute the escaped name into the command template
    return base_command.format(name=safe_name)