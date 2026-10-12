import shlex

# Template for the greeting command. The placeholder {user_name}
# will be replaced with the sanitized user name.
BASE_COMMAND = "echo 'Hello, {user_name}!'"


def generate_greeting_command(user_name: str) -> str:
    """
    Generate a shell command that greets the user by name.

    Parameters
    ----------
    user_name : str
        The user-provided name to be embedded into the command.

    Returns
    -------
    str
        The generated shell command incorporating the user-provided name.
        The name is safely escaped using shlex.quote to mitigate
        command‑injection risks.

    Notes
    -----
    This function only constructs the command string.  Execution of the
    command must be performed by a separate `execute_command` function.
    """
    # Sanitize the user name to avoid shell injection.
    safe_name = shlex.quote(user_name)

    # Insert the sanitized name into the command template.
    return BASE_COMMAND.format(user_name=safe_name)