import shlex

def prepare_greet_command(user: str) -> str:
    """
    Prepare a shell command that greets the user by name.

    The function uses `shlex.quote` to safely escape any shell metacharacters
    that might be present in the user input, preventing command injection.

    Parameters:
        user (str): The name of the user to greet.

    Returns:
        str: A shell command string that greets the user safely.
    """
    # Define the base command template
    base_command = "echo 'Hello, {user}!'"

    # Safely escape the user input
    safe_user = shlex.quote(user)

    # Replace the placeholder with the escaped value
    final_command = base_command.format(user=safe_user)

    return final_command