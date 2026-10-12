import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# A minimal set of externally‑facing domains that are explicitly allowed.
# If you need a more comprehensive whitelist, extend this list.
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.public.org",
}

# Regular expression to detect common private/loopback IP patterns.
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),  # link‑local
    ipaddress.ip_network("::1/128"),        # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),       # IPv6 unique local address
]


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address string is in a private range."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return any(addr in net for net in PRIVATE_IP_RANGES)


def _hostname_is_allowed(hostname: str) -> bool:
    """Check if a hostname is on the whitelist or resolves to an external IP."""
    # Reject obvious localhost patterns
    if hostname in ("localhost", "127.0.0.1", "::1"):
        return False

    # If the hostname is an IP literal, check it directly
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", hostname) or re.match(r"^[0-9a-fA-F:]+$", hostname):
        return not _is_private_ip(hostname)

    # Normal domain name
    if hostname.lower() in ALLOWED_DOMAINS:
        return True

    # Resolve the hostname to all addresses and ensure none are private
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        # DNS resolution failed; treat as disallowed
        return False

    for family, _, _, _, sockaddr in infos:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            return False

    # If we reach here, the hostname resolved only to public IPs
    return True


def verify_api_address(endpoint_address: str) -> str:
    """
    Validate that the supplied URL points to a secure, external API endpoint.

    Parameters
    ----------
    endpoint_address : str
        The URL to be validated.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, does not use HTTPS,
        targets a private/internal address, or is otherwise disallowed.
    """
    if not endpoint_address:
        raise ValueError("Endpoint address must be a non-empty string")

    parsed = urlparse(endpoint_address)

    # Basic scheme check
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for external API calls")

    # Netloc must contain a hostname
    if not parsed.hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Validate hostname against whitelist / private IP checks
    if not _hostname_is_allowed(parsed.hostname):
        raise ValueError(f"Hostname '{parsed.hostname}' is not allowed (private or unapproved)")

    # Reconstruct the URL to ensure consistent formatting
    cleaned = urlunparse(parsed._replace(scheme="https"))
    return cleaned