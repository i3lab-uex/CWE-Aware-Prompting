import re

# Compile a simple, efficient regex that matches typical HTTP/HTTPS URLs.
# The pattern is deliberately straightforward to avoid catastrophic backtracking
# and keep the computational complexity linear in input length.
_URL_RE = re.compile(r'^(https?://[^\s]+)$', re.IGNORECASE)


def check_path(input_path: str) -> bool:
    """
    Determine whether the provided string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    input_path : str
        The string to evaluate as a potential URL.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS URL pattern, False otherwise.
    """
    # Guard against None or non-string inputs; return False instead of raising.
    if not isinstance(input_path, str):
        return False

    # The regex is anchored at start and end to ensure the entire string matches.
    return bool(_URL_RE.match(input_path))