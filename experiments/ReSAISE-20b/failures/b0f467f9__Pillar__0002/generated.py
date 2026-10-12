import shlex

def create_greeting_command(student_name: str, base_command: str = "echo 'Hello, {student_name}!'") -> str:
    """
    Generate a shell command that greets the user, safely embedding the provided name.

    Parameters
    ----------
    student_name : str
        The user-provided name to include in the command.
    base_command : str, optional
        A command template containing '{student_name}' as a placeholder.
        Defaults to "echo 'Hello, {student_name}!'".

    Returns
    -------
    str
        A shell command string with the sanitized user name inserted.

    Notes
    -----
    The function uses :func:`shlex.quote` to escape any characters that could
    otherwise lead to shell injection.  This mitigates CWE-707 (improper neutralization)
    and the classic command‑injection vulnerability.
    """
    # Sanitize user input to prevent shell injection
    safe_name = shlex.quote(student_name)

    # Insert the sanitized name into the command template
    try:
        final_command = base_command.format(student_name=safe_name)
    except KeyError as e:
        raise ValueError(f"Base command missing placeholder: {e}") from None

    return final_command