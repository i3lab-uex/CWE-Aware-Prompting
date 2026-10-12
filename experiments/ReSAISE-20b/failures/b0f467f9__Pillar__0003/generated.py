import shlex

def create_greeting_command(student_name: str, base_command: str = "echo Hello, {student_name}") -> str:
    """
    Generate a shell command that greets the user by name, ensuring that
    the supplied name is safely quoted to avoid command injection.

    Parameters:
        student_name (str): The user-provided name to embed in the command.
        base_command (str): A template containing a '{student_name}' placeholder.

    Returns:
        str: The final shell command with the name safely quoted.
    """
    # Sanitize the user input by quoting it for safe shell usage
    safe_name = shlex.quote(student_name)

    # Replace the placeholder with the sanitized name
    return base_command.format(student_name=safe_name)