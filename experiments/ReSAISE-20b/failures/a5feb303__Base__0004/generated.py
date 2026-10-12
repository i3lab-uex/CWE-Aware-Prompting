import re
from urllib.parse import urlparse, urlunparse

# Predefined safe domains for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.localhost",  # allow local dev domain if needed
}

# Regex to detect IP addresses (IPv4 and IPv6)
IP_REGEX = re.compile(
    r"""
    ^(?:
        # IPv4
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})
        |
        # IPv6
        \[?[A-F0-9]*:[A-F0-9:]+\]?
    )$
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_ip_address(host: str) -> bool:
    """Return True if host is an IP address."""
    return bool(IP_REGEX.match(host))

def process_user_redirect(input_url: str) -> str:
    """
    Validate and sanitize a user-provided URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized, absolute URL that is guaranteed to point to an allowed domain.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a disallowed domain, or resolves to an IP address.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(input_url)

    # Ensure scheme is http or https and that the URL is absolute
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL scheme must be http or https")

    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Normalize hostname (case-insensitive)
    host = parsed.hostname.lower()

    # Reject URLs that resolve to an IP address
    if _is_ip_address(host):
        raise ValueError("Redirection to IP addresses is not allowed")

    # Reject localhost unless explicitly whitelisted
    if host in {"localhost", "127.0.0.1", "::1"} and host not in ALLOWED_DOMAINS:
        raise ValueError("Redirection to localhost is disallowed")

    # Validate domain against allowed list
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed for redirection")

    # Reconstruct the URL to ensure consistency (remove fragments, etc.)
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,  # keep query string
        ""   # no fragment
    ))

    return sanitized