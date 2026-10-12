import re

# Compile a simple, non‑backtracking regex for http/https URLs.
# It matches the scheme (http or https), followed by "://",
# and then any non‑whitespace characters until the end of string.
_HTTP_URL_RE = re.compile(r"^https?://[^\s]+$", re.IGNORECASE)


def validate_path(path: str) -> bool:
    """
    Validate whether a string is a syntactically valid HTTP or HTTPS URL.

    Parameters
    ----------
    path : str
        The string to validate.

    Returns
    -------
    bool
        True if `path` starts with "http://" or "https://"
        and contains no whitespace characters; False otherwise.
    """
    if not isinstance(path, str):
        # Non‑string input cannot be a valid URL.
        return False

    # Use fullmatch to ensure the entire string matches the pattern.
    return _HTTP_URL_RE.fullmatch(path) is not None