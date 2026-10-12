import re
import socket
from urllib.parse import urlparse
import ipaddress

# Regular expression to detect common internal hostnames.
_INTERNAL_HOSTNAME_RE = re.compile(
    r"""
    ^(?:localhost|127\.0\.\d{1,3}\.\d{1,3}|192\.168|10|172\.(?:1[6-9]|2\d|3[0-1]))   # IP ranges
    |^\s*$  # empty string
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Optional: maintain a whitelist of approved domains.
_APPROVED_DOMAINS = {
    # Example entries; populate as needed
    "api.example.com",
    "services.mycompany.org",
}


def _is_internal_ip(ip: str) -> bool:
    """
    Return True if the given IP string belongs to a private, loopback,
    or link-local network.
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # If the string is not a valid IP, treat it as non‑internal
        return False

    # ip_address.is_private covers 10/8, 172.16/12, 192.168/16
    # ip_address.is_loopback covers 127.0.0.1, ::1
    # ip_address.is_link_local covers fe80::/10
    return addr.is_private or addr.is_loopback or addr.is_link_local


def _is_internal_hostname(hostname: str) -> bool:
    """
    Detect common internal hostnames such as localhost or IPs in private ranges.
    """
    return bool(_INTERNAL_HOSTNAME_RE.match(hostname))


def verify_api_address(endpoint_address: str) -> str:
    """
    Validate that *endpoint_address* is a secure, external API endpoint.

    The function checks:

    1. The URL scheme must be HTTPS.
    2. The hostname cannot resolve to an internal IP address or
       belong to a known private/loopback range.
    3. Optionally, the hostname must be in an approved domain whitelist
       (if one is defined).

    Parameters
    ----------
    endpoint_address : str
        The URL to validate.

    Returns
    -------
    str
        The original, verified URL.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTPS, resolves to an internal IP,
        or is outside the approved domain whitelist.
    """
    if not endpoint_address:
        raise ValueError("Endpoint address is empty")

    parsed = urlparse(endpoint_address)

    # 1. Scheme must be HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # 2. Resolve hostname to IP(s) and check each
    if not parsed.hostname:
        raise ValueError("URL does not contain a hostname")

    # Prevent obvious internal hostnames
    if _is_internal_hostname(parsed.hostname):
        raise ValueError(f"Hostname '{parsed.hostname}' is disallowed (internal)")

    try:
        # Resolve all IP addresses for the hostname
        host_ips = socket.getaddrinfo(parsed.hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed: {exc}") from exc

    for info in host_ips:
        ip = info[4][0]
        if _is_internal_ip(ip):
            raise ValueError(f"Hostname '{parsed.hostname}' resolves to internal IP {ip}")

    # 3. Optional whitelist check
    if _APPROVED_DOMAINS:
        # Allow subdomains of approved domains
        hostname = parsed.hostname.lower()
        if not any(hostname == domain or hostname.endswith("." + domain) for domain in _APPROVED_DOMAINS):
            raise ValueError(f"Hostname '{hostname}' is not in the approved domain list")

    return endpoint_address