import shlex

def create_greeting_command(username: str, base_command: str) -> str:
    """
    Prepare a shell command that greets the user by inserting their name into
    the provided command template.

    Parameters:
        username (str): The user-provided name to include in the command.
        base_command (str): A string containing a single placeholder
                            '{username}' that will be replaced with the
                            sanitized username.

    Returns:
        str: The final shell command string ready for execution.

    Notes:
        - The username is escaped using shlex.quote to prevent command
          injection vulnerabilities.
        - If the placeholder '{username}' is missing from base_command,
          a ValueError is raised.
    """
    if "{username}" not in base_command:
        raise ValueError("The command template must contain a '{username}' placeholder.")

    # Safely escape the user input
    safe_username = shlex.quote(username)

    # Replace placeholder with escaped username
    command = base_command.replace("{username}", safe_username)
    return command