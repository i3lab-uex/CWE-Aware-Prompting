import shlex

def make_greeting_command(name: str, base_command: str) -> str:
    """
    Generate a shell command that greets the user by embedding their name
    into `base_command`. The user's input is safely escaped to avoid
    command‑injection vulnerabilities.

    Parameters
    ----------
    name : str
        The username supplied by the user.
    base_command : str
        A command template containing a `{name}` placeholder where the
        escaped username should be inserted.

    Returns
    -------
    str
        The fully formed shell command with the username safely quoted.
    """
    # Escape the user supplied name to ensure it cannot break out of
    # the intended command context.  shlex.quote returns a string that
    # is safe to use in POSIX shells.
    escaped_name = shlex.quote(name)

    # Perform a safe substitution.  We avoid using `str.format` directly
    # with untrusted input by quoting the value first.
    return base_command.replace("{name}", escaped_name)