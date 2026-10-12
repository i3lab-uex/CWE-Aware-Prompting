import re
from urllib.parse import urlparse, urlunparse

# Predefined set of safe domains (add or remove as needed)
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.org",
    "myapp.local",
}

# Regular expression to validate URLs (basic check)
_URL_REGEX = re.compile(
    r"^(https?://)"          # http or https scheme
    r"([A-Za-z0-9.-]+)"      # domain
    r"(?:/[\w\-./?%&=]*)?$"  # optional path/query
)

def secure_url_redirect(destination_url: str) -> str:
    """
    Validate and sanitize a user-provided URL for redirection.

    Parameters
    ----------
    destination_url : str
        The URL provided by the user for redirection.

    Returns
    -------
    str
        A sanitized, safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed or its domain is not in ALLOWED_DOMAINS.
    """
    # Basic sanity check with regex
    if not _URL_REGEX.match(destination_url):
        raise ValueError("Malformed URL")

    parsed = urlparse(destination_url)

    # Normalize domain (case-insensitive)
    host = parsed.hostname.lower() if parsed.hostname else ""
    # Remove leading 'www.' for comparison
    host = re.sub(r"^www\.", "", host)

    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed for redirection")

    # Reconstruct the URL to ensure no scheme manipulation
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return safe_url