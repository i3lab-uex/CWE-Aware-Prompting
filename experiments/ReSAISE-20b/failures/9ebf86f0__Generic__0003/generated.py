import shlex

# Assume a global base command template is defined elsewhere in the module.
# Example: base_command = "echo 'Hello, {user_name}!'"
base_command: str = "echo 'Hello, {user_name}!'"


def generate_greeting_command(user_name: str) -> str:
    """
    Generate a shell command that greets the specified user.

    The function safely escapes the user-provided name to avoid shell injection.
    It returns a fully-formed command string that can be executed by an external
    executor such as `execute_command`.

    Parameters:
        user_name (str): The name supplied by the user.

    Returns:
        str: A shell command string with the sanitized user name embedded.
    """
    # Sanitize the user input to prevent shell injection
    safe_name = shlex.quote(user_name)

    # Construct the command using the template
    command = base_command.format(user_name=safe_name)

    return command