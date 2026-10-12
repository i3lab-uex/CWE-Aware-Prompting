import shlex

# Base command template with a placeholder for the user name.
BASE_COMMAND = "echo 'Hello, {user}!'"


def prepare_greet_command(user: str) -> str:
    """
    Prepare a shell command that greets the user.

    The function safely inserts the provided `user` string into
    a predefined command template by quoting it with shlex.quote.
    This prevents shell injection attacks.

    Args:
        user: The user's name to be included in the command.

    Returns:
        A string containing the final shell command ready for execution.
    """
    # Quote the user input to escape any special characters
    safe_user = shlex.quote(user)

    # Replace the placeholder in the base command with the quoted user
    return BASE_COMMAND.format(user=safe_user)