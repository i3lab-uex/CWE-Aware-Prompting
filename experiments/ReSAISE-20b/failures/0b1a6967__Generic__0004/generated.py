import re
from urllib.parse import urlparse
import ipaddress

# Define a whitelist of approved domains.
# Add or remove entries as needed for your environment.
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.company.com",
    # Add more fully‑qualified domain names here.
}

# Regular expression to match IPv6 addresses (with or without brackets)
IPV6_REGEX = re.compile(r"^\[?(?P<ip>[^]]+)\]?$")

def _is_internal_ip(ip: str) -> bool:
    """
    Determine if an IP address string represents a private, loopback,
    or link‑local address that should be blocked.
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        # Not a valid IP address; let the caller handle it.
        return False

    return (
        ip_obj.is_private
        or ip_obj.is_loopback
        or ip_obj.is_link_local
    )

def verify_api_address(endpoint_address: str) -> str:
    """
    Verify that a given URL points to an approved external API endpoint.

    Parameters
    ----------
    endpoint_address : str
        The URL that needs to be verified.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, has no hostname,
        points to a private/internal IP address, or is not on the
        whitelist of approved domains.
    """
    if not isinstance(endpoint_address, str):
        raise ValueError("Endpoint address must be a string")

    parsed = urlparse(endpoint_address)

    # Scheme validation
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS allowed.")

    # Hostname extraction
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Detect IPv6 address in brackets and strip them for validation
    match = IPV6_REGEX.match(hostname)
    if match:
        hostname_ip = match.group("ip")
    else:
        hostname_ip = hostname

    # If the host is an IP address, check for internal addresses
    try:
        ipaddress.ip_address(hostname_ip)
        if _is_internal_ip(hostname_ip):
            raise ValueError(f"IP address '{hostname_ip}' is internal or private")
    except ValueError:
        # Not an IP address; treat as a domain name
        if hostname.lower() not in ALLOWED_DOMAINS:
            raise ValueError(f"Domain '{hostname}' is not on the whitelist")

    # Additional optional checks (e.g., DNS rebinding) can be added here.

    return endpoint_address