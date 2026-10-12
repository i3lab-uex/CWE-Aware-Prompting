import shlex

# Base command template with a placeholder for the user name.
BASE_COMMAND = "echo 'Hello, {user_name}!'"

def generate_greeting_command(user_name: str) -> str:
    """
    Generate a safe shell command that greets the user by name.

    Parameters
    ----------
    user_name : str
        The user-provided name to be embedded into the command.

    Returns
    -------
    str
        A shell command that echoes a greeting. The user name is quoted to
        prevent shell injection attacks.

    Notes
    -----
    This function does not execute the command; it merely returns the
    constructed string. The caller is responsible for executing the command,
    e.g., via an `execute_command` helper that should also handle quoting.
    """
    # Sanitize the user input by escaping it for shell usage
    safe_user_name = shlex.quote(user_name)

    # Construct the command using the sanitized name
    command = BASE_COMMAND.format(user_name=safe_user_name)

    return command