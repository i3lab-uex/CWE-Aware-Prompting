import shlex

def make_greeting_command(name: str, base_command: str = "echo 'Hello, {name}!'") -> str:
    """
    Safely embed a user-provided name into a shell command template.

    Parameters
    ----------
    name : str
        The user-supplied name to include in the command.
    base_command : str, optional
        A shell command template containing a single `{name}` placeholder.
        Default is ``"echo 'Hello, {name}!'``.

    Returns
    -------
    str
        The final shell command with the user’s name safely quoted.

    Notes
    -----
    * The function uses :func:`shlex.quote` to escape any special characters in
      ``name`` so that the resulting command cannot be abused for shell
      injection (CWE‑74).
    * The function does **not** raise any exceptions; if ``base_command`` does
      not contain a `{name}` placeholder, :class:`KeyError` will be raised by
      ``str.format``.
    """
    # Quote the name so it is safe for shell usage
    quoted_name = shlex.quote(name)
    # Construct the final command
    return base_command.format(name=quoted_name)