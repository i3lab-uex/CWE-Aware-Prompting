import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# A simple whitelist of approved domains (case‑insensitive)
WHITELIST = {
    "api.example.com",
    "service.internal.net",
    "trusted.api.org",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    (^127\.|^0\.)|
    (^(10|172\.1[6-9]|172\.2[0-9]|172\.3[01])\.)|
    (^192\.168\.)
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """
    Return True if the given IP address string is private.
    Handles both IPv4 and IPv6 addresses.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to a list of IP addresses.
    Raises socket.gaierror if the hostname cannot be resolved.
    """
    return list({addr[4][0] for addr in socket.getaddrinfo(hostname, None)})


def validate_callback(callback_url: str) -> str:
    """
    Validate a webhook callback URL.

    Parameters
    ----------
    callback_url : str
        The external webhook URL supplied by a third‑party.

    Returns
    -------
    str
        A fully qualified, safe URL that can be used for internal API calls.

    Raises
    ------
    ValueError
        If the URL domain is not in the whitelist or if it resolves to a private/loopback
        IP address. Also raised for malformed URLs or unsupported schemes.
    """
    # Basic URL parsing
    parsed = urlparse(callback_url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Normalize the domain (case‑insensitive)
    host = parsed.hostname.lower()

    if host not in WHITELIST:
        raise ValueError(f"Domain '{host}' is not whitelisted")

    # Resolve the hostname to IP addresses
    try:
        ips = _resolve_hostname(host)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{host}': {exc}") from exc

    # Ensure none of the resolved IPs are private or loopback
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to private IP {ip}")

    # Re‑construct the URL ensuring no query or fragment is present
    safe_url = urlunparse(
        (
            parsed.scheme,
            f"{host}{':' + str(parsed.port) if parsed.port else ''}",
            parsed.path or "/",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return safe_url