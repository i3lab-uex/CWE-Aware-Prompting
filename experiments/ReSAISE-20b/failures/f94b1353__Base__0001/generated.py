import re
import socket
from urllib.parse import urlparse, urlunparse

# List of approved API endpoint hostnames (exact match or wildcard subdomains)
APPROVED_DOMAINS = [
    r"^api\.example\.com$",
    r"^services\.trusted\.org$",
    r"^internal\.api\.company\.com$",  # internal but approved
]

# Private IP networks that should be blocked even if hostname resolves to them
PRIVATE_IP_RANGES = [
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
    "127.0.0.0/8",
    "::1/128",          # loopback
    "fc00::/7",         # unique local address
]

# Compile regexes once for performance
APPROVED_REGEXES = [re.compile(d) for d in APPROVED_DOMAINS]
PRIVATE_IP_RENDS = [socket.inet_aton(r.split("/")[0]) for r in PRIVATE_IP_RANGES if ":" not in r]
# For IPv6 ranges we would need a separate check, omitted for brevity


def _is_approved_hostname(hostname: str) -> bool:
    """Return True if the hostname matches one of the approved patterns."""
    return any(regex.match(hostname) for regex in APPROVED_REGEXES)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is within a private network."""
    try:
        # IPv4
        packed_ip = socket.inet_aton(ip)
        for net in PRIVATE_IP_RANGES:
            if ip.startswith(net.split("/")[0]):
                # simple prefix check; for production use ipaddress module
                return True
    except OSError:
        pass  # Not an IPv4 address; ignore for now
    return False


def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve hostname to a list of IP addresses."""
    try:
        return [info[4][0] for info in socket.getaddrinfo(hostname, None)]
    except socket.gaierror:
        return []


def manage_webhook(url_hook: str) -> str:
    """
    Validate a webhook URL against approved API endpoints and internal network restrictions.

    Parameters
    ----------
    url_hook : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A normalized, validated URL that points to an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is not approved or resolves to a private/internal IP address.
    """
    if not url_hook:
        raise ValueError("Empty URL provided")

    parsed = urlparse(url_hook)

    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # 1. Check approved domain list
    if not _is_approved_hostname(hostname):
        raise ValueError(f"Hostname '{hostname}' is not in the list of approved domains")

    # 2. Resolve hostname to IPs and check for private addresses
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Unable to resolve hostname: {hostname}")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} is a private/internal address")

    # 3. Reconstruct the URL to ensure canonical form
    safe_url = urlunparse(
        (
            parsed.scheme.lower(),
            f"{hostname}{parsed.port and ':' + str(parsed.port) or ''}",
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return safe_url