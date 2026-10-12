import re
from urllib.parse import urlparse, urlunparse

# List of domains considered safe for redirection
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.io"
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}


def redirect_user_safely(target_url: str) -> str:
    """
    Validate a user-supplied URL and return it if its domain is approved.
    
    Parameters
    ----------
    target_url : str
        The URL provided by the user.

    Returns
    -------
    str
        The sanitized, validated URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list or if the scheme is disallowed.
    """
    # Parse the URL
    parsed = urlparse(target_url)

    # Ensure scheme is present and allowed
    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed or missing URL scheme: {parsed.scheme!r}")

    # Extract hostname (lowercase for comparison)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Normalize hostname (strip trailing dot)
    hostname = hostname.rstrip(".").lower()

    # Verify the domain is in the approved list
    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved for redirection")

    # Rebuild the URL to ensure consistency (e.g., remove default ports)
    cleaned = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return cleaned