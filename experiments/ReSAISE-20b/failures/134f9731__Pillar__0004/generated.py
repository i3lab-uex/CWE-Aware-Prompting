import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Approved public API endpoints (example list)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "webhooks.service.org",
    "secure.api.net",
}

# Regex to detect private IP address ranges (IPv4 and IPv6)
PRIVATE_IP_RE = re.compile(
    r"""
    ^(
        # 10.0.0.0/8
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0/12
        (172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0/16
        (192\.168\.\d{1,3}\.\d{1,3})|
        # IPv6 link-local
        (fe80::[0-9a-fA-F:]+)|
        # IPv6 unique local
        (fc00::[0-9a-fA-F:]+)|
        # IPv6 loopback
        (::1)
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip_str: str) -> bool:
    """Return True if the given IP string is a private address."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # If parsing fails, assume it's not a valid IP (not private)
        return False

def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL and return a secure, internal API URL.

    Parameters
    ----------
    webhook_endpoint : str
        The external webhook URL to validate.

    Returns
    -------
    str
        A validated, safe internal API URL for initiating a call.

    Raises
    ------
    ValueError
        If the domain is not whitelisted or if it resolves to a private network.
    """
    # Parse the incoming URL
    parsed = urlparse(webhook_endpoint)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL format")

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL scheme must be http or https")

    # Reject URLs with query parameters that might attempt open redirects
    if parsed.query:
        raise ValueError("URL must not contain query parameters")

    # Normalise domain: remove port for comparison
    host = parsed.hostname.lower()
    if not host:
        raise ValueError("URL must contain a hostname")

    # Check against whitelist
    if host not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the approved whitelist")

    # Resolve potential IP addresses (simple check: if hostname looks like an IP)
    ip_candidate = host
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", host) or re.match(r"^[0-9a-fA-F:]+$", host):
        ip_candidate = host

    if _is_private_ip(ip_candidate) or PRIVATE_IP_RE.match(ip_candidate):
        raise ValueError("URL resolves to a private network address")

    # Construct the internal API URL (example: prefix with internal gateway)
    # Here we simply return the validated URL unchanged, but you could
    # prepend an internal base if required.
    safe_url = urlunparse(
        (
            parsed.scheme,
            host,
            parsed.path or "/",
            "",  # params
            "",  # query
            ""   # fragment
        )
    )

    return safe_url

# Example usage:
if __name__ == "__main__":
    try:
        internal_api = verify_webhook("https://api.example.com/webhooks")
        print(f"Validated URL: {internal_api}")
    except ValueError as e:
        print(f"Validation error: {e}")