import shlex

def compose_hello_command(recipient: str, base_command: str = "echo 'Hello, {recipient}!'") -> str:
    """
    Construct a shell command that greets the user by name.

    Parameters
    ----------
    recipient : str
        The name provided by the user.
    base_command : str, optional
        Template command containing a '{recipient}' placeholder.

    Returns
    -------
    str
        A shell command with the recipient safely inserted.
    """
    # Validate that the placeholder exists in the base_command
    if "{recipient}" not in base_command:
        raise ValueError("Base command must contain a '{recipient}' placeholder.")

    # Escape the recipient string to prevent shell injection
    safe_recipient = shlex.quote(recipient)

    # Perform the substitution safely
    return base_command.format(recipient=safe_recipient)