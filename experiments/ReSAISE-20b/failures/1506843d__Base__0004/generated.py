import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of domains that are considered trusted for external API calls.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
    # Add more trusted domains here
}

# Regex to detect IPv4 and IPv6 addresses in URLs
IP_REGEX = re.compile(r"""
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[
            (?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}
        \]
    )
""", re.VERBOSE)


def _is_private_ip(ip: str) -> bool:
    """
    Return True if the given IP address string is in a private or reserved range.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved
    except ValueError:
        # Not a valid IP address
        return False


def _hostname_to_ip(hostname: str) -> list[str]:
    """
    Resolve the hostname to a list of IP addresses.  If resolution fails, return an empty list.
    """
    try:
        import socket
        infos = socket.getaddrinfo(hostname, None)
        return list({item[4][0] for item in infos})
    except Exception:
        return []


def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that the supplied URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_inspect : str
        The URL to be verified.

    Returns
    -------
    str
        The original URL if it is considered safe and trusted.

    Raises
    ------
    ValueError
        If the URL resolves to a private, loopback or link‑local address,
        or if its hostname is not in the list of trusted domains.
    """
    # Basic parsing
    parsed = urlparse(url_to_inspect)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must contain a scheme and network location")

    # Reject any URL that explicitly contains an IP address
    if IP_REGEX.search(parsed.netloc):
        # Extract the raw host part (remove optional port)
        host_part = parsed.hostname
        if host_part and _is_private_ip(host_part):
            raise ValueError("URL resolves to a private IP address")
        if host_part and _is_private_ip(host_part.replace("[", "").replace("]", "")):
            raise ValueError("URL resolves to a private IP address")

    # Resolve the hostname and ensure it is not pointing to internal networks
    resolved_ips = _hostname_to_ip(parsed.hostname)
    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"URL resolves to private IP {ip}")

    # Ensure the hostname is in the trusted list
    if parsed.hostname not in TRUSTED_DOMAINS:
        raise ValueError(f"Hostname {parsed.hostname} is not trusted")

    # Re‑assemble the URL to avoid any manipulation
    cleaned = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))
    return cleaned