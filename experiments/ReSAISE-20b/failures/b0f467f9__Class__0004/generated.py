import shlex

def create_greeting_command(student_name: str, base_command: str) -> str:
    """
    Generate a shell command that greets the user by embedding their name
    safely into the provided base_command template.

    Parameters:
        student_name (str): The name to embed in the command.
        base_command (str): A command template containing '{student_name}' as a placeholder.

    Returns:
        str: The final shell command with the user’s name safely quoted.
    """
    # Quote the input to prevent shell injection
    safe_name = shlex.quote(student_name)

    # Replace placeholder with the quoted name
    return base_command.format(student_name=safe_name)