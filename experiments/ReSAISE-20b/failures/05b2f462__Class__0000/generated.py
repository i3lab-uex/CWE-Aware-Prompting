import shlex

def prepare_greet_command(user: str) -> str:
    """
    Prepare a shell command that greets the user.

    The base command template contains a `{user}` placeholder which will be
    replaced with the provided user name.  To mitigate shell injection (CWE‑74),
    the user input is safely escaped using :func:`shlex.quote`.

    Parameters
    ----------
    user: str
        The user's name to be inserted into the command.

    Returns
    -------
    str
        A fully formed shell command string with the user name safely quoted.

    Examples
    --------
    >>> prepare_greet_command('Alice')
    "echo \"Hello, Alice!\""

    >>> prepare_greet_command('$(rm -rf /)')
    'echo "Hello, $(rm -rf /)!"'
    """
    # Define the command template.  The placeholder `{user}` will be
    # replaced by the escaped user name.
    base_command = 'echo "Hello, {user}!"'

    # Use shlex.quote to safely escape any characters that could be
    # interpreted by the shell.
    safe_user = shlex.quote(user)

    # Insert the escaped user name into the template
    final_command = base_command.format(user=safe_user)

    return final_command