import re

# Compile the regular expression once for efficiency.
# The pattern matches a string that starts with "http://" or "https://"
# followed by at least one non‑whitespace character.
_HTTP_PATH_RE = re.compile(r'^https?://\S+$', re.IGNORECASE)


def is_valid_path(site_path: str) -> bool:
    """
    Determine whether the supplied string represents a valid HTTP or HTTPS URL path.

    The function uses a simple regular expression to validate that the string
    begins with "http://" or "https://", followed by at least one non‑whitespace
    character.  It is intentionally conservative to avoid excessive backtracking,
    thereby mitigating potential denial‑of‑service (CWE‑407) attacks.

    Parameters
    ----------
    site_path : str
        The string to be evaluated as a potential valid path.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS URL pattern, False otherwise.
    """
    # Avoid raising exceptions for malformed input; simply return False if
    # the argument is not a string or does not match the pattern.
    try:
        return bool(_HTTP_PATH_RE.fullmatch(site_path))
    except Exception:  # pragma: no cover
        return False