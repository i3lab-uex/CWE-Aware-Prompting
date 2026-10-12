import re
import socket
from urllib.parse import urlparse, urlunparse
from ipaddress import ip_address, IPv4Address, IPv6Address

# List of domains that are considered trusted.  Add any other allowed
# external API hosts here.
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.trusted.net",
    "v1.partner.org",
}

# Regular expression to match a valid HTTP/HTTPS URL.
_URL_RE = re.compile(
    r'^(?P<scheme>https?)://'
    r'(?P<host>[^:/?#]+)'
    r'(?::(?P<port>\d+))?'
    r'(?:/[^?#]*)?'
    r'(?:\?[^\#]*)?'
    r'(?:\#[^\s]*)?$',
    re.IGNORECASE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address string is private or reserved."""
    try:
        addr = ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return True

    if addr.is_loopback or addr.is_link_local:
        return True
    # RFC1918 private ranges and the 127/8 loopback are handled by is_private
    if addr.is_private:
        return True
    # IPv6 unique local addresses (fc00::/7)
    if isinstance(addr, IPv6Address) and addr.is_private:
        return True
    # Additional reserved ranges (e.g., 0.0.0.0/8, ::1)
    if addr.is_reserved or addr.is_multicast:
        return True
    return False


def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that the given URL points to an external trusted API endpoint.

    Parameters
    ----------
    api_url : str
        The URL to be validated.

    Returns
    -------
    str
        The same URL if it is valid and trusted.

    Raises
    ------
    ValueError
        If the URL does not use http/https, is not in ALLOWED_DOMAINS,
        or resolves to a private/internal IP address.
    """
    if not isinstance(api_url, str):
        raise ValueError("api_url must be a string")

    match = _URL_RE.match(api_url.strip())
    if not match:
        raise ValueError("Malformed URL")

    scheme = match.group('scheme').lower()
    host = match.group('host')
    port = int(match.group('port')) if match.group('port') else (
        443 if scheme == 'https' else 80
    )

    # Enforce that the host is in the list of allowed domains.
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Resolve the hostname to IP addresses and ensure none are private.
    try:
        addrinfo = socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

    for entry in addrinfo:
        sockaddr = entry[4]
        ip_str = sockaddr[0]  # IPv4 or IPv6 address string
        if _is_private_ip(ip_str):
            raise ValueError(
                f"Resolved IP '{ip_str}' for host '{host}' is private or reserved"
            )

    # All checks passed – return the normalized URL.
    parsed = urlparse(api_url)
    normalized = urlunparse(parsed._replace(scheme=scheme, netloc=f"{host}:{port}" if port not in (80, 443) else host))
    return normalized