import re
from urllib.parse import urlparse, urlunparse

# Predefined list of safe domains (case‑insensitive)
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe-site.net",
}

# Regular expression to validate domain format
DOMAIN_RE = re.compile(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

def secure_url_redirect(destination_url: str) -> str:
    """
    Validate and sanitize a user‑provided URL for safe redirection.

    Parameters
    ----------
    destination_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized URL that is guaranteed to point to an allowed domain.

    Raises
    ------
    ValueError
        If the URL is malformed or its domain is not in ALLOWED_DOMAINS.
    """
    # Parse the URL and ensure it has a scheme
    parsed = urlparse(destination_url.strip())
    if not parsed.scheme:
        # Default to https for safety
        parsed = parsed._replace(scheme="https")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain).")

    # Extract the domain part, removing port if present
    host = parsed.hostname.lower()
    if not host or not DOMAIN_RE.match(host):
        raise ValueError(f"Invalid domain: {host}")

    # Enforce that the host is in the allowed list
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed for redirection.")

    # Rebuild the URL with a secure scheme (https)
    safe_parsed = parsed._replace(scheme="https")
    return urlunparse(safe_parsed)