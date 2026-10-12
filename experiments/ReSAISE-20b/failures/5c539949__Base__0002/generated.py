import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (example)
APPROVED_DOMAINS = {
    "example.com",
    "www.example.org",
    "api.safe-site.net",
}

# Regex for private IP ranges to block direct IP redirection
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (?:                # IPv4
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1
    )
    |
    (?:                # IPv6 private addresses
        fd[0-9a-f]{2}:[0-9a-f:]+|
        fe80:[0-9a-f:]+
    )
    $
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP address."""
    try:
        # Attempt to interpret as IPv4
        octets = host.split(".")
        if len(octets) == 4 and all(0 <= int(part) < 256 for part in octets):
            return bool(PRIVATE_IP_REGEX.match(host))
    except ValueError:
        pass
    # IPv6 or hostname – skip IP check here
    return False

def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate and sanitize a user‑supplied redirect URL.

    Parameters
    ----------
    redirect_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized, absolute URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not in APPROVED_DOMAINS or if it points to a private IP.
    """
    # Parse the URL
    parsed = urlparse(redirect_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and include scheme and host")

    # Reject non‑HTTP(S) schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only HTTP(S) URLs are allowed")

    # Reject private IP addresses
    if _is_private_ip(parsed.hostname or ""):
        raise ValueError("Redirect to private IP addresses is prohibited")

    # Normalize hostname (lowercase)
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Check against approved domains
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to ensure no extra fragments or query tampering
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            "",  # params
            parsed.query,  # allow query parameters from the approved domain
            "",  # fragment
        )
    )

    return sanitized