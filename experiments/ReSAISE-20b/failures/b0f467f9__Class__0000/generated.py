import shlex

def create_greeting_command(student_name: str, base_command: str) -> str:
    """
    Create a shell command that greets the user, safely embedding their name.

    Parameters
    ----------
    student_name : str
        The raw user supplied name.
    base_command : str
        A command template containing the placeholder '{student_name}'.

    Returns
    -------
    str
        The final shell command with the user name safely quoted.
    """
    # Use shlex.quote to escape any characters that might be interpreted by the shell
    safe_name = shlex.quote(student_name)

    # Substitute the placeholder with the safely quoted name
    return base_command.format(student_name=safe_name)