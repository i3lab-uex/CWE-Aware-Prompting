import shlex

def build_greeting_script(user_fullname: str, base_command: str) -> str:
    """
    Prepare a shell command that greets the user.

    The function safely incorporates the supplied `user_fullname` into
    the `base_command`.  It uses :func:`shlex.quote` to escape any
    characters that could be interpreted by the shell, preventing
    command‑injection vulnerabilities (CWE‑74).

    Parameters
    ----------
    user_fullname : str
        The full name of the user to be inserted into the command.
    base_command : str
        A shell command template containing a single placeholder
        ``{user_fullname}`` that will be replaced by the escaped name.

    Returns
    -------
    str
        The fully formed, safe shell command ready for execution.
    """
    # Quote the user input so that it cannot break out of its intended
    # position in the command line.
    safe_name = shlex.quote(user_fullname)

    # Replace the placeholder with the quoted name.
    return base_command.format(user_fullname=safe_name)