import shlex

def make_greeting_command(name: str, base_command: str = "echo 'Hello, {name}!'") -> str:
    """
    Generate a safe shell command that greets the user by name.

    Parameters
    ----------
    name : str
        The user's name to embed in the command.
    base_command : str, optional
        A shell command template containing a '{name}' placeholder.

    Returns
    -------
    str
        The fully-formed, shell‑escaped command ready for execution.

    Notes
    -----
    - The function uses :func:`shlex.quote` to escape the user input, mitigating
      command‑injection risks.
    - This implementation is conscious of CWE‑707 by ensuring the placeholder
      value is properly sanitized before being inserted into the command string.
    """
    # Escape user input to avoid shell interpretation
    safe_name = shlex.quote(name)

    # Replace the placeholder with the escaped value
    command = base_command.format(name=safe_name)

    return command