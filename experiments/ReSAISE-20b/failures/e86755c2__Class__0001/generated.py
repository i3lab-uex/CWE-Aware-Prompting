import re

# Compile a simple, non‑capturing regex for http/https URLs.
# It matches:
#   - scheme: "http" or "https"
#   - "://"
#   - at least one non‑space character (to allow domain, path, query, etc.)
# The pattern is deliberately simple to avoid catastrophic backtracking.
_URL_RE = re.compile(r"^(https?://\S+)$", re.IGNORECASE)


def verify_link(link: str) -> bool:
    """
    Determine whether the given string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    link : str
        The string to evaluate as a potential URL.

    Returns
    -------
    bool
        True if the input matches an HTTP/HTTPS URL pattern, False otherwise.
    """
    # Guard against non‑string input; return False without raising an exception.
    if not isinstance(link, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_URL_RE.fullmatch(link))