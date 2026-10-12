import shlex

# Predefined shell command template with a placeholder for the user's name.
BASE_COMMAND = "echo 'Hello, {name_of_user}!'"  # Example template


def assemble_greet_command(name_of_user: str) -> str:
    """
    Construct a shell command that greets the user by name.

    The user's name is safely escaped using shlex.quote to prevent shell injection.
    The resulting command uses the predefined BASE_COMMAND template.

    Args:
        name_of_user: The user's name to insert into the command.

    Returns:
        A string containing the complete shell command with the user's name safely
        embedded.
    """
    # Escape the user input to avoid shell injection vulnerabilities
    safe_name = shlex.quote(name_of_user)

    # Substitute the escaped name into the command template
    return BASE_COMMAND.format(name_of_user=safe_name)