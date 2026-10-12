import re
from urllib.parse import urlparse

# List of approved domains (add your own safe domains here)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe.example.net",
}

# Regular expression to detect IP addresses (both IPv4 and IPv6)
IP_ADDRESS_RE = re.compile(
    r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[
            (?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}
        \]
    )
    $
    """,
    re.VERBOSE,
)


def _is_ip_address(host: str) -> bool:
    """Return True if the host is an IP address."""
    return bool(IP_ADDRESS_RE.match(host))


def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate a user-supplied URL for safe redirection.

    Parameters
    ----------
    redirect_url : str
        The URL input provided by the user.

    Returns
    -------
    str
        The validated URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not part of the approved list or if it uses a disallowed scheme.
    """
    # Parse URL
    parsed = urlparse(redirect_url)

    # Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Extract hostname (lowercase for case-insensitive comparison)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    host = host.lower()

    # Reject plain IP addresses (unless explicitly whitelisted)
    if _is_ip_address(host):
        raise ValueError("Direct IP addresses are not allowed for redirection")

    # Check against approved domains
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain {host!r} is not approved for redirection")

    # Reconstruct the URL to ensure it contains only the safe components
    safe_url = parsed.geturl()
    return safe_url


# Example usage (uncomment to test)
# try:
#     print(secure_redirect_handler("https://example.com/page"))
# except ValueError as e:
#     print(f"Redirect rejected: {e}")