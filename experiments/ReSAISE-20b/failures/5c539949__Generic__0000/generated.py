import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered safe for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "secure.example.net"
}

# Allowed URL schemes for redirection.
ALLOWED_SCHEMES = {"http", "https"}


def _is_approved_domain(host: str) -> bool:
    """
    Check if the host is an approved domain or a sub‑domain of one.
    """
    # Remove port if present
    host = host.split(":")[0].lower()
    for domain in APPROVED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate a user supplied URL and return it if it is safe for redirection.

    Parameters
    ----------
    redirect_url : str
        The URL supplied by the user that should be redirected to.

    Returns
    -------
    str
        The validated, safe URL ready for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not part of the approved list,
        or if the scheme is disallowed, or if the URL is malformed.
    """
    # Strip whitespace and normalise percent‑encoding
    url = redirect_url.strip()

    # Parse the URL
    parsed = urlparse(url)

    # Basic checks: must have a scheme and netloc (i.e. not relative URLs)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute with a scheme and host")

    # Ensure the scheme is allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed URL scheme: {parsed.scheme}")

    # Validate the host against approved domains
    if not _is_approved_domain(parsed.netloc):
        raise ValueError(f"Unapproved domain: {parsed.netloc}")

    # Re‑assemble the URL to ensure it is in a canonical form
    safe_url = urlunparse(parsed)

    return safe_url