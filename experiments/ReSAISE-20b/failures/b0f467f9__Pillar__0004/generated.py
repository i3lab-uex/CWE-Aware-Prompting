import shlex

def create_greeting_command(student_name: str, base_command: str) -> str:
    """
    Safely embed the user's name into a shell command template.

    Parameters
    ----------
    student_name : str
        The user supplied name to be inserted into the command.
    base_command : str
        A shell command template containing the placeholder '{student_name}'.

    Returns
    -------
    str
        The final shell command with the name safely quoted to prevent
        command injection.
    """
    # Quote the user input so it is treated as a single literal argument
    safe_name = shlex.quote(student_name)

    # Use the placeholder in the template; no additional interpolation
    return base_command.format(student_name=safe_name)