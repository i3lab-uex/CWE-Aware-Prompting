import shlex

def create_greeting_command(student_name: str, base_command: str) -> str:
    """
    Generate a shell command that greets the user by embedding their name
    into the provided base_command template.

    Parameters
    ----------
    student_name : str
        The name supplied by the user.
    base_command : str
        A command template containing the placeholder '{student_name}'.

    Returns
    -------
    str
        The final shell command with the user's name safely inserted.
    """
    # Safely escape the user input to avoid shell injection
    safe_name = shlex.quote(student_name)

    # Replace the placeholder with the escaped name
    return base_command.format(student_name=safe_name)