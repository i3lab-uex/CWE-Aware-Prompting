import re
import socket
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
#   Approved external API domains
# --------------------------------------------------------------------------- #
APPROVED_DOMAINS = {
    "api.openai.com",
    "api.example.com",      # add your trusted domains here
}

# --------------------------------------------------------------------------- #
#   Helper functions
# --------------------------------------------------------------------------- #
def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or reserved range."""
    # IPv4
    private_ipv4 = (
        re.compile(r"^10\."),
        re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\."),
        re.compile(r"^192\.168\."),
    )
    for pattern in private_ipv4:
        if pattern.match(ip):
            return True

    # IPv6
    private_ipv6 = (
        re.compile(r"^fc00:"),
        re.compile(r"^fd00:"),
    )
    for pattern in private_ipv6:
        if pattern.match(ip):
            return True

    # Reserved IPs
    reserved_ips = (
        "0.0.0.0",
        "127.0.0.1",
        "169.254.",
        "255.255.255.255",
    )
    for reserved in reserved_ips:
        if ip.startswith(reserved):
            return True

    return False


def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve hostname to all IPv4 and IPv6 addresses."""
    try:
        infos = socket.getaddrinfo(hostname, None)
        return list({info[4][0] for info in infos})
    except socket.gaierror:
        return []


# --------------------------------------------------------------------------- #
#   Main function
# --------------------------------------------------------------------------- #
def check_api_url(endpoint_url: str) -> str:
    """
    Validate that the provided URL points to an approved external API.

    Parameters
    ----------
    endpoint_url : str
        The URL to be validated.

    Returns
    -------
    str
        A normalized URL that has been confirmed to point to an approved domain.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain, targets a private or
        reserved address, or uses an unsupported scheme.
    """
    # Parse and normalize the URL
    parsed = urlparse(endpoint_url)
    if not parsed.scheme or parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject obvious internal hostnames
    if re.match(r"^(localhost|127\.0\.0\.1|::1)$", hostname, re.I):
        raise ValueError("Internal hostnames are not allowed")

    # Resolve the hostname to IP addresses
    ip_addresses = _resolve_hostname(hostname)
    if not ip_addresses:
        raise ValueError(f"Unable to resolve hostname: {hostname}")

    # Ensure no IP resolves to a private or reserved address
    for ip in ip_addresses:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname resolves to a private address: {ip}")

    # Verify that the hostname is in the approved list
    if hostname.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Hostname '{hostname}' is not an approved domain")

    # Rebuild the URL to ensure consistent formatting
    normalized_url = urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc,
            parsed.path or "",
            "",  # params
            parsed.query or "",
            "",  # fragment
        )
    )

    return normalized_url