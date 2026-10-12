import shlex

# Predefined shell command template
BASE_COMMAND = "echo 'Hello, {recipient}! Welcome to the system.'"

def compose_hello_command(recipient: str) -> str:
    """
    Construct a shell command that greets the user by name.

    Parameters
    ----------
    recipient : str
        The name provided by the user.  It is escaped to avoid shell injection.

    Returns
    -------
    str
        A fully quoted shell command that safely includes the user name.
    """
    # Sanitize the recipient by quoting it for shell usage
    safe_recipient = shlex.quote(recipient)

    # Replace the placeholder with the quoted recipient
    command = BASE_COMMAND.format(recipient=safe_recipient)

    return command