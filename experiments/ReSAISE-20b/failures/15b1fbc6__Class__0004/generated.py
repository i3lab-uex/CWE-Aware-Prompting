import re
from urllib.parse import urlparse, ParseResult

# List of domains that are allowed for redirection
APPROVED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "myapp.example.net"
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def handle_user_redirect(user_url: str) -> str:
    """
    Safely validate a user-provided URL and return it for redirection.

    Parameters
    ----------
    user_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        The sanitized, fully‑qualified URL ready for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unapproved scheme, or its domain is not in
        :data:`APPROVED_DOMAINS`.
    """
    # Strip leading/trailing whitespace to avoid subtle injection
    user_url = user_url.strip()

    # Reject empty input early
    if not user_url:
        raise ValueError("URL must not be empty")

    # Parse the URL
    parsed = urlparse(user_url)

    # Ensure we have a scheme and netloc (i.e., absolute URL)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and include a scheme")

    # Verify the scheme is allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Scheme '{parsed.scheme}' is not allowed")

    # Normalise the netloc: lower‑case and strip any default port
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Remove common port suffixes for comparison
    if parsed.port:
        netloc = f"{hostname}:{parsed.port}"
    else:
        netloc = hostname

    # Check that the domain is in the approved list
    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved for redirection")

    # Re‑construct the URL to avoid any hidden characters or malicious fragments
    safe_url = ParseResult(
        scheme=parsed.scheme.lower(),
        netloc=netloc,
        path=parsed.path or "",
        params=parsed.params or "",
        query=parsed.query or "",
        fragment=""  # Disallow fragments to prevent client‑side redirects
    ).geturl()

    return safe_url