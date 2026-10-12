import shlex

# Predefined command template with a placeholder for the user's name.
BASE_COMMAND = "echo 'Hello, {name_of_user}!'"  # Example template


def assemble_greet_command(name_of_user: str) -> str:
    """
    Construct a shell command that greets the user by name.

    Parameters
    ----------
    name_of_user : str
        The user's supplied name to be inserted into the command.

    Returns
    -------
    str
        A shell command string with the user's name safely quoted to avoid
        command injection.

    Notes
    -----
    The function uses :func:`shlex.quote` to escape any special shell characters
    that might be present in ``name_of_user``. This mitigates the risk of CWE‑74
    (Command Injection) by ensuring that the injected value cannot alter the
    structure of the shell command.
    """
    # Sanitize the user input to prevent shell injection
    safe_name = shlex.quote(name_of_user)

    # Replace the placeholder with the sanitized name
    return BASE_COMMAND.format(name_of_user=safe_name)