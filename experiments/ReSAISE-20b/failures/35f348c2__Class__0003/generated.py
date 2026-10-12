import re

# Compile a safe, efficient regex that matches HTTP/HTTPS URLs.
# The pattern is anchored to the start and end of the string,
# avoiding catastrophic backtracking by using non-greedy, simple
# character classes and explicit quantifiers.
_URL_RE = re.compile(
    r"""^https?://          # http:// or https://
        (?:(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})  # domain (e.g., example.com)
        (?::\d{1,5})?       # optional port (0-65535)
        (?:/[^?#]*)?        # optional path, no query or fragment
        $""",
    re.VERBOSE | re.IGNORECASE,
)

def validate_path(path: str) -> bool:
    """
    Validate that a given string is a well‑formed HTTP or HTTPS URL.

    Parameters
    ----------
    path : str
        The input string to validate.

    Returns
    -------
    bool
        True if the string matches a valid HTTP/HTTPS URL, False otherwise.
    """
    # Return False for non-string input early to avoid regex overhead
    if not isinstance(path, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern
    return bool(_URL_RE.fullmatch(path))