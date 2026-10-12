import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of approved domains (case‑insensitive)
APPROVED_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
    "internal.api.company.net",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:                       # start of string
        10\.                 |   # 10.0.0.0 – 10.255.255.255
        172\.(?:1[6-9]|2[0-9]|3[01])\. |  # 172.16.0.0 – 172.31.255.255
        192\.168\.
    )
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private range."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        # Not a valid IP address; treat as non‑private for safety
        return False


def _is_internal_host(hostname: str) -> bool:
    """Check if the hostname resolves to a private IP."""
    try:
        # Resolve all addresses for the hostname
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        # Cannot resolve; treat as external for safety
        return False

    for info in infos:
        ip = info[4][0]
        if _is_private_ip(ip):
            return True
    return False


def manage_webhook(url_hook: str) -> str:
    """
    Validate a webhook URL.

    Parameters
    ----------
    url_hook : str
        The URL provided by an external service.

    Returns
    -------
    str
        A sanitized URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is not approved or points to an internal network location.
    """
    if not isinstance(url_hook, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url_hook)

    # Scheme must be http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL scheme must be http or https")

    # Hostname is required
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Normalize to lower case for comparison
    host_lower = hostname.lower()

    if host_lower not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved")

    # Ensure the host does not resolve to a private IP
    if _is_internal_host(hostname):
        raise ValueError(f"Domain '{hostname}' resolves to an internal IP address")

    # Rebuild the URL to ensure it is clean
    safe_url = urlunparse((
        parsed.scheme,
        f"{parsed.hostname}:{parsed.port}" if parsed.port else parsed.hostname,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # fragments are stripped
    ))

    return safe_url


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         safe = manage_webhook("https://api.example.com/webhook?token=abc")
#         print(f"Safe URL: {safe}")
#     except ValueError as e:
#         print(f"Invalid webhook: {e}")