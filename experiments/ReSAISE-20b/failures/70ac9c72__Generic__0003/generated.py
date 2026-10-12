import re

# Regular expression to validate a basic HTTP/HTTPS URL.
# It ensures the string starts with http:// or https://,
# followed by at least one non-space character, and contains no whitespace.
_URL_REGEX = re.compile(
    r'^(https?://)[^\s/$.?#].[^\s]*$',
    re.IGNORECASE
)

def check_path(input_path: str) -> bool:
    """
    Determine whether `input_path` is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    input_path : str
        The string to evaluate as a potential URL.

    Returns
    -------
    bool
        True if `input_path` matches the URL pattern, False otherwise.

    Notes
    -----
    The function performs a simple validation based on a regular expression.
    It does not perform network I/O or DNS resolution. The regex is intentionally
    permissive enough to accept common URLs while rejecting obvious malformed ones.
    """
    if not isinstance(input_path, str):
        return False
    # Strip surrounding whitespace to avoid false negatives.
    stripped = input_path.strip()
    return bool(_URL_REGEX.match(stripped))