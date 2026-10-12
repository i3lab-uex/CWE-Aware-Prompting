import shlex

def prepare_greet_command(user: str) -> str:
    """
    Construct a safe shell command that greets the specified user.

    Parameters
    ----------
    user : str
        The name of the user to greet.  This value is treated as external input and
        must be properly escaped before being interpolated into the command string.

    Returns
    -------
    str
        A shell command that echoes a greeting to the user.  The returned string is
        safe for execution via tools such as `subprocess.run(..., shell=True)`.

    Notes
    -----
    The function uses :func:`shlex.quote` to neutralize any shell metacharacters
    that could lead to command injection (CWE‑74).  The template string contains a
    single placeholder ``{user}`` which is replaced by the escaped value.
    """
    # Template command with a placeholder for user input
    base_command = "echo 'Hello, {user}! Welcome to the system.'"

    # Escape user input for safe inclusion in a shell command
    safe_user = shlex.quote(user)

    # Substitute the escaped user into the template
    final_command = base_command.format(user=safe_user)

    return final_command