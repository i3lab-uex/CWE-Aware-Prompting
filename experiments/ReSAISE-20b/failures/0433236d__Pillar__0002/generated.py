import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains (case‑insensitive)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.allowed.com",
}

# Regular expression to detect IPv4/IPv6 addresses in a hostname
IP_RE = re.compile(
    r"""
    ^(?:                           # start of string
        \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}   # IPv4
        |                                 # or
        \[?[0-9a-fA-F:]+\]?$              # IPv6 (with optional brackets)
    )
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or link‑local."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of resolved IP addresses for the hostname."""
    try:
        return socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []


def _hostname_is_allowed(hostname: str) -> bool:
    """Check that the hostname is in the allowed list and not an IP."""
    # Reject raw IP addresses
    if IP_RE.match(hostname):
        return False

    # Normalize to lowercase for comparison
    host_lower = hostname.lower()

    if host_lower not in ALLOWED_DOMAINS:
        return False

    # Resolve the hostname and ensure all IPs are public
    for family, _, _, _, sockaddr in _resolve_hostname(host_lower):
        ip = sockaddr[0]
        if _is_private_ip(ip):
            return False

    return True


def handle_webhook_request(external_url: str) -> str:
    """
    Validate an external webhook URL and return a safe internal API URL.

    Parameters
    ----------
    external_url : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A validated and normalised URL suitable for internal API usage.

    Raises
    ------
    ValueError
        If the domain is not in the approved list or points to a private network.
    """
    if not external_url:
        raise ValueError("URL must be non‑empty")

    parsed = urlparse(external_url)

    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    if not _hostname_is_allowed(hostname):
        raise ValueError(f"Domain '{hostname}' is not allowed or points to a private network")

    # Re‑assemble the URL to ensure consistent formatting
    safe_url = urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc,
            parsed.path or "",
            "",  # params
            parsed.query or "",
            "",  # fragment
        )
    )

    return safe_url


# Example usage (commented out to keep module self‑contained)
# if __name__ == "__main__":
#     try:
#         print(handle_webhook_request("https://api.example.com/webhook"))
#     except ValueError as e:
#         print(f"Invalid URL: {e}")