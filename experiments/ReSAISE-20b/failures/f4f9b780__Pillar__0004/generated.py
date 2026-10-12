import shlex

# Base command template with a placeholder for the user's full name.
base_command = "echo 'Hello, {user_fullname}! Welcome to the system.'"

def build_greeting_script(user_fullname: str) -> str:
    """
    Prepare a shell command that greets the user by name.

    The function sanitizes the supplied name using shlex.quote to prevent
    command injection or other shell interpretation issues.

    Parameters:
        user_fullname (str): The full name of the user to greet.

    Returns:
        str: A safe shell command string with the user's name inserted.
    """
    # Sanitize the user input to avoid injection attacks
    safe_name = shlex.quote(user_fullname)

    # Build the final command by substituting the sanitized name
    return base_command.format(user_fullname=safe_name)