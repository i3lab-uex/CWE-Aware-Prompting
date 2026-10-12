import re

# Regular expression for a basic HTTP/HTTPS URL.
# It checks that the string starts with http:// or https://,
# followed by at least one non‑space character.
_HTTP_URL_RE = re.compile(
    r'^(?:https?://)'
    r'(?:[^\s/$.?#].[^\s]*)$',
    re.IGNORECASE
)

def check_path(string: str) -> bool:
    """
    Validate whether the given string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    string : str
        The input string to validate as a path/URL.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS URL pattern, False otherwise.

    Notes
    -----
    - The function does not raise exceptions; any error results in a False return.
    - This is a simple validation and does not check DNS resolution or scheme correctness beyond the pattern.
    """
    if not isinstance(string, str):
        return False
    # Use fullmatch to ensure the entire string conforms to the pattern.
    match = _HTTP_URL_RE.fullmatch(string.strip())
    return bool(match)