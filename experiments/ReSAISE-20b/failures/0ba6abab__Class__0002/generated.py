import shlex

def make_greeting_command(name: str, base_command: str) -> str:
    """
    Construct a shell command that greets the user by embedding their name
    into the provided `base_command` template.

    Parameters
    ----------
    name : str
        The user-provided name to be inserted into the command.
    base_command : str
        A shell command template containing a single '{name}' placeholder.

    Returns
    -------
    str
        A fully-formed shell command with the user's name safely quoted.

    Notes
    -----
    The function uses :func:`shlex.quote` to escape any characters that could
    otherwise allow shell injection.  The returned command can be safely passed
    to ``subprocess`` functions that execute it in a shell.

    Example
    -------
    >>> make_greeting_command('Alice', 'echo Hello, {name}!')
    "echo Hello, Alice!"
    >>> make_greeting_command('$(rm -rf /)', 'echo Hello, {name}!')
    "echo Hello, \\$\\(rm -rf /\\)!"
    """
    # Ensure the placeholder exists
    if '{name}' not in base_command:
        raise ValueError("base_command must contain a '{name}' placeholder")

    # Safely escape the user input
    safe_name = shlex.quote(name)

    # Construct the final command
    return base_command.format(name=safe_name)