import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# Regular expression to reject URLs that point to local hostnames.
LOCALHOST_RE = re.compile(r'^(localhost|127\.0\.0\.1|::1)$', re.IGNORECASE)

# List of IP networks that are considered private or non‑public.
PRIVATE_NETWORKS = [
    ipaddress.ip_network('0.0.0.0/8'),      # "This" network
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('127.0.0.0/8'),     # Loopback
    ipaddress.ip_network('169.254.0.0/16'),  # Link‑local
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('224.0.0.0/4'),     # Multicast
    ipaddress.ip_network('240.0.0.0/4'),     # Reserved for future use
    ipaddress.ip_network('::1/128'),        # IPv6 loopback
    ipaddress.ip_network('fe80::/10'),      # Link‑local IPv6
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address belongs to a private or reserved network."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # If parsing fails, treat as unsafe.
        return True
    for net in PRIVATE_NETWORKS:
        if addr in net:
            return True
    return False

def enforce_api_security(api_endpoint: str) -> str:
    """
    Validate that ``api_endpoint`` is a publicly reachable HTTPS URL.

    The function performs the following checks:

    1. The scheme must be ``https``.
    2. The hostname cannot be a local host name or IP address
       (127.0.0.1, ::1, localhost).
    3. The hostname must resolve to at least one IP address that is
       not in a private or reserved network block.
    4. The resolved IP address must be reachable via DNS (no NXDOMAIN).

    If any of the checks fail, a ``ValueError`` is raised.

    Parameters
    ----------
    api_endpoint : str
        The URL to be validated.

    Returns
    -------
    str
        The original ``api_endpoint`` if it passes all checks.

    Raises
    ------
    ValueError
        If the URL does not meet security requirements.
    """
    if not isinstance(api_endpoint, str):
        raise ValueError("API endpoint must be a string")

    parsed = urlparse(api_endpoint)

    # 1. Scheme check
    if parsed.scheme.lower() != 'https':
        raise ValueError("Only HTTPS URLs are allowed")

    # 2. Hostname check
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject obvious local hostnames
    if LOCALHOST_RE.match(hostname):
        raise ValueError("Hostname points to localhost")

    # 3. Resolve hostname
    try:
        # Use getaddrinfo for both IPv4 and IPv6 support
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"DNS resolution failed for {hostname}") from exc

    # 4. Ensure at least one public IP
    public_ip_found = False
    for family, _, _, _, sockaddr in addr_info:
        ip_str = sockaddr[0]
        if _is_private_ip(ip_str):
            continue
        public_ip_found = True
        break

    if not public_ip_found:
        raise ValueError("Resolved IP addresses are all private or reserved")

    # 5. Reconstruct URL to guarantee normalized form
    sanitized = parsed._replace(scheme='https')
    return urlunparse(sanitized)

# Example usage (commented out to keep module importable)
# if __name__ == "__main__":
#     try:
#         safe_url = enforce_api_security("https://api.example.com/v1/data")
#         print(f"Verified URL: {safe_url}")
#     except ValueError as e:
#         print(f"URL rejected: {e}")