import re
from urllib.parse import urlparse, urlunparse

# Predefined list of domains that are allowed for redirection
SAFE_DOMAINS = {
    "example.com",
    "trusted.example.org",
    "myapp.local",
}

# Regular expression to detect numeric IP addresses
_IP_REGEX = re.compile(r"""
    ^
    (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
    (?:25[0-5]|2[0-4]\d|1?\d{1,2})
    $
""", re.VERBOSE)


def _is_ip_address(host: str) -> bool:
    """Return True if the host is an IP address."""
    return _IP_REGEX.match(host) is not None


def secure_url_redirect(destination_url: str) -> str:
    """
    Validate and sanitize a destination URL for safe redirection.

    Parameters
    ----------
    destination_url : str
        The user supplied URL to redirect to.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is guaranteed to point to an allowed domain.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme, or its domain is not in SAFE_DOMAINS.
    """
    if not destination_url:
        raise ValueError("Destination URL cannot be empty")

    # Parse the URL
    parsed = urlparse(destination_url)

    # Ensure we have a scheme and netloc (i.e., not a relative path)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and contain a scheme (http/https)")

    # Only allow http or https schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs that resolve to an IP address unless explicitly allowed
    host = parsed.hostname or ""
    if _is_ip_address(host):
        raise ValueError("Redirection to IP addresses is prohibited")

    # Normalize the hostname (case-insensitive)
    host_lower = host.lower()

    # Allow subdomains of safe domains if desired; here we only allow exact matches
    if host_lower not in SAFE_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed for redirection")

    # Rebuild the URL to ensure it is canonical
    sanitized = urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return sanitized