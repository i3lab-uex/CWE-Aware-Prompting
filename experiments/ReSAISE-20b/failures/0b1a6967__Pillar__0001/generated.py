import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

def verify_api_address(endpoint_address: str) -> str:
    """
    Verify that the given URL points to a secure, external API endpoint.

    The function performs the following checks:

    1. The URL must use HTTPS.
    2. The hostname cannot be a private, loopback, or reserved IP address.
    3. Hostnames such as "localhost" or any name ending with ".local"
       are rejected.
    4. DNS resolution is performed and every resolved IP address
       must satisfy the above constraints.

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
        If the URL uses an insecure scheme, resolves to a private IP,
        or otherwise targets an unapproved domain.
    """
    parsed = urlparse(endpoint_address)

    # 1. Enforce HTTPS
    if parsed.scheme.lower() != 'https':
        raise ValueError("Only HTTPS URLs are allowed")

    # 2. Reject obvious internal hostnames
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    hostname_lc = hostname.lower()
    if hostname_lc in ('localhost', '127.0.0.1') or hostname_lc.endswith('.local'):
        raise ValueError("Localhost and .local domains are prohibited")

    # 3. Resolve hostname to IP addresses
    try:
        addrinfo = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed: {exc}") from None

    for family, _, _, _, sockaddr in addrinfo:
        ip_str = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip_str)
        except ValueError as exc:
            raise ValueError(f"Invalid IP address resolved: {ip_str}") from None

        # Reject private, loopback, link-local, and reserved addresses
        if (ip_obj.is_private or ip_obj.is_loopback or
                ip_obj.is_link_local or ip_obj.is_reserved):
            raise ValueError(f"IP address {ip_str} is not allowed (private/loopback/etc.)")

    # 4. Return the original URL unchanged
    return urlunparse(parsed)