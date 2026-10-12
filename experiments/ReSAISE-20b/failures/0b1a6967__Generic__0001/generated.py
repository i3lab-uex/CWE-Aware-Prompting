import socket
from urllib.parse import urlparse
import ipaddress

def verify_api_address(endpoint_address: str) -> str:
    """
    Verify that the given URL points to a secure, external API endpoint.

    The function checks:
        * HTTPS scheme
        * Non‑localhost hostname
        * Resolved IP address is not in private, loopback, link‑local,
          or multicast ranges

    Parameters
    ----------
    endpoint_address : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, not HTTPS, points to a disallowed domain,
        or resolves to an internal IP address.
    """
    # Parse the URL
    parsed = urlparse(endpoint_address)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {endpoint_address}")

    # Ensure HTTPS
    if parsed.scheme.lower() != 'https':
        raise ValueError(f"Only HTTPS URLs are allowed: {endpoint_address}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError(f"URL does not contain a valid hostname: {endpoint_address}")

    # Resolve the hostname to all IPv4/IPv6 addresses
    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{hostname}': {exc}") from exc

    # Validate each resolved IP address
    for family, _, _, _, sockaddr in addr_info:
        ip_str = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip_str)
        except ValueError as exc:
            raise ValueError(f"Invalid IP address resolved from '{hostname}': {ip_str}") from exc

        # Reject loopback, private, link‑local, multicast, unspecified,
        # and reserved addresses
        if (ip_obj.is_loopback or ip_obj.is_private or ip_obj.is_link_local or
                ip_obj.is_multicast or ip_obj.is_unspecified or
                ip_obj.is_reserved):
            raise ValueError(
                f"Disallowed IP address resolved from '{hostname}': {ip_str}"
            )

    # All checks passed
    return endpoint_address