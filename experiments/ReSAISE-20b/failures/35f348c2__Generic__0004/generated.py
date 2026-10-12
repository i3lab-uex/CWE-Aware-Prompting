import re

# Regular expression that matches a simple HTTP or HTTPS URL.
# It checks for:
#   * scheme: http or https (case‑insensitive)
#   * authority: at least one non-whitespace character after '://'
#   * optional path/query/fragment (anything except whitespace)
_URL_RE = re.compile(
    r'^(https?://[^\s/$.?#].[^\s]*)$',
    re.IGNORECASE
)

def validate_path(path: str) -> bool:
    """
    Validate that the given string is a well‑formed HTTP or HTTPS URL.

    Parameters
    ----------
    path : str
        The string to validate.

    Returns
    -------
    bool
        ``True`` if *path* is a valid HTTP/HTTPS URL, otherwise ``False``.

    Notes
    -----
    The function is intentionally permissive about the host and path portions,
    only ensuring that they contain non‑whitespace characters.  This keeps the
    implementation simple while still rejecting obvious malformed inputs.
    """
    if not isinstance(path, str):
        return False
    return bool(_URL_RE.match(path))