import socket
import ipaddress
from urllib.parse import urlparse

# List of approved external API domains (case‑insensitive)
APPROVED_DOMAINS = {
    "api.openai.com",
    "api.github.com",
    "example-external-api.com",
}

# IP networks considered internal/private
INTERNAL_IP_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),  # link‑local
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),        # unique local
]

def _is_internal_ip(ip: str) -> bool:
    """Return True if the given IP string is in a private/internal network."""
    addr = ipaddress.ip_address(ip)
    return any(addr in net for net in INTERNAL_IP_NETWORKS)

def verify_api_link(url_to_check: str) -> str:
    """
    Validate that `url_to_check` points to an approved external API.

    The function checks:
      1. The URL is well‑formed and uses http/https.
      2. The hostname resolves to at least one IP address that is not internal/private.
      3. The hostname matches an entry in the approved domain list.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        resolves to a private/internal IP address, or
        does not belong to an approved domain.
    """
    # 1. Parse and validate scheme
    parsed = urlparse(url_to_check)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # 2. Resolve hostname to IPs
    try:
        addr_info = socket.getaddrinfo(parsed.hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for {parsed.hostname}") from exc

    # 3. Ensure at least one resolved IP is not internal
    for entry in addr_info:
        ip = entry[4][0]
        if not _is_internal_ip(ip):
            break
    else:
        raise ValueError("All resolved IPs are internal/private; URL is disallowed")

    # 4. Verify domain against approved list (case‑insensitive)
    hostname = parsed.hostname.lower()
    if hostname not in APPROVED_DOMAINS:
        # Allow subdomains of approved domains
        matched = any(hostname.endswith("." + domain) for domain in APPROVED_DOMAINS)
        if not matched:
            raise ValueError(f"Domain {hostname} is not in the approved list")

    return url_to_check