import re
from urllib.parse import urlparse, ParseResult
import ipaddress

# List of approved public-facing API domains (example)
APPROVED_DOMAINS = {
    "api.example.com",
    "webhook.myservice.org",
    "hooks.anotherdomain.net"
}

# Regular expression for common private IP ranges (IPv4 and IPv6)
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:                  # start of the string
        (10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}          |   # 10.x.x.x or 127.x.x.x
        (172\.(1[6-9]|2\d|3[0-1]))\.\d{1,3}\.\d{1,3} |   # 172.16-31.x.x
        (192\.168)\.\d{1,3}\.\d{1,3}                |   # 192.168.x.x
        (169\.254)\.\d{1,3}\.\d{1,3}                |   # link-local 169.254.x.x
        (fc00|fd00):.*                              |   # IPv6 unique local addresses
        fe80:.*                                      # link-local IPv6
    )$
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_private_ip(ip_str: str) -> bool:
    """Return True if the IP is private or loopback."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not a valid IP address; treat as non-private.
        return False

def _is_private_hostname(hostname: str) -> bool:
    """Check if a hostname resolves to a private IP."""
    # Resolve the hostname; if resolution fails, we treat it as non-private
    try:
        import socket
        for addrinfo in socket.getaddrinfo(hostname, None):
            ip = addrinfo[4][0]
            if _is_private_ip(ip):
                return True
    except Exception:
        pass
    return False

def manage_webhook(url_hook: str) -> str:
    """
    Validate a webhook URL.

    Parameters
    ----------
    url_hook : str
        The URL provided by an external service that should point to a public API endpoint.

    Returns
    -------
    str
        The validated URL if it points to an approved domain and is not targeting a private network.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list or points to a private/internal network.
    """
    if not isinstance(url_hook, str):
        raise ValueError("Webhook URL must be a string")

    parsed: ParseResult = urlparse(url_hook)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL format")

    # Normalise hostname (lowercase, strip port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Check against approved domains
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not an approved API endpoint")

    # Reject URLs that target private IP ranges or internal networks
    if _is_private_ip(host):
        raise ValueError("URL points to a private IP address")

    if _is_private_hostname(host):
        raise ValueError("URL hostname resolves to a private IP address")

    # Ensure the scheme is safe
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only HTTP/HTTPS schemes are allowed")

    # Reconstruct the URL to guarantee a clean output
    safe_url = parsed.geturl()
    return safe_url