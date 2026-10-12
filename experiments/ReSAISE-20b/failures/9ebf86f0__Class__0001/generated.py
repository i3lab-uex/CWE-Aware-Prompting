import shlex

# Base command template; replace `{user_name}` with the sanitized value.
base_command = "echo 'Hello, {user_name}!'"

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
        A safe shell command that echoes a greeting.
    
    Notes
    -----
    The function uses :func:`shlex.quote` to escape the user input,
    preventing command injection (CWE‑74).
    """
    # Escape the user input to prevent shell metacharacters from being interpreted.
    safe_name = shlex.quote(user_name)

    # Construct the final command using the escaped name.
    return base_command.format(user_name=safe_name)