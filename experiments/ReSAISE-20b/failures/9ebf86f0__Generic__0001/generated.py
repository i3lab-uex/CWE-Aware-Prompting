import shlex

# Assume this function is provided elsewhere in the codebase.
def execute_command(cmd: str) -> None:
    """Execute a shell command. Implementation not shown."""
    pass


def generate_greeting_command(user_name: str, base_command: str = "echo Hello {user_name}") -> str:
    """
    Generate a shell command that greets the user by name.

    Parameters
    ----------
    user_name : str
        The user-provided name to be embedded into the command.
    base_command : str, optional
        A template string for the shell command with a placeholder `{user_name}`.
        Defaults to `"echo Hello {user_name}"`.

    Returns
    -------
    str
        The generated shell command incorporating the user-provided name.

    Notes
    -----
    The function sanitizes ``user_name`` using :func:`shlex.quote` to mitigate
    shell injection risks.  The sanitized name is then substituted into the
    ``base_command`` template.

    Raises
    ------
    ValueError
        If the base command does not contain a `{user_name}` placeholder.
    """
    if "{user_name}" not in base_command:
        raise ValueError("base_command must contain a '{user_name}' placeholder")

    # Sanitize the user input to prevent command injection
    safe_user = shlex.quote(user_name)

    # Construct the final command
    cmd = base_command.format(user_name=safe_user)

    # Execute the command (implementation not shown)
    execute_command(cmd)

    return cmd