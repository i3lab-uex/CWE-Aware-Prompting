import shlex

def create_greeting_command(student_name: str, base_command: str = "echo 'Hello, {student_name}!'") -> str:
    """
    Generate a shell command that greets the user by name.

    Parameters
    ----------
    student_name : str
        The name provided by the user.
    base_command : str, optional
        A command template containing a '{student_name}' placeholder. The default
        is a simple echo statement.

    Returns
    -------
    str
        A shell command string with the user’s name safely quoted to prevent
        command injection.
    """
    # Sanitize the user input by quoting it for shell usage
    safe_name = shlex.quote(student_name)

    # Replace the placeholder with the sanitized name
    command = base_command.format(student_name=safe_name)

    return command