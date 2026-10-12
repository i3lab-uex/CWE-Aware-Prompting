#!/usr/bin/env python3
"""
Utility to safely construct a shell command that greets a user.
The function uses shlex.quote to neutralise any shell metacharacters
present in the supplied username, mitigating command‑injection risks.

CWE-707: The implementation ensures that the constructed message
(is the final command string) is well‑formed and does not expose
unexpected behaviour to downstream components.
"""

import shlex

# Base command template – the placeholder `{username}` will be replaced
BASE_COMMAND = "echo 'Hello, {username}! Welcome to the system.'"

def create_greeting_command(username: str) -> str:
    """
    Prepare a shell command that greets the specified user.

    Parameters
    ----------
    username : str
        The name of the user to include in the greeting.  It may contain
        arbitrary characters; they will be safely escaped.

    Returns
    -------
    str
        A shell command string ready for execution.  The username is
        quoted using shlex.quote to prevent injection of shell syntax.
    """
    # Sanitize the user input so that it cannot break out of the quoted
    # context in the final command.
    safe_username = shlex.quote(username)

    # Substitute the placeholder with the sanitized value
    command = BASE_COMMAND.format(username=safe_username)

    return command

# Example usage (for demonstration only – not part of the library API)
if __name__ == "__main__":
    # Simulate user input that could be malicious
    raw_user = "Alice; rm -rf /"
    cmd = create_greeting_command(raw_user)
    print(f"Constructed command: {cmd}")