import re
from urllib.parse import urlparse, urlunparse

# Predefined set of safe domains for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "mydomain.net",
}

# Allowed schemes for redirection
ALLOWED_SCHEMES = {"http", "https"}


def user_defined_redirect(redirect_url: str) -> str:
    """
    Validates and sanitizes a user-provided URL for safe redirection.

    Parameters
    ----------
    redirect_url : str
        The URL provided by the user for redirection.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not in ALLOWED_DOMAINS or if it uses an
        unsupported scheme.
    """

    # Reject empty strings and strip whitespace
    if not redirect_url or not redirect_url.strip():
        raise ValueError("Redirect URL cannot be empty")

    # Parse the input URL
    parsed = urlparse(redirect_url.strip())

    # Ensure scheme is present and allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate netloc (domain + optional port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Normalize domain: strip leading 'www.' for comparison
    normalized_host = host.lower()
    if normalized_host.startswith("www."):
        normalized_host = normalized_host[4:]

    # Check against allowed domains
    if normalized_host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{normalized_host}' is not allowed for redirection")

    # Reconstruct the URL to ensure no query or fragment injection
    sanitized = urlunparse((
        parsed.scheme,
        f"{host}:{parsed.port}" if parsed.port else host,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized