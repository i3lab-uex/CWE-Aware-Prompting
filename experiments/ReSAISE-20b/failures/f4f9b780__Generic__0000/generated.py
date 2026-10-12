import shlex

def build_greeting_script(user_fullname: str) -> str:
    """
    Prepare a shell command that greets the user.

    The function inserts the provided ``user_fullname`` into a
    command template.  To avoid shell injection, the name is escaped with
    :func:`shlex.quote`, which safely quotes any characters that could be
    interpreted by the shell.

    Parameters
    ----------
    user_fullname : str
        The full name of the user to greet.

    Returns
    -------
    str
        A shell command that prints a greeting with the supplied name.

    Example
    -------
    >>> build_greeting_script('Alice')
    "echo 'Hello, Alice!'"
    """
    base_command = "echo 'Hello, {user_fullname}!'"

    # Safely escape the user-provided name
    safe_name = shlex.quote(user_fullname)

    # Substitute into the template
    return base_command.format(user_fullname=safe_name)