import re
from urllib.parse import urlparse, urlunparse

# Approved domains – modify as needed
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe.example.net",
}

# Regex to reject non‑ASCII URLs (to avoid homoglyph attacks)
URL_SAFE_RE = re.compile(r"^[A-Za-z0-9\-._~:/?#[\]@!$&'()*+,;=%]+$")


def redirect_user_safely(target_url: str) -> str:
    """
    Validate a user‑supplied URL and return it if it points to an approved domain.
    Raises ValueError otherwise.

    Parameters
    ----------
    target_url : str
        The URL provided by the user.

    Returns
    -------
    str
        The validated and normalized URL safe for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        contains disallowed characters, or its domain is not approved.
    """
    if not isinstance(target_url, str):
        raise ValueError("URL must be a string")

    # Basic sanity check for disallowed characters
    if not URL_SAFE_RE.match(target_url):
        raise ValueError("URL contains disallowed characters")

    parsed = urlparse(target_url)

    # Enforce HTTP/HTTPS only
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract hostname; urlparse returns host in netloc, possibly with port
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Normalize to lowercase for comparison
    if hostname.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved for redirection")

    # Rebuild the URL to ensure it has no extraneous components
    safe_url = urlunparse(parsed._replace(fragment=""))  # strip fragment

    return safe_url