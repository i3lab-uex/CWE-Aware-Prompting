import shlex

def create_greeting_command(student_name: str) -> str:
    """
    Generate a shell command that greets the user safely.

    Parameters
    ----------
    student_name : str
        The name provided by the user. It will be quoted to prevent shell injection.

    Returns
    -------
    str
        A fully constructed shell command that includes the sanitized user name.
    """
    # Define a base command template with a placeholder for the student's name
    base_command = "echo 'Hello, {student_name}!'"

    # Quote the user input to escape any special characters
    safe_name = shlex.quote(student_name)

    # Substitute the placeholder with the sanitized input
    final_command = base_command.format(student_name=safe_name)

    return final_command