import shlex

# Predefined shell command template.
# The placeholder `{recipient}` will be replaced by the user‑supplied name.
BASE_COMMAND_TEMPLATE = "echo 'Hello, {recipient}'"

def compose_hello_command(recipient: str) -> str:
    """
    Construct a shell command that greets the given recipient.
    
    Parameters
    ----------
    recipient : str
        The name provided by the user that will be inserted into the command.
    
    Returns
    -------
    str
        A shell command string with the recipient safely quoted to prevent
        injection attacks.
    
    Notes
    -----
    The function uses :func:`shlex.quote` to escape the recipient string.
    This mitigates CWE‑707 (Improper Neutralization) by ensuring that any
    shell metacharacters in the input are safely escaped before being
    interpolated into the command template.
    """
    # Safely escape user input to avoid shell injection
    safe_recipient = shlex.quote(recipient)
    
    # Replace the placeholder with the quoted recipient
    command = BASE_COMMAND_TEMPLATE.format(recipient=safe_recipient)
    
    return command