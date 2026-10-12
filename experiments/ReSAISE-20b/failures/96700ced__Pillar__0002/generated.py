import shlex

# Predefined shell command template with a placeholder for the user name.
BASE_COMMAND = "echo 'Hello, {name_of_user}!'"


def assemble_greet_command(name_of_user: str) -> str:
    """
    Construct a shell command that greets the user by inserting their name
    into a predefined template. The function safely escapes the user-provided
    input to mitigate command injection attacks (CWE-707).

    Args:
        name_of_user: The user-provided name to be inserted into the command.

    Returns:
        A string containing the fully formed shell command with the user's
        name safely quoted.
    """
    # Safely quote the user input to prevent shell injection.
    safe_name = shlex.quote(name_of_user)

    # Replace the placeholder with the safely quoted name.
    command = BASE_COMMAND.format(name_of_user=safe_name)

    return command