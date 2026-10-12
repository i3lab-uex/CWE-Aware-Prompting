import shlex

# Template command with a placeholder for the user's full name.
BASE_COMMAND = "echo 'Hello, {user_fullname}!'"

def build_greeting_script(user_fullname: str) -> str:
    """
    Prepare a shell command that greets the user by name.

    Parameters
    ----------
    user_fullname : str
        The user's full name to embed in the command.

    Returns
    -------
    str
        A safe shell command string that includes the quoted user name.

    Notes
    -----
    - The function uses :func:`shlex.quote` to escape any characters that
      could otherwise be interpreted by the shell, preventing command
      injection attacks (CWE-78).
    - The returned string is safe to pass directly to ``subprocess`` with
      `shell=True` or to an interactive shell.
    """
    # Sanitize the user input by quoting it for safe inclusion in a shell command
    safe_name = shlex.quote(user_fullname)

    # Replace the placeholder with the sanitized name
    command = BASE_COMMAND.format(user_fullname=safe_name)

    return command