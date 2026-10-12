import re
from urllib.parse import urlparse, urlunparse

# A predefined set of safe domains for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "myapp.local",
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}


def user_defined_redirect(redirect_url: str) -> str:
    """
    Validates and sanitizes a user-provided URL for safe redirection.

    Parameters
    ----------
    redirect_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized absolute URL that is guaranteed to use an allowed scheme
        and domain.

    Raises
    ------
    ValueError
        If the URL is malformed, uses a disallowed scheme, or its domain
        is not in `ALLOWED_DOMAINS`.
    """
    if not redirect_url:
        raise ValueError("Redirect URL must be provided")

    # Parse the URL
    parsed = urlparse(redirect_url)

    # Ensure scheme is present and allowed
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed scheme: {parsed.scheme}")

    # Ensure netloc (domain + optional port) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Extract the hostname (without port)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Normalize the domain to lower case for comparison
    if hostname.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not allowed")

    # Reconstruct the URL to guarantee a clean, absolute form
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or "",
    ))

    return sanitized