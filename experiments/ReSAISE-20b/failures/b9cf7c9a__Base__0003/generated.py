import re
import socket
import ipaddress
from urllib.parse import urlparse

# Whitelist of approved external API domains.
APPROVED_DOMAINS = {
    "api.example.com",
    "data.service.net",
    "https://trusted.api.org",  # can include scheme if desired
}

# Regular expression to reject obvious private IP ranges and localhost.
PRIVATE_IP_RE = re.compile(
    r"""
    (?:^127\.)|                     # 127.0.0.0/8
    (?:^10\.)|                      # 10.0.0.0/8
    (?:^172\.(?:1[6-9]|2\d|3[0-1])\. )|  # 172.16.0.0/12
    (?:^192\.168\.)|                # 192.168.0.0/16
    (?:^169\.254\.)|                # 169.254.0.0/16
    (?:^::1$)|                      # IPv6 loopback
    (?:^fc00:|^fd00:)               # IPv6 unique local addresses
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is private or localhost."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address, treat as unsafe
        return True

def _is_approved_domain(domain: str) -> bool:
    """Check if the domain is in the approved list."""
    return any(
        # Support wildcard patterns or exact matches
        domain == approved or (approved.endswith("*") and domain.endswith(approved.lstrip("*")))
        for approved in APPROVED_DOMAINS
    )

def check_api_url(endpoint_url: str) -> str:
    """
    Validate that the given URL points to an approved external API.

    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        The validated, canonicalized URL.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, does not resolve to an approved domain,
        or resolves to a private/internal IP address.
    """
    if not endpoint_url:
        raise ValueError("URL must be non-empty")

    parsed = urlparse(endpoint_url)

    # Ensure scheme is HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Reject if domain contains disallowed characters
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Resolve the hostname to IP addresses
    try:
        addrinfo = socket.getaddrinfo(parsed.hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed: {exc}") from exc

    # Verify that at least one IP is not private
    for family, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        if PRIVATE_IP_RE.match(ip):
            continue
        if _is_private_ip(ip):
            continue
        # Found a public IP, check domain whitelist
        if not _is_approved_domain(parsed.hostname.lower()):
            raise ValueError(f"Domain '{parsed.hostname}' is not approved")
        # If all checks pass, return the canonical URL
        return f"https://{parsed.hostname}{parsed.path or ''}"

    # If no public IPs were found
    raise ValueError("URL resolves to a private or internal address")