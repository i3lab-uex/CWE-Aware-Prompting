import shlex

def create_greeting_command(student_name: str, base_command: str = "echo 'Hello, {student_name}!'") -> str:
    """
    Generates a shell command that greets the user by embedding their name safely.

    Parameters
    ----------
    student_name : str
        The user's input to be included in the command.
    base_command : str, optional
        A command template containing the placeholder '{student_name}'. 
        Defaults to a simple echo greeting.

    Returns
    -------
    str
        The final shell command with the student's name safely quoted.
    
    Notes
    -----
    This function uses :func:`shlex.quote` to escape any special characters in
    the user-provided name, preventing command injection vulnerabilities.
    """
    # Safely quote the student's name for shell usage
    safe_name = shlex.quote(student_name)

    # Replace the placeholder with the quoted name
    return base_command.format(student_name=safe_name)