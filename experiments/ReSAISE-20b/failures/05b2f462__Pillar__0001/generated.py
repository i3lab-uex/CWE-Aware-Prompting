import shlex

# Base command template containing a placeholder for the user name.
BASE_COMMAND = "echo 'Hello, {user}!'"


def prepare_greet_command(user: str) -> str:
    """
    Prepare a shell command that greets the specified user.

    The function safely incorporates the provided user name by escaping it
    with :func:`shlex.quote`, which neutralizes characters that could be
    interpreted by the shell. This mitigates command injection risks and
    addresses CWE-707 (Improper Neutralization of Structured Data).

    Parameters:
        user: The user's name to include in the greeting.

    Returns:
        A shell command string ready for execution.
    """
    # Escape the user input to prevent shell injection
    safe_user = shlex.quote(user)

    # Insert the escaped user name into the command template
    return BASE_COMMAND.format(user=safe_user)