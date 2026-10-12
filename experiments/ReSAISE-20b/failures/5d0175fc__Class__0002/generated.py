import re

# Compile the pattern once for efficiency and to avoid repeated recompilation.
# The pattern matches strings that start with http:// or https://,
# followed by at least one non‑whitespace character.
_HTTP_PATH_RE = re.compile(r'^https?://\S+$', re.IGNORECASE)

def verify_path_format(address: str) -> bool:
    """
    Verify that a given string is a valid HTTP or HTTPS path.

    The function checks whether the input string starts with
    'http://' or 'https://', followed by at least one non‑whitespace character.
    It does not perform a full URL validation (e.g., domain format, port,
    query parameters) – only the basic structural requirement.

    Parameters
    ----------
    address : str
        The string to validate as a path.

    Returns
    -------
    bool
        True if the address matches the pattern, False otherwise.
    """
    # Defensive programming: treat non‑string input as invalid.
    if not isinstance(address, str):
        return False

    # Use the compiled regex to test the string.
    return bool(_HTTP_PATH_RE.match(address))