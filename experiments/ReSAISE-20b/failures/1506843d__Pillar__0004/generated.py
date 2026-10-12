import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# A whitelist of trusted domains.  In a real application this list should be
# configurable, not hard‑coded.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.trusted.org",
    "data.partner.net",
}

# Regular expression for matching IPv4 and IPv6 addresses
IPV4_REGEX = re.compile(r"""
    ^
    (?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}
    (?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)
    $
""", re.VERBOSE)

IPV6_REGEX = re.compile(r"""
    ^
    \[
        (?:
            [0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){7}
            |
            ([0-9a-fA-F]{1,4}:){1,7}:
            |
            ([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}
            |
            ([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}
            |
            ([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}
            |
            ([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}
            |
            ([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}
            |
            [0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})
            |
            :((:[0-9a-fA-F]{1,4}){1,7}|:)
        )
    \]
    $
""", re.VERBOSE)

def _is_ip_address(host: str) -> bool:
    """Return True if host is a literal IP address (IPv4 or IPv6)."""
    return bool(IPV4_REGEX.match(host) or IPV6_REGEX.match(host))

def _resolve_to_ips(host: str):
    """Resolve host to a list of IP addresses (IPv4/IPv6)."""
    try:
        # getaddrinfo returns a list of tuples; we want the IP part.
        return [
            socket.inet_ntop(socket.AF_INET, addr[4][0:4])
            if addr[0] == socket.AF_INET
            else socket.inet_ntop(socket.AF_INET6, addr[4][0:16])
            for addr in socket.getaddrinfo(host, None)
        ]
    except socket.gaierror:
        return []

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private/reserved range."""
    try:
        return ipaddress.ip_address(ip).is_private or \
               ipaddress.ip_address(ip).is_loopback or \
               ipaddress.ip_address(ip).is_link_local or \
               ipaddress.ip_address(ip).is_reserved
    except ValueError:
        # Not a valid IP address
        return True

def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that a URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_inspect : str
        The URL to be verified.

    Returns
    -------
    str
        The validated URL (unchanged if valid).

    Raises
    ------
    ValueError
        If the URL does not belong to a trusted domain or attempts to reach
        an internal/sensitive network location.
    """
    parsed = urlparse(url_to_inspect)

    # Basic scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc).")

    # Separate host and port
    host, _, port = parsed.netloc.partition(":")
    if not host:
        raise ValueError("URL netloc must contain a hostname or IP address.")

    # 1. If host is an IP literal, ensure it's not private
    if _is_ip_address(host):
        if _is_private_ip(host):
            raise ValueError("IP address points to a private or reserved network.")
        # All good – return as is
        return urlunparse(parsed)

    # 2. Host is a domain name – check against trusted list
    if host.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the trusted domain list.")

    # 3. Resolve host to IP(s) and ensure none are private
    resolved_ips = _resolve_to_ips(host)
    if not resolved_ips:
        raise ValueError(f"Unable to resolve hostname: {host}")

    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(
                f"Resolved IP {ip} for host {host} is private or reserved."
            )

    # If we reach here, the URL passed all checks
    return urlunparse(parsed)