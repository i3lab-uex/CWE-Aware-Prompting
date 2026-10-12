import re

# Compile a simple, non‑backtracking regex that matches HTTP/HTTPS URLs.
# The pattern allows any non-whitespace characters after the scheme and
# host, which is sufficient for a basic path validation.  It avoids
# complex nested patterns that could lead to exponential backtracking.
_HTTP_URL_RE = re.compile(r'^(https?)://[^\s]+$', re.IGNORECASE)

def validate_path(path: str) -> bool:
    """
    Validate whether the given string is a well‑formed HTTP or HTTPS URL.

    Parameters
    ----------
    path : str
        The input string to validate.

    Returns
    -------
    bool
        True if the string matches the pattern, False otherwise.
    """
    # Guard against non‑string input without raising an exception
    if not isinstance(path, str):
        return False

    # Use the compiled regex for efficient matching
    return bool(_HTTP_URL_RE.match(path))