import shlex

def create_greeting_command(student_name: str, base_command: str = "echo 'Hello, {student_name}!'\n") -> str:
    """
    Generates a shell command that greets the user by name.

    Parameters
    ----------
    student_name : str
        The name supplied by the user.  It will be sanitized to avoid shell
        injection attacks.
    base_command : str, optional
        A command template that contains a single placeholder `{student_name}`.
        The default greets the user with `echo`.

    Returns
    -------
    str
        A shell command string where the placeholder has been replaced with a
        safely quoted version of `student_name`.

    Notes
    -----
    The function uses :func:`shlex.quote` to escape the name so that any
    special characters (e.g. semicolons, backticks, quotes) are treated as
    literal data rather than shell syntax.  This mitigates CWE‑74.
    """
    # Ensure the placeholder exists
    if "{student_name}" not in base_command:
        raise ValueError("base_command must contain the placeholder '{student_name}'")

    # Safely quote the user supplied name
    safe_name = shlex.quote(student_name)

    # Replace the placeholder with the quoted value
    command = base_command.format(student_name=safe_name)
    return command