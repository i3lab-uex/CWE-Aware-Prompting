import re
from urllib.parse import urlparse, urlunparse

# Predefined safe domains (add or modify as needed)
ALLOWED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "myapp.local"
}

# Regular expression to validate domain names
DOMAIN_RE = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)

def user_defined_redirect(redirect_url: str) -> str:
    """
    Validate and sanitize a user supplied URL for safe redirection.

    Parameters
    ----------
    redirect_url : str
        The URL provided by the user for redirection.

    Returns
    -------
    str
        A sanitized, safe URL ready for use in a redirect response.

    Raises
    ------
    ValueError
        If the URL is malformed or its domain is not in ALLOWED_DOMAINS.
    """
    if not redirect_url:
        raise ValueError("Redirect URL must not be empty")

    # Parse the incoming URL
    parsed = urlparse(redirect_url)

    # Reject relative URLs (e.g., "/path") or URLs without a scheme
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Redirect URL must be absolute with a scheme")

    # Only allow http and https schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Redirect URL scheme must be http or https")

    # Normalise domain (case-insensitive)
    netloc = parsed.netloc.lower()

    # Extract host part, strip port if present
    host = netloc.split(":")[0]

    # Basic domain validation
    if not DOMAIN_RE.match(host):
        raise ValueError(f"Invalid host in redirect URL: {host}")

    # Check against allowed domains
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed for redirection")

    # Reconstruct a clean URL (drop fragments, query parameters can be kept)
    sanitized = urlunparse((
        parsed.scheme,
        netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # remove fragment
    ))

    return sanitized