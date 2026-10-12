import shlex

def create_greeting_command(student_name: str, base_command: str) -> str:
    """
    Generate a shell command that greets the user by embedding their name
    safely into the provided command template.

    Parameters
    ----------
    student_name : str
        The name input provided by the user to be included in the command.
    base_command : str
        A command template string where '{student_name}' is a placeholder for the username.

    Returns
    -------
    str
        The final shell command with the user's name safely embedded.
    """
    # Safely quote the user-provided name to prevent command injection
    safe_name = shlex.quote(student_name)

    # Replace the placeholder with the quoted name
    return base_command.format(student_name=safe_name)