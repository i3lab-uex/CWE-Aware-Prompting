# validate_and_execute_command.py

from typing import Optional, List


def validate_and_execute_command(cmd: str,
                                 allowed_commands: List[str]) -> Optional[str]:
    """
    Validate a user-provided command against an allowed list and return it if valid.

    Parameters
    ----------
    cmd : str
        The command string provided by the user.
    allowed_commands : List[str]
        A list of commands that are permitted to be executed.

    Returns
    -------
    Optional[str]
        The original command if it is present in `allowed_commands`; otherwise None.

    Notes
    -----
    - The function performs a strict equality check; no substring or pattern matching is allowed.
    - No external execution occurs in this function – it only validates the command.
    """
    # Normalise input to avoid trivial whitespace differences
    cmd_clean = cmd.strip()

    # Check against the allowed list (case-sensitive)
    if cmd_clean in allowed_commands:
        return cmd_clean
    return None


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    ALLOWED_COMMANDS = [
        "ls -la",
        "pwd",
        "whoami",
    ]

    user_cmd = input("Enter command: ")
    validated = validate_and_execute_command(user_cmd, ALLOWED_COMMANDS)

    if validated is None:
        print("Command not allowed.")
    else:
        print(f"Validated command: {validated}")