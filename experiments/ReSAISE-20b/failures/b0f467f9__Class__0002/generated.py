import shlex

def create_greeting_command(student_name: str, base_command: str) -> str:
    """
    Generate a shell command that greets the user by embedding their name into
    `base_command`. The user's input is safely escaped using shlex.quote to
    prevent shell injection (CWE‑74).

    Parameters:
        student_name: The name supplied by the user.
        base_command: A command template containing the placeholder
                      '{student_name}'.

    Returns:
        A fully-formed shell command string with the user's name safely quoted.
    """
    # Escape the user-provided name to ensure it is treated as a single argument
    safe_name = shlex.quote(student_name)

    # Substitute the placeholder with the escaped name
    command = base_command.replace("{student_name}", safe_name)

    return command