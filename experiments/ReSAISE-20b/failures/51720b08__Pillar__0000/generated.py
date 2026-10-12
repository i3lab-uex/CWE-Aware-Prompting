import shlex

def compose_hello_command(recipient: str, base_command: str = "echo 'Hello, {recipient}!'" ) -> str:
    """
    Construct a shell command that greets the specified recipient.

    The function safely escapes the recipient string to prevent shell injection
    and then substitutes it into a predefined command template.

    Parameters
    ----------
    recipient : str
        The name supplied by the user.
    base_command : str, optional
        A shell command template containing a single placeholder `{recipient}`.
        The default template simply echoes a greeting.

    Returns
    -------
    str
        A shell command string with the recipient name safely inserted.
    """
    # Ensure the placeholder exists in the template
    if "{recipient}" not in base_command:
        raise ValueError("The base_command must contain the placeholder '{recipient}'")

    # Safely escape the recipient to avoid shell injection
    safe_recipient = shlex.quote(recipient)

    # Perform the substitution
    command = base_command.format(recipient=safe_recipient)
    return command