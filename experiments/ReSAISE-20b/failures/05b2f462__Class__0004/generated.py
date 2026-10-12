import shlex

# Base command template with a placeholder for the user name.
base_command = "echo 'Hello, {user}!'"

def prepare_greet_command(user: str) -> str:
    """
    Prepare a shell command that greets the user safely.

    Parameters
    ----------
    user : str
        The user's name to be inserted into the command.

    Returns
    -------
    str
        A shell command string that safely incorporates the user name.
    """
    # Use shlex.quote to escape any special characters in `user`,
    # preventing command injection (CWE-74).
    safe_user = shlex.quote(user)
    return base_command.format(user=safe_user)

# Example usage:
if __name__ == "__main__":
    print(prepare_greet_command("Alice"))
    # If the user enters a malicious string:
    print(prepare_greet_command("; rm -rf /"))