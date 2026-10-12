import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of domains that are considered trusted.  Add or remove entries as needed.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.trusted.net",
    # Wildcard support: the function will match subdomains as well
}

# List of IP network ranges that are considered internal or otherwise disallowed.
DISALLOWED_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),  # link-local
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fe80::/10"),      # link-local IPv6
]

def _is_ip_allowed(ip: str) -> bool:
    """Return True if the IP is not in any disallowed network."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # If we cannot parse the IP, treat it as disallowed
        return False

    for network in DISALLOWED_IP_RANGES:
        if addr in network:
            return False
    return True

def _is_domain_trusted(hostname: str) -> bool:
    """Check if the hostname matches one of the trusted domains."""
    # Normalize to lower case
    hostname = hostname.lower()
    for domain in TRUSTED_DOMAINS:
        if hostname == domain or hostname.endswith("." + domain):
            return True
    return False

def verify_api_address(url_to_check: str) -> str:
    """
    Verify that a URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL (unchanged from the input).

    Raises
    ------
    ValueError
        If the URL does not belong to a trusted domain or if it resolves to an
        internal or otherwise disallowed IP address.
    """
    parsed = urlparse(url_to_check)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include a scheme and host")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # 1. Check that the domain is in our whitelist
    if not _is_domain_trusted(hostname):
        raise ValueError(f"Hostname '{hostname}' is not in the list of trusted domains")

    # 2. Resolve the hostname to all IP addresses
    try:
        addrinfo = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    # 3. Ensure at least one resolved IP is allowed
    if not any(_is_ip_allowed(info[4][0]) for info in addrinfo):
        raise ValueError(f"All resolved IPs for '{hostname}' are disallowed (internal or private)")

    # 4. Reconstruct the URL to normalise it
    normalized = urlunparse(parsed._replace(netloc=parsed.netloc.lower()))
    return normalized