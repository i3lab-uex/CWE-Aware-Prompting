import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of domains that are explicitly allowed to be called by the product.
APPROVED_DOMAINS = {
    "api.example.com",
    "service.trusted.org",
    # Add more approved domains here.
}

# IPv4 and IPv6 ranges considered internal/private
INTERNAL_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),          # loopback
    ipaddress.ip_network("::1/128"),             # IPv6 loopback
    ipaddress.ip_network("fe80::/10"),           # link-local
    ipaddress.ip_network("fc00::/7"),            # unique local (ULA)
]

def _is_internal_ip(ip: str) -> bool:
    """Return True if the IP address is in a private/internal range."""
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        # If the IP cannot be parsed, treat it as unsafe.
        return True
    for net in INTERNAL_IP_RANGES:
        if ip_obj in net:
            return True
    return False

def validate_service_url(service_url: str) -> str:
    """
    Validate that `service_url` points to an approved external API.

    The function performs the following checks:
        1. Parses the URL and ensures it has a scheme (http/https) and network location.
        2. Resolves the hostname to one or more IP addresses.
        3. Ensures that every resolved IP address is not in a private/internal range.
        4. Confirms that the hostname ends with one of the approved domains.

    Parameters
    ----------
    service_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL does not contain a scheme, has an unapproved domain,
        or resolves to any internal IP address.
    """
    if not isinstance(service_url, str):
        raise ValueError("service_url must be a string")

    parsed = urlparse(service_url)

    # 1. Basic URL validation
    if not parsed.scheme or parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("URL must use http or https scheme")
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (hostname)")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # 2. Resolve hostname to IP addresses
    try:
        addr_info = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    # 3. Check each IP address
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_internal_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{hostname}' is internal or private")

    # 4. Domain approval check
    # Normalize hostname to lower case for comparison.
    hostname_lc = hostname.lower()
    if not any(hostname_lc == domain or hostname_lc.endswith("." + domain)
               for domain in APPROVED_DOMAINS):
        raise ValueError(f"Hostname '{hostname}' is not in the list of approved domains")

    # Reconstruct a clean URL (preserve path, query, fragment)
    cleaned_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))
    return cleaned_url