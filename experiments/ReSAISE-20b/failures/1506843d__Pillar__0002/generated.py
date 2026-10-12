import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of domains that are explicitly trusted for external API calls.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.trusted.org",
    # Add more trusted domains as needed.
}

# Regular expression to detect common internal IP address patterns
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}          |  # 10.0.0.0/8
        172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3} |  # 172.16.0.0/12
        192\.168\.\d{1,3}\.\d{1,3}              |  # 192.168.0.0/16
        127\.\d{1,3}\.\d{1,3}\.\d{1,3}          |  # localhost
        ::1                                     |  # IPv6 loopback
        fc00::/7                                 # Unique local address (ULA)
    )
    $
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private or reserved range."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        return False

def _resolve_host_to_ip(host: str) -> str:
    """Resolve a hostname to its first IPv4 address."""
    try:
        # Prefer IPv4 addresses
        infos = socket.getaddrinfo(host, None, family=socket.AF_INET)
        if not infos:
            raise ValueError(f"Unable to resolve host: {host}")
        return infos[0][4][0]
    except socket.gaierror as exc:
        raise ValueError(f"DNS resolution failed for {host}: {exc}") from exc

def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that the supplied URL points to an external, trusted API endpoint.
    
    Parameters
    ----------
    url_to_inspect : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL does not belong to a trusted domain or attempts to access an internal
        network location.
    """
    # Basic parsing and scheme validation
    parsed = urlparse(url_to_inspect)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Ensure netloc is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc).")

    # Normalize host: strip port if present
    host, _, port = parsed.netloc.partition(":")
    host_lower = host.lower()

    # Check against the trusted domain list
    if host_lower not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the list of trusted domains.")

    # Resolve hostname to IP and check for private addresses
    ip = _resolve_host_to_ip(host_lower)
    if _is_private_ip(ip):
        raise ValueError(f"Resolved IP {ip} for host '{host}' is private or internal.")

    # Reconstruct the URL to ensure it uses the resolved IP if needed
    # (This step is optional; we simply return the original URL for clarity.)
    validated_url = urlunparse(parsed)
    return validated_url