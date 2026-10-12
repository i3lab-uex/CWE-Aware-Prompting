import shlex

def create_greeting_command(student_name: str, base_command: str) -> str:
    """
    Generate a shell command that greets the user by embedding their name
    into the provided base_command template.

    Parameters:
        student_name (str): The user-provided name to include in the command.
        base_command (str): A template string containing '{student_name}' as
                            a placeholder for the sanitized name.

    Returns:
        str: The final shell command with the user’s input safely quoted.
    """
    # Quote the user input to avoid shell injection
    safe_name = shlex.quote(student_name)

    # Replace the placeholder with the safely quoted name
    return base_command.format(student_name=safe_name)