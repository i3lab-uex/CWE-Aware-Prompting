import re

# Regular expression that matches a simple HTTP/HTTPS URL.
# It allows any non‑whitespace characters after the scheme and
# requires at least one character in the host part.
_HTTP_URL_RE = re.compile(r"^https?://[^\s]+$", re.IGNORECASE)

def is_valid_path(site_path: str) -> bool:
    """
    Determine whether a given string is a valid HTTP or HTTPS path.

    Parameters
    ----------
    site_path : str
        The string to be evaluated as a potential valid path.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS URL pattern,
        otherwise False.

    Notes
    -----
    - No exceptions are raised; the function returns False on any error.
    - The regex is intentionally permissive to avoid rejecting
      legitimate URLs that may contain unusual characters,
      but it still ensures the string starts with http:// or https://
      and contains at least one character after that.
    """
    if not isinstance(site_path, str):
        # Non‑string input cannot be a valid path.
        return False
    # Using fullmatch ensures the entire string must match the pattern.
    return bool(_HTTP_URL_RE.fullmatch(site_path))