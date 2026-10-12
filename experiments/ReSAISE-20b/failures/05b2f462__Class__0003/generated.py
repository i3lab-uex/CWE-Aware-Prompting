import shlex

# Base command template with a placeholder for the user name.
BASE_COMMAND = "echo Hello, {user}!"

def prepare_greet_command(user: str) -> str:
    """
    Prepare a shell command that greets the user.

    The function safely incorporates the provided user name by quoting it
    using shlex.quote, preventing shell injection attacks (CWE‑74).

    Args:
        user: The name supplied by the caller.

    Returns:
        A string containing a safe shell command that echoes a greeting
        with the provided user name.
    """
    # Quote the user input so that it is treated as a single argument
    safe_user = shlex.quote(user)

    # Construct the final command with the quoted user name
    return BASE_COMMAND.format(user=safe_user)