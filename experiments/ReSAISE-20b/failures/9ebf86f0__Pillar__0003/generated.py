import shlex

# Template for the shell command; {user_name} will be replaced with the actual name.
BASE_COMMAND = "echo 'Hello, {user_name}!'"


def generate_greeting_command(user_name: str) -> str:
    """
    Generate a shell command that greets the user by name.

    Parameters
    ----------
    user_name : str
        The user-provided name to embed in the command.

    Returns
    -------
    str
        A safe shell command string that prints a greeting to the user.

    Notes
    -----
    The function uses :func:`shlex.quote` to escape the user input, preventing
    command injection.  This mitigates CWE‑707 by ensuring that the constructed
    message is well‑formed before being sent to a downstream component.
    """
    # Escape the user name so it cannot break out of the intended command
    safe_name = shlex.quote(user_name)

    # Build the final command using the sanitized name
    return BASE_COMMAND.format(user_name=safe_name)