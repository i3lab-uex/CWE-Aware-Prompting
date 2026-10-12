import re
from urllib.parse import urlparse, urlunparse

# Predefined list of safe domains for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local"
}

# Regular expression to detect protocol‑relative URLs (e.g., //example.com)
PROTOCOL_RELATIVE_RE = re.compile(r"^//", re.IGNORECASE)

def secure_url_redirect(destination_url: str) -> str:
    """
    Sanitize a user‑supplied URL for safe redirection.

    Parameters
    ----------
    destination_url : str
        The raw URL provided by the user.

    Returns
    -------
    str
        A fully qualified, safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, protocol‑relative, or its domain is not in
        ALLOWED_DOMAINS.
    """

    # Reject protocol‑relative URLs to avoid confusion about the origin
    if PROTOCOL_RELATIVE_RE.match(destination_url):
        raise ValueError("Protocol‑relative URLs are not allowed")

    # Parse the URL and ensure it contains a scheme
    parsed = urlparse(destination_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and contain a scheme")

    # Normalize the scheme to lower‑case
    scheme = parsed.scheme.lower()
    if scheme not in ("http", "https"):
        raise ValueError("Only HTTP and HTTPS schemes are allowed")

    # Extract hostname and compare against the whitelist
    host = parsed.hostname.lower() if parsed.hostname else ""
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed for redirection")

    # Rebuild the URL to ensure consistent formatting
    safe_parsed = parsed._replace(scheme=scheme, netloc=host + (f":{parsed.port}" if parsed.port else ""))
    safe_url = urlunparse(safe_parsed)

    return safe_url