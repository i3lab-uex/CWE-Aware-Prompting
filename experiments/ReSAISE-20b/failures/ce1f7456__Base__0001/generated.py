import re
from urllib.parse import urlparse, urlunparse

# Predefined list of safe domains (example)
SAFE_DOMAINS = {
    "example.com",
    "www.example.org",
    "api.safe-site.net"
}

# Regular expression to detect private IP ranges
PRIVATE_IP_RE = re.compile(
    r"^(?:(?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|169\.254\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3}"
    r"|172\.((?:1[6-9])|(?:2\d)|(?:3[0-1]))\.\d{1,3}\.\d{1,3})$"
)


def _is_private_ip(ip: str) -> bool:
    """Check if an IP address is in a private or loopback range."""
    return PRIVATE_IP_RE.match(ip) is not None


def secure_url_redirect(destination_url: str) -> str:
    """
    Validate and sanitize a user‑supplied URL for safe redirection.

    Parameters
    ----------
    destination_url : str
        The URL supplied by the user to redirect to.

    Returns
    -------
    str
        A sanitized, fully‑qualified URL that is allowed for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not in SAFE_DOMAINS or resolves to a private IP.
    """
    if not destination_url:
        raise ValueError("Destination URL cannot be empty")

    parsed = urlparse(destination_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Resolve netloc to handle IPv6 and domain names
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject URLs that resolve to private IP addresses
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", host) and _is_private_ip(host):
        raise ValueError("Redirect to private IP addresses is forbidden")

    # Normalise host (lowercase) and compare against safe domains
    normalized_host = host.lower()
    if normalized_host not in SAFE_DOMAINS:
        raise ValueError(f"Domain '{normalized_host}' is not allowed for redirection")

    # Rebuild the URL to ensure no unexpected fragments or query parameters
    safe_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/",
            "",  # params
            "",  # query
            ""   # fragment
        )
    )

    return safe_url