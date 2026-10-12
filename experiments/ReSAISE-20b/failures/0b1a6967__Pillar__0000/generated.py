import re
import socket
from urllib.parse import urlparse
import ipaddress

# Regular expression to detect IPv4 or IPv6 literals in a hostname
IP_LITERAL_RE = re.compile(
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
    re.VERBOSE
)

# List of well‑known internal hostnames that should never be used for external APIs
INTERNAL_HOSTNAMES = {
    "localhost",
    "127.0.0.1",
    "::1",
}

# Common private IP ranges
PRIVATE_IP_RANGES = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
    ipaddress.IPv6Network("fc00::/7"),   # Unique local addresses
    ipaddress.IPv6Network("fe80::/10")  # Link‑local addresses
]


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address string is in a private range."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    for network in PRIVATE_IP_RANGES:
        if addr in network:
            return True
    return False


def _is_internal_hostname(hostname: str) -> bool:
    """Return True if the hostname is a known internal host."""
    return hostname.lower() in INTERNAL_HOSTNAMES


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve the hostname to a list of IP addresses.
    If resolution fails, an empty list is returned.
    """
    try:
        infos = socket.getaddrinfo(hostname, None)
        return list({info[4][0] for info in infos})
    except socket.gaierror:
        return []


def verify_api_address(endpoint_address: str) -> str:
    """
    Verify that a given URL is safe for use as an external API endpoint.

    The function performs the following checks:

        1. The URL scheme must be HTTPS.
        2. The hostname must not be an internal address (localhost, 127.x.x.x,
           ::1, or any private IP ranges).
        3. If the hostname is an IP literal, it must not be in a private range.
        4. If the hostname is a domain name, DNS resolution must not resolve
           to any private IP address.

    If all checks pass the original URL is returned unchanged.  Otherwise a
    ValueError is raised with an explanatory message.

    Args:
        endpoint_address: The URL to validate.

    Returns:
        str: The verified URL if it is allowed.

    Raises:
        ValueError: If the URL targets an unapproved domain or any address
                    within internal networks.
    """
    if not endpoint_address:
        raise ValueError("Endpoint address must be a non‑empty string")

    parsed = urlparse(endpoint_address)

    # 1. Scheme must be HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError(f"URL must use HTTPS, got scheme '{parsed.scheme}'")

    # 2. Extract hostname (may include port)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # 3. Reject known internal hostnames
    if _is_internal_hostname(hostname):
        raise ValueError(f"Hostname '{hostname}' is an internal address")

    # 4. If hostname is an IP literal, check for private ranges
    if IP_LITERAL_RE.match(hostname):
        # Strip brackets for IPv6 literal
        ip_str = hostname.strip("[]")
        if _is_private_ip(ip_str):
            raise ValueError(f"IP address '{ip_str}' is a private/internal IP")
        return endpoint_address

    # 5. Resolve domain name and ensure none of the resolved IPs are private
    resolved_ips = _resolve_hostname(hostname)
    if not resolved_ips:
        # If DNS resolution fails, be conservative and reject
        raise ValueError(f"Hostname '{hostname}' could not be resolved")

    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(
                f"Resolved IP address '{ip}' for hostname '{hostname}' "
                "is a private/internal IP"
            )

    # All checks passed
    return endpoint_address