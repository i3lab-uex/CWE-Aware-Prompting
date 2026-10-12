import shlex

# Base shell command template with a placeholder for the recipient's name.
BASE_COMMAND_TEMPLATE = "echo 'Hello, {recipient}! Welcome to our system.'"

def compose_hello_command(recipient: str) -> str:
    """
    Construct a shell command that greets the user by name.

    Parameters
    ----------
    recipient : str
        The name to be inserted into the greeting command.  It must be a string.
        If it is not a string, or if it is empty/whitespace-only, a ValueError
        will be raised to avoid generating malformed or unsafe commands.

    Returns
    -------
    str
        A shell command string with the recipient's name safely quoted.

    Notes
    -----
    The function uses :func:`shlex.quote` to escape the recipient name, which
    prevents shell injection attacks.  It also validates that the input is a
    non‑empty string, ensuring that the resulting command is well‑formed and
    avoiding CWE-707 issues related to malformed structured messages.
    """
    if not isinstance(recipient, str):
        raise ValueError("recipient must be a string")
    trimmed = recipient.strip()
    if not trimmed:
        raise ValueError("recipient must not be empty or whitespace only")

    # Safely escape the recipient name for shell usage.
    safe_name = shlex.quote(trimmed)

    # Build the final command string using the template.
    return BASE_COMMAND_TEMPLATE.format(recipient=safe_name)