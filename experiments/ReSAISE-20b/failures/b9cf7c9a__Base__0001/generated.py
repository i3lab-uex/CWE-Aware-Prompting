import re
import socket
from urllib.parse import urlparse, urlunparse
from ipaddress import ip_address, IPv4Address, IPv6Address

# A simple whitelist of approved external domains.
# Add or remove entries as your policy requires.
APPROVED_DOMAINS = {
    "api.example.com",
    "service.otherdomain.org",
    # allow subdomains of a domain
    r"^.*\.trustedapi\.net$",
}

# Regular expression to detect IP addresses in the hostname
IP_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$|^[0-9a-fA-F:]+$")

def _is_ip(hostname: str) -> bool:
    """Return True if hostname is an IP address."""
    return bool(IP_RE.match(hostname))

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is private, loopback or otherwise non‑public."""
    try:
        ip_obj = ip_address(ip)
        return (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
            or ip_obj.is_multicast
        )
    except ValueError:
        return False

def _is_approved_domain(hostname: str) -> bool:
    """Check if the hostname matches any approved domain pattern."""
    for pattern in APPROVED_DOMAINS:
        if re.match(pattern, hostname):
            return True
    return False

def check_api_url(endpoint_url: str) -> str:
    """
    Validate that the supplied URL points to an approved external API.

    Parameters
    ----------
    endpoint_url : str
        The URL provided by an untrusted source.

    Returns
    -------
    str
        The original URL if it is approved.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain or resolves to a private/internal IP.
    """
    if not endpoint_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(endpoint_url)

    # Basic scheme check
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract hostname
    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a hostname")

    # Resolve hostname to IP(s) and validate each
    try:
        resolved_ips = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for {host}") from exc

    # Check that all resolved IPs are public
    for family, _, _, _, sockaddr in resolved_ips:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname {host} resolves to private IP {ip}")

    # Verify hostname against approved list
    if not _is_approved_domain(host):
        raise ValueError(f"Hostname {host} is not in the approved domain list")

    # Reconstruct URL to normalize it (e.g., remove default ports)
    cleaned_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return cleaned_url