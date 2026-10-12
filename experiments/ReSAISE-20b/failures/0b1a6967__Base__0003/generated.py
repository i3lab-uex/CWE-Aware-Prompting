import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# A simple whitelist of allowed hostnames or domain suffixes.
ALLOWED_DOMAINS = [
    "api.example.com",
    ".example.org",  # any sub‑domain of example.org
]

# Regex to detect common private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        # 10.0.0.0/8
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0/12
        (?:172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0/16
        (?:192\.168\.\d{1,3}\.\d{1,3})|
        # localhost
        (?:127\.0(?:\.\d{1,3}\.\d{1,3})?)|
        # IPv6 loopback
        (?:::1)|
        # link‑local
        (?:fe80:|fc00:|fd00:)
    )$
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_ip_private(ip: str) -> bool:
    """Return True if the IP is in a private or loopback range."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        return False

def _host_allowed(host: str) -> bool:
    """Check if the host is in the whitelist."""
    # Direct match
    if host.lower() in (d.lower().lstrip(".") for d in ALLOWED_DOMAINS):
        return True
    # Suffix match (e.g., sub.example.org)
    for d in ALLOWED_DOMAINS:
        if d.startswith("."):
            if host.lower().endswith(d.lower()):
                return True
    return False

def verify_api_address(endpoint_address: str) -> str:
    """
    Validate that the provided URL points to a secure, external API endpoint.

    Raises ValueError if:
        * The URL is malformed.
        * The scheme is not http or https.
        * The host resolves to a private/loopback IP.
        * The host is not in the whitelist.

    Returns:
        The normalized URL (scheme, netloc, path, params, query, fragment).
    """
    if not isinstance(endpoint_address, str):
        raise ValueError("Endpoint address must be a string")

    parsed = urlparse(endpoint_address)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Resolve the hostname to all IPs
    try:
        _, _, ip_list = socket.gethostbyname_ex(host)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{host}': {exc}") from exc

    # Reject any private or loopback IP
    for ip in ip_list:
        if _is_ip_private(ip):
            raise ValueError(f"Hostname '{host}' resolves to a private IP address: {ip}")

    # Additional regex guard for IPv6 link‑local, etc.
    if PRIVATE_IP_REGEX.match(host):
        raise ValueError(f"Hostname '{host}' is disallowed by private IP regex")

    # Check against the whitelist
    if not _host_allowed(host):
        raise ValueError(f"Hostname '{host}' is not in the approved list")

    # Reconstruct a clean URL (remove userinfo, port if default)
    netloc = host
    if parsed.port and ((parsed.scheme == "http" and parsed.port != 80) or
                        (parsed.scheme == "https" and parsed.port != 443)):
        netloc += f":{parsed.port}"

    cleaned = urlunparse((
        parsed.scheme,
        netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))
    return cleaned