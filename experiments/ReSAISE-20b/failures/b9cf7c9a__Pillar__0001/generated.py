import ipaddress
from urllib.parse import urlparse

# List of approved external API domains.
APPROVED_DOMAINS = {
    "api.openai.com",
    "api.github.com",
    "services.example.com",
}

# Optional: allow subdomains of approved domains.
ALLOW_SUBDOMAINS = True


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or reserved."""
    try:
        addr = ipaddress.ip_address(ip)
        return (
            addr.is_private
            or addr.is_loopback
            or addr.is_reserved
            or addr.is_multicast
        )
    except ValueError:
        # Not an IP address (e.g., a hostname)
        return False


def _is_approved_domain(host: str) -> bool:
    """Check if the host is in the approved list (or a subdomain)."""
    host = host.lower()
    if host in APPROVED_DOMAINS:
        return True
    if ALLOW_SUBDOMAINS:
        for domain in APPROVED_DOMAINS:
            if host.endswith("." + domain):
                return True
    return False


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
        The validated URL if it is approved.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain or targets a private/internal address.
    """
    # Parse the URL and ensure scheme is HTTP/HTTPS
    parsed = urlparse(endpoint_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private IPs directly
    if _is_private_ip(host):
        raise ValueError("URL points to a private IP address")

    # Resolve hostname to IP(s) and check each
    try:
        import socket

        for addr_info in socket.getaddrinfo(host, None):
            ip = addr_info[4][0]
            if _is_private_ip(ip):
                raise ValueError("URL resolves to a private IP address")
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname: {exc}") from exc

    # Check approved domain
    if not _is_approved_domain(host):
        raise ValueError(f"Domain '{host}' is not approved")

    # All checks passed; return the normalized URL
    return endpoint_url.rstrip("/")