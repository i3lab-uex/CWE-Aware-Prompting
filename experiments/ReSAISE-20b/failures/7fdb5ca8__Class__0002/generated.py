import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# A list of domains that are explicitly trusted for external API calls.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.trusted.org",
    "data.partner.net",
}

# Regular expression to detect IP addresses in the URL.
IP_REGEX = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or reserved range."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback or \
               ipaddress.ip_address(ip).is_link_local or ipaddress.ip_address(ip).is_reserved
    except ValueError:
        # Not a valid IP address; treat as non‑private.
        return False

def _is_trusted_domain(host: str) -> bool:
    """Check if the host matches one of the trusted domains."""
    # Exact match or subdomain of a trusted domain
    return any(host == td or host.endswith("." + td) for td in TRUSTED_DOMAINS)

def verify_api_address(url_to_check: str) -> str:
    """
    Validate that a URL points to an external, trusted API.

    Parameters
    ----------
    url_to_check : str
        The URL to be verified.

    Returns
    -------
    str
        The validated URL, unchanged.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an internal address,
        or does not belong to a trusted domain.
    """
    # Basic URL parsing
    parsed = urlparse(url_to_check)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must have a scheme and network location")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject URLs that explicitly use an IP address
    if IP_REGEX.match(host):
        raise ValueError("Using raw IP addresses is not allowed")

    # Resolve the hostname to IPs
    try:
        addr_info = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed: {exc}") from exc

    # Ensure none of the resolved IPs are private
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname resolves to a private IP address: {ip}")

    # Ensure the host is within the trusted domain list
    if not _is_trusted_domain(host):
        raise ValueError(f"Hostname '{host}' is not in the list of trusted domains")

    # Optionally, you can enforce HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for external API calls")

    # Reconstruct the URL to normalize it
    cleaned = urlunparse(parsed._replace(scheme="https", netloc=host))
    return cleaned