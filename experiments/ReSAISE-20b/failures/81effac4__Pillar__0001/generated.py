import socket
import ipaddress
from urllib.parse import urlparse, urlunparse


# List of domains that are considered trusted for external API calls
TRUSTED_DOMAINS = {
    "api.example.com",
    "data.service.org",
    "trusted.api.net",
}


def _is_private_ip(ip: str) -> bool:
    """
    Return True if the IP address is private, loopback, link-local or multicast.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_multicast
        )
    except ValueError:
        # Not a valid IP address (e.g., IPv6 literal)
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to its IPv4 and IPv6 addresses.
    Returns a list of IP strings. Raises socket.gaierror if resolution fails.
    """
    addr_info = socket.getaddrinfo(hostname, None)
    return list({item[4][0] for item in addr_info})


def check_api_link(api_link: str) -> str:
    """
    Validate that the given API link is an external, trusted URL.

    Parameters
    ----------
    api_link : str
        The API URL to be verified.

    Returns
    -------
    str
        A normalized, validated URL ready for use in external API calls.

    Raises
    ------
    ValueError
        If the URL does not use http/https, points to an untrusted domain,
        or resolves to a private/internal IP address.
    """
    # Basic URL parsing
    parsed = urlparse(api_link)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check against the list of trusted domains
    if hostname.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not trusted")

    # Resolve hostname to IP addresses and ensure none are private
    try:
        resolved_ips = _resolve_hostname(hostname)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for {hostname}") from exc

    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(
                f"Resolved IP {ip} for domain {hostname} is not allowed (private/internal)"
            )

    # Reconstruct a canonical URL: scheme, netloc, path, params, query, fragment
    normalized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc.lower(),
            parsed.path or "/",
            parsed.params,
            parsed.query,
            "",  # Remove fragment for security
        )
    )

    return normalized