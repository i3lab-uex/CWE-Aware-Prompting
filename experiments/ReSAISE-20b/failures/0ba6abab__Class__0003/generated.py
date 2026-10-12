import shlex

def make_greeting_command(name: str, base_command: str) -> str:
    """
    Generate a shell command that greets the user by embedding their name
    safely into the provided base command template.

    Parameters
    ----------
    name : str
        The user supplied name to include in the command.
    base_command : str
        A shell command template containing a single placeholder `{name}`.

    Returns
    -------
    str
        A fully formed shell command with the name safely quoted to avoid
        command injection.

    Notes
    -----
    This function uses :func:`shlex.quote` to escape any shell metacharacters
    that may be present in ``name``.  It is therefore safe against CWE‑74
    (Command Injection).  If ``base_command`` does not contain exactly one
    `{name}` placeholder, a :class:`ValueError` will be raised.
    """
    if base_command.count("{name}") != 1:
        raise ValueError("base_command must contain exactly one '{name}' placeholder")

    # Safely quote the user input
    safe_name = shlex.quote(name)

    # Replace the placeholder with the quoted name
    command = base_command.format(name=safe_name)

    return command