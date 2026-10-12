import shlex

# A template for the shell command that greets a user.
# The placeholder `{user_name}` will be replaced by the sanitized input.
BASE_COMMAND = "echo 'Hello, {user_name}! Welcome!'"

def generate_greeting_command(user_name: str) -> str:
    """
    Generate a shell command that greets the specified user.

    Args:
        user_name (str): The user-provided name to embed in the command.

    Returns:
        str: A shell command string that, when executed, prints a greeting
             message for the user.

    Note:
        The function uses `shlex.quote` to safely escape the user name,
        preventing command injection attacks. The resulting command
        should be passed to an external executor (e.g., `execute_command`).
    """
    # Sanitize the user-provided name to avoid shell injection.
    safe_name = shlex.quote(user_name)

    # Format the base command with the sanitized name.
    command = BASE_COMMAND.format(user_name=safe_name)

    return command