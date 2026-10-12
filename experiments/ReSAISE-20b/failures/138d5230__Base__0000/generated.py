import re
from urllib.parse import urlparse, urlunparse

# Define a set of allowed hostnames (domains).  Add any safe domains here.
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.example.org",
    "myapp.local",
}

# Optional: allow specific IP ranges (e.g., localhost, 127.0.0.1)
ALLOWED_IP_RANGES = [
    re.compile(r"^127\.0\.0\.1$"),
    re.compile(r"^::1$"),  # IPv6 localhost
]

# Regular expression to detect IP addresses in netloc
IP_REGEX = re.compile(
    r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
    |
        # IPv6
        \[?[0-9a-fA-F:]+\]?
    )
    $
    """,
    re.VERBOSE,
)


def _is_ip_address(netloc: str) -> bool:
    """
    Returns True if the netloc is an IP address (IPv4 or IPv6).
    """
    return bool(IP_REGEX.match(netloc))


def _is_allowed_ip(ip: str) -> bool:
    """
    Checks whether the given IP address is in one of the allowed ranges.
    """
    for pattern in ALLOWED_IP_RANGES:
        if pattern.match(ip):
            return True
    return False


def user_defined_redirect(redirect_url: str) -> str:
    """
    Accepts a URL input from the user and returns a sanitized, safe redirect URL.

    Parameters
    ----------
    redirect_url : str
        The user-provided URL for redirection.

    Returns
    -------
    str
        A sanitized URL that is considered safe for redirection.

    Raises
    ------
    ValueError
        If the domain of the provided URL is not part of the allowed domains,
        or if it contains a disallowed IP address.
    """
    # Parse the URL
    parsed = urlparse(redirect_url)

    # Ensure scheme is http or https (or empty for relative URLs)
    if parsed.scheme and parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # For relative URLs (no netloc), we consider them safe
    if not parsed.netloc:
        # Reconstruct the URL to ensure no query injection
        return urlunparse(parsed)

    # Normalize netloc (strip port)
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError("URL must contain a hostname")

    # Check for IP addresses
    if _is_ip_address(host):
        if not _is_allowed_ip(host):
            raise ValueError(f"Disallowed IP address: {host}")
    else:
        # For domain names, check against allowed domains
        if host not in ALLOWED_DOMAINS:
            raise ValueError(f"Domain '{host}' is not allowed")

    # Reconstruct a sanitized URL (drop any unwanted components)
    safe_parsed = parsed._replace(
        scheme=parsed.scheme or "https",  # default to https if missing
        netloc=f"{host}{':' + str(parsed.port) if parsed.port else ''}",
    )
    return urlunparse(safe_parsed)