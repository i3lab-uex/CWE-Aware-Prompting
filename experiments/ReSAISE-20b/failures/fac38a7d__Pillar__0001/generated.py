# safe_command_executor.py

from typing import Optional, List

# Define the list of commands that are allowed to be executed.
ALLOWED_COMMANDS: List[str] = [
    "list",
    "show",
    "exit",
    "help",
]

# Convert to a set for O(1) lookup and avoid accidental duplicates.
_ALLOWED_SET = frozenset(ALLOWED_COMMANDS)


def _is_command_allowed(command: str) -> bool:
    """
    Perform a constant‑time comparison to check if the command is in
    ALLOWED_COMMANDS.  Using a set lookup provides O(1) performance and
    reduces the chance of timing‑based side channels.
    """
    # Normalise: strip whitespace and convert to lower case for a
    # deterministic comparison.  If you need exact case sensitivity,
    # remove the lower() call.
    normalized = command.strip().lower()
    return normalized in _ALLOWED_SET


def check_and_run_command(command_input: str) -> Optional[str]:
    """
    Validate a user‑supplied command against the list of allowed commands.

    Parameters
    ----------
    command_input : str
        The raw string entered by the user.

    Returns
    -------
    Optional[str]
        The command string if it is allowed; otherwise, None.

    Notes
    -----
    * The function does **not** execute the command.  It only validates it.
      Execution should be performed by a separate, trusted module.
    * The comparison is case‑insensitive and ignores surrounding whitespace.
      Adjust the normalisation logic if a stricter policy is required.

    Raises
    ------
    ValueError
        If ``command_input`` is not a string.
    """
    if not isinstance(command_input, str):
        raise ValueError("command_input must be a string")

    if _is_command_allowed(command_input):
        return command_input.strip()
    return None


# Example usage
if __name__ == "__main__":
    user_input = input("Enter command: ")
    cmd = check_and_run_command(user_input)
    if cmd is None:
        print("Command not allowed.")
    else:
        print(f"Executing command: {cmd}")