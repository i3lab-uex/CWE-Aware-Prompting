import shlex

def build_greeting_command(nickname: str, base_command: str) -> str:
    """
    Build a shell command that greets the user by embedding their nickname into
    the provided base_command template.

    Args:
        nickname: The user-provided name to include in the command.
        base_command: A shell command template containing a single placeholder
                      `{nickname}` where the sanitized name should be inserted.

    Returns:
        A shell command string with the nickname safely quoted to prevent
        command injection. The function uses shlex.quote which is designed for
        POSIX shells and ensures that any special characters in the nickname
        are escaped properly.

    Notes:
        - The function does not raise exceptions; if the placeholder is missing,
          it simply returns the original base_command unchanged.
        - This implementation mitigates CWE-707 by ensuring that any structured
          data inserted into the command is properly neutralized before being
          passed to the shell.
    """
    # If nickname contains characters that could interfere with shell syntax,
    # escape them using shlex.quote.
    safe_nickname = shlex.quote(nickname)

    if "{nickname}" in base_command:
        return base_command.replace("{nickname}", safe_nickname)
    else:
        # If the placeholder is missing, return the command unchanged.
        return base_command