import re

# Pre‑compiled regular expression for a simple HTTP/HTTPS URL.
# The pattern matches:
#   - scheme: http or https (case‑insensitive)
#   - ://
#   - any non‑whitespace characters for the rest of the URL
_URL_RE = re.compile(r"^(https?://)[^\s]+$", re.IGNORECASE)


def path_check(u: str) -> bool:
    """
    Check whether the supplied string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    u : str
        The string to validate as a path/URL.

    Returns
    -------
    bool
        True if `u` matches the expected HTTP/HTTPS format, False otherwise.
    """
    # Ensure the input is a string; if not, return False without raising.
    try:
        if not isinstance(u, str):
            return False
    except Exception:  # pragma: no cover
        return False

    # Perform a full match against the pre‑compiled regex.
    return bool(_URL_RE.fullmatch(u))