import re
import socket
from urllib.parse import urlparse, urlunparse
from ipaddress import ip_address, IPv4Address, IPv6Address

# List of allowed public API domains (add more as needed)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
    "data.provider.net",
}

# Regular expression for detecting private or reserved IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^10\.|^172\.(1[6-9]|2[0-9]|3[0-1])\.|^192\.168\.)   # IPv4 private
    |(^127\.)                                            # Loopback
    |(^169\.254\.)                                       # Link-local
    |(^0\.|^255\.|^224\.|^240\.)                         # Reserved
    |(^::1$)                                            # IPv6 loopback
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """
    Check if the given IP address string is in a private or reserved range.
    """
    try:
        addr = ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local
    except ValueError:
        # Not a valid IP address
        return False

def _resolve_hostname(hostname: str) -> set[str]:
    """
    Resolve the hostname to all IPv4/IPv6 addresses.
    Return a set of resolved IP strings.
    """
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    ips = set()
    for info in infos:
        ip_str = info[4][0]
        ips.add(ip_str)
    return ips

def analyze_webhook(webhook_address: str) -> str:
    """
    Validate a webhook URL, ensuring it points to an approved public API domain
    and does not resolve to any private/internal IP addresses.

    Parameters:
        webhook_address (str): The URL supplied by an external service.

    Returns:
        str: A validated URL that can be safely used for internal API requests.

    Raises:
        ValueError: If the domain is not in ALLOWED_DOMAINS or if the URL resolves
                    to a private/internal network address.
    """
    parsed = urlparse(webhook_address)

    # Basic scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS allowed.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname.")

    # Normalize hostname to lower case for comparison
    hostname_lc = hostname.lower()

    if hostname_lc not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not in the list of allowed domains.")

    # Resolve hostname to IPs and check for private/reserved addresses
    resolved_ips = _resolve_hostname(hostname_lc)
    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to private IP '{ip}'. Refusing to use.")

    # Reconstruct the URL ensuring it is canonical
    safe_url = urlunparse(parsed._replace(netloc=hostname_lc + (f":{parsed.port}" if parsed.port else "")))
    return safe_url