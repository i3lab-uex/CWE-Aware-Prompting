import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (exact match)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "secure.net",
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}

def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate a user-supplied URL and return it only if its domain is approved.
    
    Parameters
    ----------
    redirect_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        The validated and sanitized URL ready for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses a disallowed scheme, or its domain
        is not in the approved list.
    """
    if not isinstance(redirect_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(redirect_url)

    # Ensure we have a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must contain a scheme and domain")

    # Normalize the scheme
    scheme = parsed.scheme.lower()
    if scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed URL scheme: {scheme}")

    # Normalise the domain (lowercase, strip port)
    netloc = parsed.netloc.lower()
    # Remove userinfo and port
    if '@' in netloc:
        _, host = netloc.rsplit('@', 1)
    else:
        host = netloc
    if ':' in host:
        host, _port = host.split(':', 1)

    # Check against approved domains
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Rebuild the URL to ensure no hidden characters
    safe_parts = (
        scheme,
        host,                    # netloc without port or userinfo
        parsed.path,
        parsed.params,
        parsed.query,
        ""                        # no fragment
    )
    safe_url = urlunparse(safe_parts)

    return safe_url