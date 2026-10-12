import socket
import ipaddress
from urllib.parse import urlparse

# List of domains that are explicitly allowed as trusted API endpoints.
TRUSTED_DOMAINS = {
    "api.trusted.com",
    "services.safe.org",
    # Add more trusted domains here as needed
}

# List of URL schemes that are permitted.
ALLOWED_SCHEMES = {"http", "https"}


def _is_internal_ip(ip: str) -> bool:
    """
    Determine whether an IP address is private, loopback,
    link-local or otherwise considered internal.
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # If the address cannot be parsed, treat it as unsafe.
        return True
    return (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_reserved
    )


def _hostname_resolves_to_external_ip(hostname: str) -> bool:
    """
    Resolve the hostname and ensure that at least one of its IP addresses
    is not internal. If all resolved addresses are internal, return False.
    """
    try:
        addr_infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return False

    for family, _, _, _, sockaddr in addr_infos:
        ip = sockaddr[0]
        if not _is_internal_ip(ip):
            return True
    return False


def verify_api_address(url_to_check: str) -> str:
    """
    Verify that the supplied URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL, unchanged.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, resolves to a private IP,
        or is not in the list of trusted domains.
    """
    parsed = urlparse(url_to_check)

    # Validate scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate netloc (hostname and optional port)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check that the domain is in the trusted list
    if hostname.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Hostname '{hostname}' is not a trusted domain")

    # Resolve hostname to IP(s) and ensure at least one is external
    if not _hostname_resolves_to_external_ip(hostname):
        raise ValueError(
            f"Hostname '{hostname}' resolves only to internal IP addresses"
        )

    # All checks passed; return the original URL
    return url_to_check