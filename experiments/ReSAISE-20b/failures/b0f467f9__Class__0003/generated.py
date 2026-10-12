import shlex

def create_greeting_command(student_name: str, base_command: str) -> str:
    """
    Generate a shell command that greets the user, safely embedding their name.

    Parameters
    ----------
    student_name : str
        The user's name to embed in the command.
    base_command : str
        A command template containing a single placeholder `{student_name}`.

    Returns
    -------
    str
        The final shell command with the name safely quoted to avoid injection.
    """
    # Sanitize user input for shell usage
    safe_name = shlex.quote(student_name)

    try:
        command = base_command.format(student_name=safe_name)
    except KeyError as exc:
        raise ValueError(
            f"Base command missing placeholder '{{student_name}}': {base_command}"
        ) from exc

    return command