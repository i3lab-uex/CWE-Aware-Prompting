import shlex

def create_greeting_command(student_name: str, base_command: str = "echo 'Hello, {student_name}!'" ) -> str:
    """
    Generate a shell command that greets the user by name.

    Parameters
    ----------
    student_name : str
        The user's name to be embedded in the command.
    base_command : str, optional
        A template string containing a '{student_name}' placeholder. Defaults to
        "echo 'Hello, {student_name}!'" which is safe for basic use.

    Returns
    -------
    str
        The final shell command with the student's name safely inserted.

    Notes
    -----
    This function uses :func:`shlex.quote` to escape the provided name, preventing
    command injection or other shell-related attacks. The placeholder must be a
    literal string '{student_name}'.  If the template does not contain this
    placeholder, a :class:`ValueError` is raised.
    """
    if "{student_name}" not in base_command:
        raise ValueError("base_command must contain the placeholder '{student_name}'")

    # Escape the user supplied name to avoid shell injection
    safe_name = shlex.quote(student_name)

    # Perform the substitution
    command = base_command.format(student_name=safe_name)
    return command